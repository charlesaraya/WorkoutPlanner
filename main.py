import argparse

from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

from thread_manager import ThreadDB
from agent import Agent

agent = Agent()

def main():
    STOP_SESSION = False
    parser = argparse.ArgumentParser(description="Process command-line arguments.")
    parser.add_argument("--thread", type=int, help="Session identifier", required=False)
    args = parser.parse_args()

    thread_db = ThreadDB()
    thread_id = thread_db.add(args.thread) if args.thread else thread_db.add()

    while(not STOP_SESSION):
        # Get user input
        user_input = input("Enter a task to plan (e.g., 'Plan a 1-hour workout session') : ")
        try:
            config = {"configurable": {"thread_id": thread_id}}
            result = agent.run({'task': user_input}, config)
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

        print("\nYour Plan:")
        print(result["final_plan"])

        continue_session = input("\n* To continue your session, press [Enter]" +
                                "\n* To start a new session, type 'new'" +
                                "\n* To quit, type 'quit'")
        if continue_session == '':
            continue
        elif continue_session == 'new':
            thread_id = thread_db.add()
        elif continue_session == 'quit':
            STOP_SESSION = True

if __name__ == "__main__":
    main()