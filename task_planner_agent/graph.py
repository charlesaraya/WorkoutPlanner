from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage, AIMessage
from langgraph.graph import START, END, StateGraph

from typing import TypedDict, Literal, List
import json

class PlannerState(TypedDict):
    task: str           # e.g., "Plan a 1-hour workout session"
    task_type: str
    total_time: int
    steps: List[str]    # e.g. ['Warp-up', 'Main excercise', 'break', 'Final excercise', 'Cool-down']
    timings: List[int]  # e.g. [10, 20, 5, 20, 5]
    final_plan: str     # e.g., "Final 1-hour workout session: Warm-up for 10 min, Main excercise for 20, ..."
    feedback: str       # e.g., "Too much Cardio, reduce it"
    action: str         # e.g., 'accept' | 'adjust_steps' | 'adjust_timings'
    messages: list[AnyMessage]

llm = ChatOpenAI(model="gpt-4o-mini")

# Helper function
def add_feedback_if_any(message, state):
    feedback = state.get("feedback", '')
    if feedback:
        message += f"\nFeedback:{feedback}"
    return message

def add_steps_if_any(message, state):
    steps = state.get("steps", '')
    if steps:
        message += f"\nSteps:{steps}"
    return message

# Nodes
def input_node(state: PlannerState) -> PlannerState:
    """Processes the input task"""
    if not state["task"]:
        raise ValueError("Please provide a valid task.")

    messages = [SystemMessage(content="""You are a workout planner. Extract the task type and total time in minutes from the user's input. If no time is specified, set total_time to None. Returns a plain JSON string: {"task_type": str, "total_time": int or None}""")]
    messages.append(HumanMessage(content=f"Task: {state["task"]}"))

    response = llm.invoke(messages)
    result = json.loads(response.content)

    state["task_type"] = result["task_type"]
    state["total_time"] = result["total_time"]
    return state

def breakdown_node(state: PlannerState) -> PlannerState:
    """Breaks the task into steps"""
    messages = [SystemMessage(content="""You are a workout planner. Given the task type and optional feedback and optional default steps, provide a new list of routine steps related to the specific task type or update the default optional steps based on the feedback feedback. Name each name with one or two keywords. Include warm-up and cool-down steps. If not workout-related, return None. Returns a plain JSON string (not in markdown or other formatting): {"steps": List[str]}""")]
    human_message = add_steps_if_any(add_feedback_if_any(f"Task type: {state["task_type"]}", state), state)
    messages.append(HumanMessage(content=human_message))

    response = llm.invoke(messages)
    result = json.loads(response.content)

    state["steps"] = result["steps"]
    state["feedback"] = '' # Reset feedback
    return state

def ask_time_node(state: PlannerState) -> PlannerState:
    """Asks the user to provide a time if not specified"""
    user_input = input("Can you please provide a workout duration (e.g., '1-hour', '30-minutes'): ")
    state["task"] = f"{state["task"]} for {user_input}"

    # Re-extract total_time with updated task
    messages = [SystemMessage(content="""You are a workout planner. Given the task, extract the total time in minutes from the user's input. Returns a plain JSON string (not in markdown or other formatting): {{"total_time": int}}""")]
    messages.append(HumanMessage(content=f"Task: {state["task"]}"))

    response = llm.invoke(messages)
    result = json.loads(response.content)

    state["total_time"] = result["total_time"]
    return state

def timing_node(state: PlannerState) -> PlannerState:
    """Assigns a time for each step in the plan"""
    messages = [SystemMessage(content=f"""You are a workout planner. Given the suggested steps, total time and optional feedback, assign timings that sum exactly to {state["total_time"]} minutes. Remove steps if you see fit to be realistic with the total session time. Returns a plain JSON string (not in markdown or other formatting): {{"steps": List[str], "timings": List[int]}}""")]
    human_message = f"Steps: {state["steps"]}\nTotal time: {state["total_time"]} minutes"
    human_message_with_feedback = add_feedback_if_any(human_message, state)
    messages.append(HumanMessage(content=human_message_with_feedback))

    response = llm.invoke(messages)
    result = json.loads(response.content)

    state["steps"] = result["steps"]
    state["timings"] = result["timings"]
    return state

def format_node(state: PlannerState) -> PlannerState:
    """Formats the final plan"""
    total_time = sum(state["timings"])
    step_times = [f"{step} ({time} min)\n" for step, time in zip(state["steps"], state["timings"])]
    final_plan = f"{state["task"]} ({total_time} min):\n* {'* '.join(step_times)}"
    return {'final_plan': final_plan}

def feedback_node(state: PlannerState) -> PlannerState:
    """Asks user for feedback"""
    feedback_prompt = "Are you happy with this plan, or would you like to change or add other routines?:"
    print(f"\n{state["final_plan"]}")
    user_feedback = input(feedback_prompt).lower()

    # Use LLM to interpret feedback
    messages = [SystemMessage(content="""You are a task planner. Given the current plan and user feedback, determine the next action. Return plain JSON (no markdown or other formatting): {"feedback": 'str', "action": 'accept' | 'adjust_steps' | 'adjust_timings'}""")]
    messages.append(HumanMessage(content=f"Current Plan: {state["final_plan"]}\nUser Feedback: {user_feedback}"))

    response = llm.invoke(messages)
    result = json.loads(response.content)

    state["feedback"] = result["feedback"]
    state["action"] = result["action"]
    return state

# Conditional routing functions
def check_time(state: PlannerState) -> Literal["ask_time", "timing"]:
    """Route based on whether total_time is provided"""
    if state["total_time"] is None or state["total_time"] <= 0:
        return "ask_time"
    return "timing"

def check_timing(state: PlannerState) -> Literal["timing", "format"]:
    """Route based on whether timings match the expected total time of the task"""
    if state["total_time"] != sum(state["timings"]):
        return "timing"
    return "format"

def check_feedback(state: PlannerState) -> Literal["ask_time", "timing", "END"]:
    action = state.get("action", "accept") # fallback if action is missing
    if action == 'accept':
        return END
    elif action == 'adjust_steps':
        return "breakdown"
    elif action == 'adjust_timings':
        return "timing"
    return END # fallback

# Build Graph
def build_graph():
    # Initialize the StateGraph with the PlannerState schema
    builder = StateGraph(PlannerState)
    # Add nodes
    builder.add_node("input", input_node)
    builder.add_node("breakdown", breakdown_node)
    builder.add_node("ask_time", ask_time_node)
    builder.add_node("timing", timing_node)
    builder.add_node("format", format_node)
    builder.add_node("feedback_node", feedback_node)
    # Connect nodes
    builder.add_edge(START, "input")
    builder.add_edge("input", "breakdown")
    builder.add_conditional_edges("breakdown", check_time, {"ask_time": "ask_time", "timing": "timing"})
    builder.add_conditional_edges("ask_time", check_time, {"ask_time": "ask_time", "timing": "timing"})
    builder.add_conditional_edges("timing", check_timing, {"timing": "timing", "format": "format"})
    builder.add_edge("format", "feedback_node")
    builder.add_conditional_edges("feedback_node", check_feedback, {"breakdown": "breakdown", "timing": "timing", END: END})

    return builder.compile()