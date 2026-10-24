
import os

from dotenv import load_dotenv
from deepeval.models import DeepEvalBaseLLM
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


# 1. Keep Groq for your refund agent.
groq_model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
)


# 2. Gemini model for DeepEval metrics.
gemini_model = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    temperature=0,
    google_api_key=(
        os.getenv("GOOGLE_API_KEY")
        or os.getenv("GEMINI_API_KEY")
    ),
)


# 3. DeepEval-compatible wrapper for Gemini.
class GeminiEvalModel(DeepEvalBaseLLM):

    def __init__(self, model):
        self.model = model

    def load_model(self):
        return self.model

    def get_model_name(self):
        return "Gemini 3.8 Flash"

    def generate(self, prompt: str, schema=None):
        if schema is not None:
            structured_model = self.model.with_structured_output(schema)
            return structured_model.invoke(prompt)

        response = self.model.invoke(prompt)
        return response.content

    async def a_generate(self, prompt: str, schema=None):
        if schema is not None:
            structured_model = self.model.with_structured_output(schema)
            return await structured_model.ainvoke(prompt)

        response = await self.model.ainvoke(prompt)
        return response.content


# 4. Export this variable for your DeepEval metrics.
eval_model = GeminiEvalModel(model=gemini_model)


# 5. Test Gemini independently when running this file.
if __name__ == "__main__":
    response = eval_model.generate(
        "Explain what a refund agent does in one sentence."
    )
    print(response)
