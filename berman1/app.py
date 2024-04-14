import autogen

config_list = [
    {
        'model': 'gpt-3.5-turbo-16k',
        'api_key': 'sk-1111'
    }
]

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
# Additional Assistants should have a name and a system message explaining their expertise
assistant = autogen.AssistantAgent(
    name="coder",
    llm_config=llm_config,
    system_message="expert python programmer that writes proper python code."
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work-dir": "web"},
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved to the full satisfaction,
    Otherwise, reply CONTINUE, or the reason the task is not solved yet."""    
)


task1="""
Give me a summary of this article: https://apnews.com/article/strait-of-hormuz-vessel-33fcffde2d867380e98c89403776a8ac
"""

user_proxy.initiate_chat(
    assistant,
    message=task1
)
