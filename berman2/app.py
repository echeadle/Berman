import autogen
import tempfile
from autogen.coding import DockerCommandLineCodeExecutor

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-3.5-turbo", "gpt-3.5-turbo-1106"]
    }    
)

llm_config={
    "timeout": 600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0
}

assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config,
)

temp_dir = tempfile.TemporaryDirectory()


with DockerCommandLineCodeExecutor(work_dir=work_dir) as code_executor:
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config={"executor": code_executor},
        llm_config=llm_config,
        system_message="""Reply TERMINATE if the task has been solved to the full satisfaction,
        Otherwise, reply CONTINUE, or the reason the task is not solved yet."""
    )

# user_proxy = autogen.UserProxyAgent(
#     name="user_proxy",
#     human_input_mode="NEVER",
#     max_consecutive_auto_reply=10,
#     is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
#     code_execution_config={"executor": code_executor},,
#     llm_config=llm_config,
#     system_message="""Reply TERMINATE if the task has been solved to the full satisfaction,
#     Otherwise, reply CONTINUE, or the reason the task is not solved yet."""    
# )


    
user_proxy.initiate_chat(
    assistant,
    message="""What date is today? Compare the year-to-date gain for META and TESLA.""",
    summary_method="reflection_with_llm",
)