from src.States.blog_state import BlogPost
from langchain_core.messages import HumanMessage, SystemMessage
from src.States.blog_state import Blog
class BlogNode:
    '''
    A class to represent the blog node
    '''
    def __init__(self, llm):
        self.llm=llm
    def title_creation(self, state: BlogPost):
        """
        Create the title for the blog
        """
        
        if 'topic' in state and state['topic']:
            prompt="""
            You are an SEO blog title generator.

            Generate ONLY ONE blog title.

            Rules:
            - Return exactly one line.
            - No markdown.
            - No explanation.
            - No headings.
            - No table of contents.
            - No blog content.

            Topic:
            {topic}
            """
            system_message=prompt.format(topic=state['topic'])
            response=self.llm.invoke(system_message)
            return {'blog': {'title': response.content.strip()}}
        
    def content_generation(self, state: BlogPost):
        """
        create a content generation for the blog
        """
        
        if 'topic' in state and state['topic']:
            
            prompt="""
            You are expert blog content writer. Use markdown formatting. Generate a detailed blog content with detailed breakdown for the {topic}
            """
            system_message=prompt.format(topic=state['topic'])
            response=self.llm.invoke(system_message)
            return {'blog': {'title': state['blog']['title'], 'content': response.content}}
        
    def translation(self, state: BlogPost):
        """
            Translate the content to the specified language
        """
        
        translation_prompt="""
        Translate the following content into {current_language}.
        - maintain the original tone, style and formatting.
        - Adapt the cultural reference and idioms to be appropriate for {current_language}.
        ORIGIAL CONTENT:
        {blog_content}
        
        """
        blog_content=state['blog']['content']
        message=[
            HumanMessage(translation_prompt.format(current_language=state['current_language'], blog_content=blog_content))
        ]
        translation_content = self.llm.invoke(message)
        return {
            "blog": {
                "title": state["blog"]["title"],
                "content": translation_content.content
            }
        }
        
    def route(self, state: BlogPost):
        return {'current_language': state['current_language']}
    
    def route_decision(self, state: BlogPost):
        """
            Route the content to the respective language
        """
        
        if state['current_language']=='telugu':
            return 'telugu'
        elif state['current_language']=='hindi':
            return 'hindi'
        else:
            return state['current_language']
        
            
            