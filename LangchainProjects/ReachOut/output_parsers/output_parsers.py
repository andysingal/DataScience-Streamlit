from typing import Dict, List, Any
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

class Summary(BaseModel):
    summary: str = Field(description="summary")
    facts: List[str] = Field(description="interesting facts about the person")
    
    def dict_parser(self) -> Dict[str, Any]:
        return {
            "summary": self.summary,
            "facts": self.facts,
        }
        
        
profile_summary_output_parser = PydanticOutputParser(pydantic_object=Summary)

class reachoutMessage(BaseModel):
    subject: str = Field(description="subject line decribing the purpose briefly.")
    message: str = Field(description="message draft that we can send to the person.")
    
    def dict_parser(self) -> Dict[str, Any]:
        return {
            "subject": self.subject,
            "message": self.message,
        }

reachout_message_output_parser = PydanticOutputParser(pydantic_object=reachoutMessage)
