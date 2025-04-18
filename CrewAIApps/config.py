from os import environ as env
from dotenv import load_dotenv
load_dotenv()

import openai
from langchain.llms import OpenAI

api_key = env["OPENAI_API_KEY"]
openai.api_key = api_key

# Step 2: Initialize the LLM gpt-3.5-turbo, gpt-4o, gpt-4.1-mini, gpt-4, gpt-4o
llm = OpenAI(model="gpt-4", temperature=0.7, openai_api_key=api_key) # gpt-4o-mini, # gpt-3.5-turbo

# openai_embeddings = OpenAIEmbeddings(
#     model="text-embedding-ada-002",
#     openai_api_key=api_key
# )

# from openai import OpenAI
# client = OpenAI()

# gpt-4.1-2025-04-14
# response = client.responses.create(
#     model="gpt-4.1",
#     instructions="Talk like a pirate.",
#     input="Are semicolons optional in JavaScript?",
# )

# print(response.output_text)


# 🚫 Not Supported:
# gpt-4.1-mini
# gpt-4o-mini
# gpt-mini
# gpt-small, etc.