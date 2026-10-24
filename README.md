# Refund Agent Evaluation with DeepEval

An AI-powered refund agent built with LangChain and LangGraph, with a primary focus on **LLM evaluation using DeepEval**.

This project demonstrates how to evaluate a tool-using AI agent beyond whether its final answer looks correct. It uses multiple evaluation metrics to assess task completion, planning, tool usage, argument correctness, and answer quality.

## Project Focus: LLM Evaluation

The main goal of this project is to demonstrate practical skills in evaluating LLM-powered agents, identifying failure points, and measuring agent performance using DeepEval.

### Evaluation Metrics

The project implements seven DeepEval metrics across agent-trace and single-turn evaluation stages.

**Agent Trace Metrics**

| Metric | What it evaluates |
|---|---|
| Task Completion | Whether the agent successfully completes the user's intended task. |
| Step Efficiency | How efficiently the agent executes its steps. |
| Plan Quality | The quality of the agent's execution plan. |
| Plan Adherence | Whether the agent follows its intended plan. |

**Single-Turn Metrics**

| Metric | What it evaluates |
|---|---|
| Argument Correctness | Whether the arguments supplied to tools are correct. |
| Tool Correctness | Whether the agent calls the expected tools. |
| Answer Correctness (GEval) | Whether the final answer reaches the correct logical conclusion. |

### Evaluation Implementation

- **Custom evaluation model wrapper:** Integrates Gemini with DeepEval through `DeepEvalBaseLLM`.
- **LLM-as-a-judge:** Uses an LLM to assess agent responses against evaluation criteria.
- **Threshold-based scoring:** Configures metric thresholds to determine whether evaluation results meet defined standards.
- **Reason generation:** Enables explanations for metric scores to help interpret evaluation results.
- **Tool-call evaluation:** Compares actual tool usage against expected tool calls.
- **Trace-based evaluation:** Uses LangChain callback integration to capture execution traces for agentic metrics.
- **Evaluation dataset:** Uses predefined inputs, expected outputs, and expected tools to assess agent behavior.

## Refund Agent

The refund agent serves as the system under evaluation. It uses tools to retrieve purchase history, calculate eligible refunds, validate dates, and issue refund tickets when appropriate.

The agent is built with:

- Python
- LangChain
- LangGraph
- Groq API
- Pydantic

## Tech Stack

- **Evaluation:** DeepEval
- **Evaluation model:** Google Gemini API
- **Agent model:** Groq API
- **Agent framework:** LangChain and LangGraph
- **Validation:** Pydantic
- **Configuration:** python-dotenv
- **Testing:** Pytest and DeepEval CLI


## Understanding Evaluation Results

| Status | Meaning |
|---|---|
| PASSED | The metric met its configured threshold. |
| FAILED | The metric did not meet its threshold, or the enclosing test failed. |
| ERRORED | Evaluation could not complete because of an exception, timeout, or API error. |
| NONE | No pass/fail decision was made, such as when no threshold is configured. |

A key part of LLM evaluation is distinguishing an actual agent failure from an evaluator failure. API rate limits, timeouts, and malformed evaluator responses can prevent a metric from producing a valid score.

## What This Project Demonstrates

- Designing an evaluation suite for a tool-using AI agent.
- Implementing and configuring multiple DeepEval metrics.
- Integrating a custom LLM evaluator.
- Capturing agent traces for agentic evaluation.
- Evaluating tool selection, tool arguments, and final answers.
- Using thresholds and metric reasons to interpret evaluation results.
- Debugging evaluation failures caused by API limits and timeouts.

## Author

**Abubakar**

AI/ML student focused on LLM evaluation, agentic AI, and building reliable AI applications.
