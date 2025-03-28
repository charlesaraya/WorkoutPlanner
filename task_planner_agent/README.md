# Workout Planner Agent
The Workout Planner Agent, a little project built with LangGraph that helps users plan an actionable workout session. In a nutshell, based on the time a user wants to put in their workout, it breaks a session into different routines and their timeline. Whether you’re planning a short at-home workout, a chill yoga session, or a hardcore body-building grind, this agent should got you covered. It's my playground for mastering LangGraph workflows, and God knows where where the journey will take me.

## Feats
The agent is a solid foundation with LangGraph, LLM integration, and conditional workflows:
* **LLM-Powered**: Leverages `GPT-3.5-turbo` for intelligent task breakdown and timing.
* **Dynamic Steps**: The LLM crafts steps based on your task—workouts get cardio, yoga gets poses, and random tasks get a sensible default.
* **Conditional Flow**: Missed the workout time? Are suggested timings wrong? It loops back to ask you.
* **Error Handling**: Catches bad inputs and keeps you in the loop with clear feedback.

### Setup
Clone this repo:
```
git clone https://github.com/yourusername/task-planner-agent.git
cd task-planner-agent
```
Install dependencies:
```
pip install -r requirements.txt
```
Set your API key:
```
export OPENAI_API_KEY="your-key-here"
```

### Run It
Fire it up with:
```
python main.py
```

Try inputs like:

* "Plan a 1-hour workout session"
* "Plan a 30-minute yoga session"
* "Plan a study session" (it’ll ask for a time)

Example Output:
<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

```
Plan a 1-hour workout session (60 min):
* Warm-up (10 min)
* Cardio (20 min)
* Strength (20 min)
* Cool-down (10 min)
```