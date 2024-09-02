"""
    This is the main entrypoint for the `reachout` agent. The idea is to use the Langchain agents to parse the profile details and then use those details and your objectives to craft a personal reachout message for that person.
"""

from Introduction.hello import create_personalized_reachout
from ReachOut.agents.profile_search_agent import profile_url_search
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

def reachOut_person(name: str, purpose: str) -> dict:
    """This returns the LinkedIn URL for the person and generates a reachout message."""
    persons_detail = f"LinkedIn profile URL of: {name}. This person works at Fifty Five technologies pvt ltd."
    profile_url = profile_url_search(persons_detail)
    response = create_personalized_reachout(url=profile_url, local=True, purpose=purpose)

    subject = response.subject
    message = response.message

    return {"subject": subject, "message": message}

if __name__ == '__main__':
    
    name = 'Jayant Nehra'
    purpose = "I am a newly graduated student who is interested in the Data Engineering field. I saw an opportunity in his organization and would love to reach out to him and find out if he can refer me to an open Intern Position for the data engineer role."
    
    result = reachOut_person(name, purpose)
    
    pprint(result, indent=4)
