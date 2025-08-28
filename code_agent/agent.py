import os
import logging

from google.adk.agents import LlmAgent
from google.adk.code_executors import GkeCodeExecutor

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper())
logger = logging.getLogger(__name__)


# Agent Definition
root_agent = LlmAgent(
    name="coding_agent",
    model="gemini-2.0-flash",

 instruction="""You are a helpful and capable AI agent that can write and execute Python code to answer questions and perform tasks.

When a user asks a question, follow these steps:
1. Analyze the request.
2. Write a complete, self-contained Python script to accomplish the task.
3. Your code will be executed in a secure environment.
4. Return the full and complete output from the code execution, including any text, results, or error messages.""",
description="A general-purpose agent that executes Python code to answer questions or perform tasks.",
    code_executor=GkeCodeExecutor(
        namespace="default",
    ),
)
logger.info(f"ADK Agent '{root_agent.name}' created.")
