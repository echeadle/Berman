import pprint

from autogen import AssistantAgent, UserProxyAgent

pprint.pprint(AssistantAgent.DEFAULT_SYSTEM_MESSAGE)

print("*" * 50)

pprint.pprint(UserProxyAgent.DEFAULT_SYSTEM_MESSAGE)