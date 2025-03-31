from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from agent.agent import Agent

app = FastAPI()
agent = Agent(enable_feedback_node=False)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process")
def process_task(request: Request, task: str = Form(...), thread_id: str = Form(...)):
    """API endpoint to process tasks."""
    response = agent.run(task, thread_id)
    # Check if the request comes from HTMX (via headers)
    if request.headers.get("hx-request"):
        # Return HTML fragment for HTMX to update the page
        return HTMLResponse(content=f"<div id='response'>{response["final_plan"].replace('\n', '<br>')}</div>")
    return response["final_plan"]