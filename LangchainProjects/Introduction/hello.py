from pathlib import Path
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from loguru import logger
from ReachOut.third_parties.linkedIn_parser import linkedIn_scrap
from ReachOut.output_parsers.output_parsers import profile_summary_output_parser, reachout_message_output_parser

def retrieve_information(filename: str) -> str:
    filepath = Path(filename)
    
    if filepath.is_file():
        with open(filepath, 'r') as file:
            content = file.read()
        return content
    else:
        logger.error(f"The file {filename} does not exist.")
        raise FileNotFoundError(f"The file {filename} does not exist.")

def LLM_profile_summary(url: str = '', local: bool = True):
    if local:
        file = 'ReachOut/linkedIn_profile_data/JAYANT_NEHRA.json'
        context = retrieve_information(file)
    else:
        # To consume less API Tokens, I have collected the data and stored it on Github Gist. 
        # To use it with different URL unset the mock flag here.
        context = linkedIn_scrap(profile_url=url, mock= True)
            
    summary_template = """
    Given the information in the context which is enclosed in the `CONTEXT` tags, Please create a summary introduction of this person and also provide two interesting facts from the given information:
    [CONTEXT]
    {context}
    [/CONTEXT]
    
        
    Follow this schema for the output
    \n{output_format_instructions}
    
    Please generate the summary and interesting facts about the person:
    """
    
    summary_prompt_template = PromptTemplate(
        input_variables=["context"],
        template=summary_template,
        partial_variables={
            "output_format_instructions": profile_summary_output_parser.get_format_instructions()
        },
    )
    
    model = ChatOpenAI(
        temperature=0.75,
        model='gpt-3.5-turbo',
        )
    
    chain = summary_prompt_template | model | profile_summary_output_parser
    
    try:
        response = chain.invoke(input={"context": context})
        return response
    except Exception as e:
        logger.error(f"An error occurred during the OpenAI call: {e}")


def craft_personalized_reachout_message(profile_summary: str, purpose: str) -> str:
    """
    Crafts a personalized reachout message using the profile summary and the purpose of connecting.
    The LLM is instructed to generate a personalized message using the given context.
    """
    reachout_template = """
    You are an AI assistant tasked with helping to craft a personalized reachout message. 

    Below is the context about the person, enclosed within `CONTEXT` tags. The context includes a summary of the person's profile. 

    Use this context to create a personalized reachout message that includes the following:
    - A greeting with the person's name.
    - A brief compliment or mention of their work based on the profile summary.
    - The purpose of reaching out, which is provided below.
    - A polite closing, expressing a desire for mutual benefit from the connection.

    Purpose of reaching out: {purpose}

    [CONTEXT]
    {profile_summary}
    [/CONTEXT]
        
    Follow this schema for the output
    \n{reachout_message_information}
    
    Please generate the personalized message:
    """

    reachout_prompt_template = PromptTemplate(
        input_variables=["profile_summary", "purpose"],
        template=reachout_template,
        partial_variables={
            "reachout_message_information": reachout_message_output_parser.get_format_instructions()
        }
    )

    model = ChatOpenAI(
        temperature=0.75,
        model='gpt-3.5-turbo',
    )

    chain = reachout_prompt_template | model | reachout_message_output_parser

    try:
        response = chain.invoke(input={
            "profile_summary": profile_summary,
            "purpose": purpose
        })
        return response
    except Exception as e:
        logger.error(f"An error occurred during the OpenAI call: {e}")
        raise

def create_personalized_reachout(url: str, purpose: str, local: bool = True) -> str:
    profile_summary_response = LLM_profile_summary(url=url, local=local)
    profile_summary = profile_summary_response
    print(type(profile_summary))
    reachout_message = craft_personalized_reachout_message(profile_summary, purpose)
    return reachout_message

if __name__=='__main__':
    print("Langchain Version 0.2.6 Experimentation!")
    print(LLM_profile_summary(local=True))