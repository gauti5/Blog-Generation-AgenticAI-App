from typing import TypedDict

from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

class Blog(BaseModel):
    title: str=Field(description="The title of the blog post")
    content: str=Field(description="The main content of the blog post")
    
class BlogPost(TypedDict):
    topic: str
    blog: Blog
    current_language: str
    