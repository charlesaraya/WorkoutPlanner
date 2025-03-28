from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
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

llm = ChatOpenAI(model="gpt-4o-mini")

# Nodes
def input_node(state: PlannerState) -> PlannerState:
    """Processes the input task"""
    if not state["task"]:
        raise ValueError("Please provide a valid task.")

    messages = [SystemMessage(content="""You are a workout planner. Extract the task type and total time in minutes from the user's input. If no time is specified, set total_time to None. Returns a plain JSON string: {"task_type": str, "total_time": int or None}""")]
    messages.append(HumanMessage(content=f"Task: {state['task']}"))

    response = llm.invoke(messages)
    result = json.loads(response.content)

    state["task_type"] = result["task_type"]
    state["total_time"] = result["total_time"]
    return state

def breakdown_node(state: PlannerState) -> PlannerState:
    """Breaks the task into steps"""
    messages = [SystemMessage(content="""You are a workout planner. Given the task type, provide a list of routine steps related to the specific task type. Name each name with one or two keywords. If not workout-related, return None. Returns a plain JSON string (not in markdown or other formatting): {"steps": List[str]}""")]
    messages.append(HumanMessage(content=f"Task type: {state['task_type']}"))

    response = llm.invoke(messages)
    result = json.loads(response.content)

    state["steps"] = result["steps"]
    return state

# Conditional routing functions
def check_time(state: PlannerState) -> Literal["ask_time", "timing"]:
    """Route based on whether total_time is provided"""
    if state["total_time"] is None or state["total_time"] <= 0:
        return "ask_time"
    return "timing"

def ask_time_node(state: PlannerState) -> PlannerState:
    """Asks the user to provide a time if not specified"""
    user_input = input("Can you please provide a workout duration (e.g., '1-hour', '30-minutes'): ")
    state["task"] = f"{state['task']} for {user_input}"

    # Re-extract total_time with updated task
    messages = [SystemMessage(content="""You are a workout planner. Given the task, extract the total time in minutes from the user's input. Returns a plain JSON string (not in markdown or other formatting): {{"total_time": int}}""")]
    messages.append(HumanMessage(content=f"Task: {state["task"]}"))

    response = llm.invoke(messages)
    result = json.loads(response.content)

    state["total_time"] = result["total_time"]
    return state

def timing_node(state: PlannerState) -> PlannerState:
    """Assigns a time for each step in the plan"""
    messages = [SystemMessage(content=f"""You are a workout planner. Given the steps and total time, assign timings that sum exactly to {state['total_time']} minutes. Include warm-up and cool-down if necessary. Returns a plain JSON string (not in markdown or other formatting): {{"steps": List[str], "timings": List[int]}}""")]
    messages.append(HumanMessage(content=f"Steps: {state['steps']}\nTotal time: {state['total_time']} minutes"))

    response = llm.invoke(messages)
    result = json.loads(response.content)

    total_timings = sum(result["timings"])
    if state["total_time"] != total_timings:
        raise ValueError(f"LLM-assigned timings ({total_timings} min) do not match total time ({state['total_time']} min)")

    state["steps"] = result["steps"]
    state["timings"] = result["timings"]
    return state

def output_node(state: PlannerState) -> PlannerState:
    """Formats the final plan"""
    total_time = sum(state["timings"])
    step_times = [f"{step} ({time} min)\n" for step, time in zip(state['steps'], state['timings'])]
    final_plan = f"{state['task']} ({total_time} min):\n* {'* '.join(step_times)}"
    return {'final_plan': final_plan}

# Build Graph
def build_graph():
    # Initialize the StateGraph with the PlannerState schema
    builder = StateGraph(PlannerState)
    # Add nodes
    builder.add_node("input", input_node)
    builder.add_node("breakdown", breakdown_node)
    builder.add_node("ask_time", ask_time_node)
    builder.add_node("timing", timing_node)
    builder.add_node("output", output_node)
    # Connect nodes
    builder.add_edge(START, "input")
    builder.add_edge("input", "breakdown")
    builder.add_conditional_edges("breakdown", check_time, {"ask_time": "ask_time", "timing": "timing"})
    builder.add_conditional_edges("ask_time", check_time, {"ask_time": "ask_time", "timing": "timing"})
    builder.add_edge("timing", "output")
    builder.add_edge("output", END)

    return builder.compile()