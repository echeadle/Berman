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
    is_termination_msg=lambda x: True if "TERMINATE" in x.get("content") else False,
)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: True if "TERMINATE" in x.get("content") else False,
    max_consecutive_auto_reply=10,
    code_execution_config={
        "work_dir": "work_dir",
        "use_docker": False,
    },
)

task1 = """
Find arxiv papers that show how are people studying trust calibration in AI based systems
"""
user_proxy.initiate_chat(assistant, message=task1)

task2 = "analyze the above the results to list the application domains studied by these papers "
user_proxy.initiate_chat(assistant, message=task2, clear_history=False)

task3 = """Use this data to generate a bar chart of domains and number of papers in that domain and save to a file
"""
user_proxy.initiate_chat(assistant, message=task3, clear_history=False)


task4 = """Reflect on the sequence and create a recipe containing all the steps
necessary and name for it. Suggest well-documented, generalized python function(s)
 to perform similar tasks for coding steps in future. Make sure coding steps and
 non-coding steps are never mixed in one function. In the docstr of the function(s),
 clarify what non-coding steps are needed to use the language skill of the assistant.
"""
user_proxy.initiate_chat(assistant, message=task4, clear_history=False)