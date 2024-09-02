from langchain_community.tools.tavily_search import TavilySearchResults

def tavily_crawl_for_linkedIn_url(name: str) -> str:
    """This tools is used to search for any person's LinkedIn profile. And this returns the Profile URL for the person."""
    
    search = TavilySearchResults()
    response = search.run(f"{name}")
    return response[0]["url"]

if __name__=='__main__':
    name = 'Jayant Nehra'
    query = f"LinkedIn profile URL for: {name} who works at Fifty Five technologies pvt ltd."
    print(tavily_crawl_for_linkedIn_url(query))
    