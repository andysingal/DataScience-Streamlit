import os
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain import hub
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from ReachOut.tools.tools import tavily_crawl_for_linkedIn_url

load_dotenv()

def profile_url_search(persons_detail: str) -> str:
    model = ChatOpenAI(
        model='gpt-3.5-turbo',
        temperature=0.2,
    )
    
    raw_prompt = """
        Objective: Provide the LinkedIn profile URL for the specified individual.
        Instructions:

        - Input Variable: `{persons_detail}` (This represents the full name of the person whose LinkedIn profile is being requested.)
        - Output Format: 
        - The response should consist solely of the LinkedIn profile URL.
        - No additional text, explanations, or formatting should precede or follow the URL.

        Example:

        If `Input Variable: 'John Doe'`:

        Correct Output:  
        `https://www.linkedin.com/in/johndoe`

        Incorrect Outputs:
        - 'Here is the LinkedIn profile URL for John Doe: https://www.linkedin.com/in/johndoe'
        - 'https://www.linkedin.com/in/johndoe Please let me know if you need anything else.'
    """

    profile_search_prompt_template = PromptTemplate(
        template=raw_prompt,
        input_variables=["persons_detail"],
    )
    
    agent_tools = [
        Tool(
            name = "Search on Google for the LinkedIn Profile page.",
            func=tavily_crawl_for_linkedIn_url,
            description="Should be used to search on Google for the linkedin profile URL for the person."
        )
    ]
    
    react_prompt = hub.pull('hwchase17/react')
    
    react_agent = create_react_agent(
        llm=model,
        tools=agent_tools,
        prompt=react_prompt
    )
    
    agent_executor = AgentExecutor(
        agent=react_agent,
        tools=agent_tools,
        verbose=True,
    )
    
    response = agent_executor.invoke(
        input={
            "input": profile_search_prompt_template.format_prompt(persons_detail=persons_detail)
        }
    )
    
    profile_url = response["output"]
    
    return profile_url
    
    
if __name__=='__main__':
    name = 'Jayant Nehra'
    persons_detail = f"LinkedIn profile URL for: {name} who works at Fifty Five technologies pvt ltd."
    
    profile_url = profile_url_search(persons_detail)
    print(profile_url)