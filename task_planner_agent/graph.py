from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langgraph.graph import START, END, StateGraph

from typing import TypedDict, Literal, List

class PlannerState(TypedDict):
    task: str           # e.g., "Plan a 1-hour workout session"
    task_type: str
    total_time: int
    steps: List[str]    # e.g. ['Warp-up', 'Main excercise', 'break', 'Final excercise', 'Cool-down']
    timings: List[int]  # e.g. [10, 20, 5, 20, 5]
    final_plan: str     # e.g., "Final 1-hour workout session: Warm-up for 10 min, Main excercise for 20, ..."

llm = ChatOpenAI(model="gpt-3.5-turbo")

# Nodes
def input_node(state: PlannerState) -> PlannerState:
    """Processes the input task"""
    if not state["task"]:
        raise ValueError("Please provide a valid task.")

    # Prompt to extract task type and total time
    extract_prompt = PromptTemplate(
        input_variables=["task"],
        template="Given the input '{task}', extract the task type, and the total time in minutes (e.g., '60' for 1-hour, '30' for 30-minutes). Return as JSON: {{'task_type': '...', 'total_time': ...}}"
    )
    chain = extract_prompt | llm
    response = chain.invoke({"task": state["task"]})
    result = eval(response.content) # Convert JSON string to dict (ensure LLM returns valid JSON)

    state["task_type"] = result["task_type"]
    state["total_time"] = result["total_time"]
    return state

def breakdown_node(state: PlannerState) -> PlannerState:
    """Breaks the task into steps"""
    breakdown_prompt = PromptTemplate(
        input_variables=["task_type"],
        template="Given the input '{task_type}', provide an extensive list of related workout routine steps (eg: Warm-up, Full-body, Cardio, ...). Return as JSON: {{'steps': List[str]}}"
    )
    chain = breakdown_prompt | llm
    response = chain.invoke({"task_type": state["task_type"], "total_time": state["total_time"]})
    result = eval(response.content)
    return {"steps": result["steps"]}

def timing_node(state: PlannerState) -> PlannerState:
    """Assigns a time for each step in the plan (assume format like "1-hour" for now)"""
    timing_prompt = PromptTemplate(
        input_variables=["total_time", "steps"],
        template="Given the input available, select a sensible subset of '{steps}' that could fit into a workout session of '{total_time}'. Include time to warm-up and coold-down. Return as JSON: {{'steps': List[str], 'timings': List(int)}} where steps is the updated subset of steps."
    )
    chain = timing_prompt | llm
    response = chain.invoke({"total_time": state["total_time"], "steps": state["steps"]})
    result = eval(response.content)

    total_timings = sum(result["timings"]
    if result["total_time"] != total_timings:
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
    builder.add_node("timing", timing_node)
    builder.add_node("output", output_node)
    # Connect nodes
    builder.add_edge(START, "input")
    builder.add_edge("input", "breakdown")
    builder.add_edge("breakdown", "timing")
    builder.add_edge("timing", "output")
    builder.add_edge("output", END)

    return builder.compile()