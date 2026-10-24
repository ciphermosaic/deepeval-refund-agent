import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "agent")
)

from agent import agent
from dataset import dataset
from modelzz import eval_model

from deepeval.metrics import ToolCorrectnessMetric
from deepeval.integrations.langchain import CallbackHandler
from deepeval.test_case import LLMTestCase, ToolCall
from deepeval import evaluate
from dotenv import load_dotenv

load_dotenv()

for golden in dataset.goldens:
    response = agent.invoke(
        {"messages": [{"role": "user", "content": golden.input}]},
        config={"configurable": {"thread_id": str(uuid4())},
        "callbacks": [CallbackHandler()]}
    )

    actual_output = response["structured_response"].answer

    tools_called = []
    test_cases = []

    for message in response["messages"]:
        for tool_call in getattr(message, "tool_calls", []) or []:
            tools_called.append(
                ToolCall(name=tool_call["name"], input_parameters=tool_call["args"])
            )

    test_case = LLMTestCase(
        input=golden.input,
        actual_output=actual_output,
        tools_called=tools_called,
        expected_tools=golden.expected_tools
    )

    dataset.add_test_case(test_case)

metrics = [ToolCorrectnessMetric(threshold=0.8,model=eval_model,include_reason=True)]

evaluate(test_cases=dataset.test_cases, metrics=metrics)