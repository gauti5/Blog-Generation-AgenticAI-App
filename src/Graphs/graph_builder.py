from langgraph.graph import StateGraph, START, END

from src.llms.groqLLM import ChatGroq
from src.States.blog_state import BlogPost

class GraphBuilder:
    def __init__(self, llm):
        self.llm=llm
        self.graph=StateGraph(BlogPost)
        
    def build_topic_graph(self):
        """
        Build a graph to generate blogs based on topic
        """
        
        # Nodes
        self.graph.add_node("title_creation",)
        self.graph.add_node('content_generation',)
        
        # Edges
        self.graph.add_edge(START, 'title_creation')
        self.graph.add_edge('title_creation', 'content_generation')
        self.graph.add_edge('content_generation', END)
        
        return self.graph