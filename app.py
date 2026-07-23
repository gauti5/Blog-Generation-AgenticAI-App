
import uvicorn
from fastapi import FastAPI, Request

from src.Graphs.graph_builder import GraphBuilder
from src.llms.groqLLM import GroqLLM
from src.Nodes.blog_node import BlogNode
from src.States.blog_state import BlogPost

import os
from dotenv import load_dotenv
load_dotenv()

app=FastAPI()

os.environ['LANGSMITH_API_KEY']=os.getenv('LANGSMITH_API_KEY')

@app.post('/blogs')
async def create_blogs(request: Request):
    data=await request.json()
    topic=data.get('topic', '')
    
    # get llm object
    groqLLM=GroqLLM()
    llm=groqLLM.get_llm()
    
    # get the graph
    graph_builder=GraphBuilder(llm=llm)
    if topic:
        graph=graph_builder.setup_graph(usecase='topic')
        state=graph.invoke({'topic': topic})
        
    return {'data': state}

if __name__=='__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8000, reload=True)
        
        
