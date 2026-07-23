from langgraph.graph import StateGraph, START, END

from src.llms.groqLLM import ChatGroq
from src.States.blog_state import BlogPost
from src.Nodes.blog_node import BlogNode

class GraphBuilder:
    def __init__(self, llm):
        self.llm=llm
        self.graph=StateGraph(BlogPost)
        
    def build_topic_graph(self):
        """
        Build a graph to generate blogs based on topic
        """
        self.blog_node_obj=BlogNode(self.llm)
        # Nodes
        self.graph.add_node("title_creation",self.blog_node_obj.title_creation)
        self.graph.add_node('content_generation',self.blog_node_obj.content_generation)
        
        # Edges
        self.graph.add_edge(START, 'title_creation')
        self.graph.add_edge('title_creation', 'content_generation')
        self.graph.add_edge('content_generation', END)
        
        return self.graph
    
    def setup_graph(self, usecase):
        if usecase=='topic':
            self.build_topic_graph()
            
        return self.graph.compile()