import os
from os.path import join, dirname
from dotenv import load_dotenv

from IPython.display import Image, display
from autogen import AssistantAgent, UserProxyAgent
from autogen.coding import LocalCommandLineCodeExecutor

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

config_list = [
    {
        "model": os.environ.get("MODEL"), 
        "api_key": os.environ.get("OPENAI_API_KEY"),
    }
]

llm_config = {
    "cache_seed": 41,  # seed for caching and reproducibility
    "config_list": config_list,  # a list of OpenAI API configurations
    "temperature": 0,  # temperature for sampling
}  # configuration for autogen's enhanced inference API which is compatible with OpenAI API

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
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet.""",
    code_execution_config={
        "executor": LocalCommandLineCodeExecutor(work_dir= "coding"), 
    }  
   
)

task = """
What date is today? Compare the year-to-date gain for META and TESLA.
"""

chat_res = user_proxy.initiate_chat(
    assistant,
    message=task,
    summary_method="reflection_with_llm",
)

user_proxy.send(
    recipient=assistant,
    message="""Plot a chart of their stock price change YTD
    and save to stock_price_ytd.png
    """
)