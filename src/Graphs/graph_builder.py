from langgraph.graph import StateGraph, START, END

from src.llms.groqLLM import GroqLLM
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
    
    def build_language_graph(self):
        """
        Build a graph for blog generation with inputs topic and language
        """
        self.blog_node_obj=BlogNode(self.llm)
        # Nodes
        self.graph.add_node("title_creation",self.blog_node_obj.title_creation)
        self.graph.add_node('content_generation',self.blog_node_obj.content_generation)
        self.graph.add_node('telugu_translation', lambda state: self.blog_node_obj.translation({**state, 'current_language': 'telugu'}))
        self.graph.add_node('hindi_translation', lambda state: self.blog_node_obj.translation({**state, 'current_language': 'hindi'}))
        self.graph.add_node('route', self.blog_node_obj.route)
        
        # Edges and Conditional Edges
        self.graph.add_edge(START, 'title_creation')
        self.graph.add_edge('title_creation', 'content_generation')
        self.graph.add_edge('content_generation', 'route')
        self.graph.add_conditional_edges('route', self.blog_node_obj.route_decision,{
            'telugu': 'telugu_translation',
            'hindi': 'hindi_translation'
        })
        self.graph.add_edge('telugu_translation', END)
        self.graph.add_edge('hindi_translation', END)
        
        return self.graph
        
    
    def setup_graph(self, usecase):
        if usecase=='topic':
            self.build_topic_graph()
            
        if usecase=='language':
            self.build_language_graph()
            
        return self.graph.compile()
    
# below code is for the langsmith langgraph studio

llm=GroqLLM().get_llm()

graph_builder=GraphBuilder(llm)
graph=graph_builder.build_language_graph().compile()
