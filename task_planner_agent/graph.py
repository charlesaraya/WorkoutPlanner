from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_openai import ChatOpenAI

from langgraph.graph import START, END, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode

from typing import TypedDict, Literal, List

class PlannerState(TypedDict):
    task: str           # e.g., "Plan a 1-hour workout session"
    steps: List[str]    # e.g. ['Warp-up', 'Main excercise', 'break', 'Final excercise', 'Cool-down']
    timings: List[int]  # e.g. [10, 20, 5, 20, 5]
    final_plan: str     # e.g., "Final 1-hour workout session: Warm-up for 10 min, Main excercise for 20, ..."

# Nodes
def input_node(state: PlannerState) -> PlannerState:
    """Processes the input task"""
    return {'task': state['task']}

def breakdown_node(state: PlannerState) -> PlannerState:
    """Breaks the task into steps"""
    steps = ['Warm-up', 'Excercise', 'Cool-down']
    return {'steps': steps}

def timing_node(state: PlannerState) -> PlannerState:
    """Assigns a time for each step in the plan (assume format like "1-hour" for now)"""
    task = state['task'].lower()
    total_time = 60  # Default to 60 minutes if "hour" is mentioned
    if 'hour' not in task:
        total_time = 30   # Fallback for unspecified time
    total_steps = len(state['steps'])
    time_per_step = total_time // total_steps
    timings = [time_per_step] * total_steps
    return {'timings': timings}

def output_node(state: PlannerState):
    """Formats the final plan"""
    step_times = [f"{step} ({time})" for step, time in zip(state['steps'], state['timings'])]
    final_plan = f"{state['task']}: {', '.join(step_times)}"
    return {'final_plan': final_plan}

# Build Graph
def build_graph():
    # Initialize the StateGraph with the PlannerState schema
    builder = StateGraph(PlannerState)
    # Add nodes
    builder.add_node("input", input_node)
    builder.add_node("breakdown", breakdown_node)
    builder.add_node("timing", timing_node)
    builder.add_node("output", output_node)
    # Connect nodes
    builder.add_edge(START, "input")
    builder.add_edge("input", "breakdown")
    builder.add_edge("breakdown", "timing")
    builder.add_edge("timing", "output")
    builder.add_edge("output", END)

    return builder.compile()