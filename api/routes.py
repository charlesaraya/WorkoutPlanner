from fastapi import FastAPI
from pydantic import BaseModel

from agent.agent import Agent

app = FastAPI()
agent = Agent()

class TaskRequest(BaseModel):
    task: str
    thread_id: str

@app.post("/process")
def process_task(request: TaskRequest):
    """API endpoint to process tasks."""
    response = agent.run(request.task, request.thread_id)
    return {"response": response["final_plan"]}