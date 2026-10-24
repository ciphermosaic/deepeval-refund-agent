import sys
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv

from langchain.messages import AIMessage
from deepeval import evaluate
from deepeval.evaluate import CacheConfig, DisplayConfig
from deepeval.integrations.langchain import CallbackHandler
from deepeval.metrics import (
    ArgumentCorrectnessMetric,
    GEval,
    PlanAdherenceMetric,
    PlanQualityMetric,
    StepEfficiencyMetric,
    TaskCompletionMetric,
    ToolCorrectnessMetric,
)
from deepeval.test_case import LLMTestCase, SingleTurnParams, ToolCall, ToolCallParams

if __package__:
    from .dataset import dataset
    from .modelzz import eval_model
else:
    from dataset import dataset
    from modelzz import eval_model


SUCCESSFUL_TASK_DESCRIPTION = """
If the username is missing, ask the user to provide it.
For a refund request, identify the customer and the requested purchases, and
check that each purchase is no more than 30 days old and is not in the future.
Refund only the items requested by the user. If the customer or requested item
cannot be found, do not issue a refund ticket and explain why.
Once the necessary information is available, tell the user whether a refund
ticket was issued and its amount, or explain why no refund was issued.
For an information-only request, answer the question without issuing a ticket.
"""


def build_metrics():
    """Keep the thresholds and evaluator model used by the individual scripts."""
    trace_metrics = [
        TaskCompletionMetric(
            threshold=0.8,
            model=eval_model,
            task=SUCCESSFUL_TASK_DESCRIPTION,
            include_reason=True,
            async_mode=False
        ),
        StepEfficiencyMetric(
            threshold=0.8, model=eval_model, include_reason=True, async_mode=False
        ),
        PlanQualityMetric(
            threshold=0.8, model=eval_model, include_reason=True, async_mode=False
        ),
        PlanAdherenceMetric(
            threshold=0.8, model=eval_model, include_reason=True, async_mode=False
        ),
    ]
    single_turn_metrics = [
        ArgumentCorrectnessMetric(
            threshold=None, 
            model=eval_model,
            include_reason=True,
            async_mode=False
        ),
        ToolCorrectnessMetric(
            threshold=0.9, 
            model=eval_model,
            include_reason=True,
            evaluation_params=[ToolCallParams.INPUT_PARAMETERS],
            async_mode=False
        ),
        GEval(
            name="Answer Correctness",
            evaluation_params=[
                SingleTurnParams.INPUT,
                SingleTurnParams.ACTUAL_OUTPUT,
                SingleTurnParams.EXPECTED_OUTPUT,
            ],
            evaluation_steps=[
                "Check that the actual output and expected output have the same "
                "logical conclusion about the user's request.",
            ],
            threshold=0.8,
            model=eval_model,
            verbose_mode=True,
            async_mode=False
        ),
    ]
    return trace_metrics, single_turn_metrics


def main():
    load_dotenv()
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent"))
    from agent import agent

    trace_metrics, single_turn_metrics = build_metrics()
    cache_config = CacheConfig(use_cache=False, write_cache=False)
    display_config = DisplayConfig(inspect_after_run=False)
    test_cases = []

    # The callback captures the trace required by the four agentic metrics.
    for i, golden in enumerate(
        dataset.evals_iterator(
            metrics=trace_metrics,
            cache_config=cache_config,
            display_config=display_config,
        )
    ):
        if i >= 2:
            break
        response = agent.invoke(
            {"messages": [{"role": "user", "content": golden.input}]},
            config={
                "configurable": {"thread_id": str(uuid4())},
                "callbacks": [CallbackHandler()],
            },
        )

        tools_called = []
        for message in response["messages"]:
            for tool_call in getattr(message, "tool_calls", []) or []:
                tools_called.append(
                    ToolCall(
                        name=tool_call["name"],
                        input_parameters=tool_call["args"],
                    )
                )

        # Reuse the same response for the three remaining metrics. Keep these
        # cases local so repeated runs do not accumulate dataset.test_cases.
        test_cases.append(
            LLMTestCase(
                input=golden.input,
                actual_output=next(
                    message.content
                    for message in reversed(response["messages"])
                    if isinstance(message, AIMessage)
                    and not message.tool_calls
                    and message.content
                ),
                expected_output=golden.expected_output,
                tools_called=tools_called,
                expected_tools=golden.expected_tools,
            )
        )

    evaluate(
        test_cases=test_cases,
        metrics=single_turn_metrics,
        cache_config=cache_config,
        display_config=display_config,
    )
    print(f"\nCompleted all 7 metrics for {len(test_cases)} test cases.")


if __name__ == "__main__":
    main()

def test_all_evals():
    main()