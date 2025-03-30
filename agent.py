from typing import Dict
import json

from graph import build_graph

class Agent:
    def __init__(self):
        self.__graph = build_graph()

    def run(self, task: str, thread_id: str):
        config = {"configurable": {"thread_id": thread_id}}
        result = self.__graph.invoke({'task': task}, config)
        return result["final_plan"]
