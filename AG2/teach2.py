# create an AssistantAgent instance named "assistant"
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

task1 = '''
This recipe is available for you to reuse..

<begin recipe>
**Recipe Name:** Analyzing and Visualizing Application Domains in Arxiv Papers

**Steps:**

1. Collect relevant papers from arxiv using a search query.
2. Analyze the abstracts of the collected papers to identify application domains.
3. Count the number of papers in each application domain.
4. Generate a bar chart of the application domains and the number of papers in each domain.
5. Save the bar chart as an image file.

Here are the well-documented, generalized Python functions to perform the coding steps in the future:

```python
import requests
import feedparser
import matplotlib.pyplot as plt
from typing import List, Dict

def search_arxiv(query: str, max_results: int = 10) -> List[Dict[str, str]]:
    """
    Search arxiv for papers related to a specific query.

    :param query: The search query for arxiv papers.
    :param max_results: The maximum number of results to return. Default is 10.
    :return: A list of dictionaries containing the title, link, and summary of each paper.
    """
    base_url = "http://export.arxiv.org/api/query?"
    search_query = f"search_query=all:{query}"
    start = 0
    max_results = f"max_results={max_results}"
    url = f"{base_url}{search_query}&start={start}&{max_results}"
    response = requests.get(url)
    feed = feedparser.parse(response.content)

    papers = [{"title": entry.title, "link": entry.link, "summary": entry.summary} for entry in feed.entries]
    return papers

def generate_bar_chart(domains: Dict[str, int], output_file: str) -> None:
    """
    Generate a bar chart of application domains and the number of papers in each domain, and save it as an image file.

    :param domains: A dictionary containing application domains as keys and the number of papers as values.
    :param output_file: The name of the output image file.
    """
    fig, ax = plt.subplots()
    ax.bar(domains.keys(), domains.values())
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Application Domains")
    plt.ylabel("Number of Papers")
    plt.title("Number of Papers per Application Domain")

    plt.tight_layout()
    plt.savefig(output_file)
    plt.show()
```

**Usage:**

1. Use the `search_arxiv` function to collect relevant papers from arxiv using a search query.
2. Analyze the abstracts of the collected papers using your language skills to identify application domains and count the number of papers in each domain.
3. Use the `generate_bar_chart` function to generate a bar chart of the application domains and the number of papers in each domain, and save it as an image file.

</end recipe>


Here is a new task:
Plot a chart for application domains of GPT models
'''

user_proxy.initiate_chat(assistant, message=task1)