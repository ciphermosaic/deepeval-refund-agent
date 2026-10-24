# from dotenv import load_dotenv
# from langchain.chat_models import init_chat_model
# from langchain_groq import ChatGroq
# from langchain_google_genai import ChatGoogleGenerativeAI
# load_dotenv()

# groq_model = ChatGroq(model="openai/gpt-oss-120b", temperature=0)

# # model = ChatGoogleGenerativeAI(
# #     model="gemini-3.8-flash",
# #     temperature=0,
# # )

# # response = model.invoke("tell me about sun in short.")

# # print(response)


# from deepeval.models import DeepEvalBaseLLM

# # Keep your existing ChatGroq configuration.
# # Example: eval_model = ChatGroq(...)

# class GroqEvalModel(DeepEvalBaseLLM):
#     def __init__(self, model):
#         self.model = model

#     def load_model(self):
#         return self.model

#     def generate(self, prompt: str, schema=None):
#         response = self.model.invoke(prompt)
#         output = response.content

#         if schema is not None:
#             import json

#             if isinstance(output, list):
#                 output = "".join(
#                     item.get("text", "") if isinstance(item, dict)
#                     else str(item)
#                     for item in output
#                 )

#             data = json.loads(output)
#             return schema.model_validate(data)

#         return output

#     async def a_generate(self, prompt: str, schema=None):
#         response = await self.model.ainvoke(prompt)
#         output = response.content

#         if schema is not None:
#             import json

#             if isinstance(output, list):
#                 output = "".join(
#                     item.get("text", "") if isinstance(item, dict)
#                     else str(item)
#                     for item in output
#                 )

#             data = json.loads(output)
#             return schema.model_validate(data)

#         return output

#     def get_model_name(self):
#         return "Groq GPT OSS 120B"


# eval_model = GroqEvalModel(model=groq_model)

# if __name__ == "__main__":
#     response = eval_model.generate("Tell me about the Sun in short.")
#     print(response)