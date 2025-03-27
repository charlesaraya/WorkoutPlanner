from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

from graph import build_graph

def main():
    # Get user input
    user_input = input("Enter a task to plan (e.g., 'Plan a 1-hour workout session'): ")
    graph = build_graph()

    result = graph.invoke({'task': user_input})

    print("\nYour Plan:")
    print(result["final_plan"])

if __name__ == "__main__":
    main()