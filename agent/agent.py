import logging
from uuid import uuid4

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage, AIMessage
from langgraph.checkpoint.memory import InMemorySaver

from objects import Answer
from evaluations.modelzz import groq_model
from tools import (
    calculate_right_refund,
    get_today_date,
    issue_refund_ticket,
    get_user_purchase_history,
)
from prompts import agent_system_prompt

load_dotenv()

logging.basicConfig(level=logging.INFO)

agent = create_agent(
    model=groq_model,
    system_prompt=agent_system_prompt,
    tools=[
        calculate_right_refund,
        get_user_purchase_history,
        issue_refund_ticket,
        get_today_date,
    ],
    checkpointer=InMemorySaver()
)


def run_conversation():
    config = {
        "configurable": {
            "thread_id": str(uuid4())
        }
    }

    question = "I would like to request a refund"
    print(question)

    while True:
        try:
            response = agent.invoke(
                {"messages": [HumanMessage(content=question)]},
                config=config,
            )
            print(response.keys())
            print(response)

        except Exception as exc:
            logging.exception("Agent execution failed")
            print("\nThe agent encountered an error.")
            print("Check your logs and refund records before retrying.")
            print(f"Error: {exc}")
            break

        # Find the latest assistant message that is not a tool call.
        assistant_message = next(
            (
                message
                for message in reversed(response["messages"])
                if isinstance(message, AIMessage)
                and not message.tool_calls
                and message.content
            ),
            None,
        )

        if assistant_message is None:
            print("No final assistant response was generated.")
            break

        content = assistant_message.content

        if isinstance(content, str):
            answer = content
        else:
            # Handle content returned as a list of blocks.
            answer = " ".join(
                block["text"]
                for block in content
                if isinstance(block, dict)
                and block.get("type") == "text"
                and block.get("text")
            )

        if not answer.strip():
            print("The agent returned an empty response.")
            break

        print(answer)

        # Ask the user whether the conversation should continue.
        user_input = input("\nReply, or type 'exit' to stop: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Conversation ended.")
            break

        if not user_input:
            print("Please enter a response.")
            continue

        question = user_input


if __name__ == "__main__":
    run_conversation()