import os
from os.path import join, dirname
from dotenv import load_dotenv

from autogen import AssistantAgent, UserProxyAgent

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

config_list = [
    {"model": "gpt-3.5-turbo-16k", "api_key": os.environ.get("OPENAI_API_KEY")}
]

llm_config = {
    "timeout": 600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0,  # For Coding, 0 is good
}

assistant = AssistantAgent(
    name="assistant",
    llm_config=llm_config,
    # system_message  Use when you have more than one agent
)


def termination_msg(x):
    return isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()


user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",  # "ALWAYS", "TERMINATE", "NEVER"
    max_consecutive_auto_reply=10,
    is_termination_msg=termination_msg,
    code_execution_config={"work_dir": "web", "use_docker": "python:bullseye"},
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet.""",
)

task = """
Write python code to output numbers 1 to 100, and then store the code in a file
"""

user_proxy.initiate_chat(assistant, message=task)

task2 = """
Change the code in the file you just created to instead output numbers 1 to 200
"""

user_proxy.initiate_chat(assistant, message=task2)
