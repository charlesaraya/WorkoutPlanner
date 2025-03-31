# Workout Planner Agent
The Workout Planner Agent, a little project built with LangGraph that helps users plan an actionable workout session. In a nutshell, based on the time a user wants to put in their workout, it breaks a session into different routines and their timeline. Whether you’re planning a short at-home workout, a chill yoga session, or a hardcore body-building grind, this agent should got you covered. It's my playground for mastering LangGraph workflows, and God knows where where the journey will take me.

## Feats
The agent is a solid foundation with LangGraph, LLM integration, and conditional workflows:
* **LLM-Powered**: Leverages `GPT-3.5-turbo` for intelligent task breakdown and timing.
* **Dynamic Steps**: The LLM crafts steps based on your task—workouts get cardio, yoga gets poses, and random tasks get a sensible default.
* **Conditional Flow**: Prompts for missing durations and adjusts timings if they don’t align with the total.
* **FastAPI Support**: Offers a RESTful API endpoint for task processing alongside the CLI.
* **Web Interface**: Features a Jinja2-templated home page with HTMX for dynamic task submission and plan display. The feedback loop is disabled.
* **Persistance with SQLite**: The agent uses `SqliteSaver` to pick up right where the user left it.

## Workflow
* **Input**: You throw in a task (e.g., "Plan a 1-hour workout session"), and the agent uses the LLM to extract the task type (e.g. "workout", "yoga session", "boxing", etc.) and total time (60 minutes).
* **Task Breakdown**: The LLM crafts a list of steps tailored to your task, like "Warm-up", "Cardio", and "Bodyweight Squats" and so on for a regular workout session.
* **Timings**: The agent assigns timings to each step, making sure they sum up to your total time.
* **Formatting**: You get a clean, formatted plan, like "Warm-up (10 min), Cardio (40 min), Cool-down (10 min)."
* **Feedback Mechinism**: Tell the agent to adjust the plan to your taste (e.g., "Too much Cardio" or "Add stretching"). The LLM figures out if it needs to tweat steps in the plan or fix the timing, looping back to adjust the plan.

### Setup
Clone this repo:
```
git clone https://github.com/charlesaraya/ai-app-playground.git
cd ai-app-playground
```
Install dependencies:
```
pip install -r requirements.txt
```
Set your API key `.env`:
```
export OPENAI_API_KEY="your-key-here"
```

### Run It

#### CLI mode
Fire it up with:
```
python main.py --thread session_1
```

#### API Mode
Spin up the FastAPI server:
```
uvicorn api.routes:app --host 127.0.0.1 --port 8000 --reload
```

Hit the endpoint at http://localhost:8000/process:
```
curl -X POST "http://localhost:8000/process" \
     -H "Content-Type: application/json" \
     -d '{"task": "Plan a 1-hour workout session", "thread_id": "session_1"}'
```

Get a response like:
```
{"response": "Plan a 1-hour workout session (60 min, created 2025-03-30 14:35:00):\n* Warm-up (10 min)* Cardio (40 min)* Cool-down (10 min)"}
```

#### Example Input

* Try "Plan a 1-hour workout session" or "Plan a workout like last time, but 30 minutes."
* Hit `[Enter]` to keep going, `new` for a fresh session, or `quit` to bail.

#### Example Output
```
Plan a 1-hour workout session (60 min):
* Warm-up (10 min)
* Cardio (20 min)
* Strength (20 min)
* Cool-down (10 min)
```