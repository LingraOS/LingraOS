from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
import requests
import time

app = FastAPI()
agents = {}

class AgentInput(BaseModel):
    name: str
    goal: str

class AgentMessage(BaseModel):
    agent_id: str
    message: str

@app.post("/agents/create")
def create_agent(data: AgentInput):
    agent_id = str(uuid4())
    agents[agent_id] = {
        "name": data.name,
        "goal": data.goal,
        "messages": []
    }
    return {"agent_id": agent_id, "status": "created"}

@app.post("/agents/message")
def handle_message(msg: AgentMessage):
    agent = agents.get(msg.agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    agent["messages"].append({"from": "user", "content": msg.message})

    context = simulate_vector_memory_lookup(msg.message)
    response = fake_model_inference(agent["goal"], msg.message, context)

    agent["messages"].append({"from": "agent", "content": response})
    return {"response": response}

def simulate_vector_memory_lookup(text: str):
    try:
        query = {
            "vector": [0.1] * 10,
            "top_k": 2
        }
        r = requests.post("http://vector-memory-service:8004/vectors/query", json=query)
        if r.ok:
            return r.json()
        return []
    except:
        return []

def fake_model_inference(goal, user_msg, context):
    return f"I received your message: '{user_msg}' with goal: '{goal}' and context: {context}"