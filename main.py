from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI(title="VectorShift Pipeline API")

# Configure CORS - Required for Part 4
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def read_root():
    """Health check endpoint"""
    return {'status': 'healthy', 'message': 'VectorShift Pipeline API is running'}

class Node(BaseModel):
    """Node model matching frontend structure"""
    id: str
    type: str
    position: Dict[str, float]
    data: Dict[str, Any]

class Edge(BaseModel):
    """Edge model matching frontend structure"""
    source: str
    target: str
    id: str

class Pipeline(BaseModel):
    """Pipeline containing nodes and edges"""
    nodes: List[Node]
    edges: List[Edge]

def is_dag(nodes: List[Node], edges: List[Edge]) -> bool:
    """
    Check if the pipeline forms a Directed Acyclic Graph (DAG)
    Uses Kahn's algorithm (topological sort)
    
    Returns:
        bool: True if graph is a DAG, False if it contains cycles
    """
    # Build adjacency list and in-degree count
    adj_list = {node.id: [] for node in nodes}
    in_degree = {node.id: 0 for node in nodes}
    
    # Populate adjacency list and count in-degrees
    for edge in edges:
        adj_list[edge.source].append(edge.target)
        in_degree[edge.target] += 1
    
    # Initialize queue with all nodes that have no incoming edges
    queue = [node_id for node_id, degree in in_degree.items() if degree == 0]
    processed_count = 0
    
    # Process nodes in topological order
    while queue:
        current_node = queue.pop(0)
        processed_count += 1
        
        # For each neighbor, reduce in-degree
        for neighbor in adj_list[current_node]:
            in_degree[neighbor] -= 1
            # If in-degree becomes 0, add to queue
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # If we processed all nodes, it's a DAG (no cycles)
    return processed_count == len(nodes)

@app.post('/pipelines/parse')
def parse_pipeline(pipeline: Pipeline):
    """
    Parse and analyze a pipeline (Part 4 requirement)
    
    Returns:
        dict: Analysis containing num_nodes, num_edges, and is_dag
    """
    num_nodes = len(pipeline.nodes)
    num_edges = len(pipeline.edges)
    is_dag_result = is_dag(pipeline.nodes, pipeline.edges)
    
    return {
        'num_nodes': num_nodes,
        'num_edges': num_edges,
        'is_dag': is_dag_result
    }

@app.get('/pipelines/parse')
def parse_pipeline_get():
    """GET endpoint for testing"""
    return {'message': 'Please use POST method with pipeline data'}

#---------------------------------------------------------------------

# from fastapi import FastAPI, Form

# app = FastAPI()

# @app.get('/')
# def read_root():
#     return {'Ping': 'Pong'}

# @app.get('/pipelines/parse')
# def parse_pipeline(pipeline: str = Form(...)):
#     return {'status': 'parsed'}

#--------------------------------------------------------------------

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get('/')
# def read_root():
#     return {'Ping': 'Pong'}

# class Pipeline(BaseModel):
#     nodes: list
#     edges: list

# @app.post('/pipelines/parse')
# def parse_pipeline(pipeline: Pipeline):
#     return {
#         'num_nodes': len(pipeline.nodes),
#         'num_edges': len(pipeline.edges),
#         'is_dag': True
#     }