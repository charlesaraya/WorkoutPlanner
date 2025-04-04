import argparse

from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

from thread_manager import ThreadDB
from agent.agent import Agent

def main():
    STOP_SESSION = False
    parser = argparse.ArgumentParser(description="Process command-line arguments.")
    parser.add_argument("--thread", type=int, help="Session identifier", required=False)
    parser.add_argument("--db", type=str, help="DB identifier", required=False)
    args = parser.parse_args()

    thread_db = ThreadDB()
    thread_id = thread_db.add(args.thread) if args.thread else thread_db.add()

    db = args.db if args.db else "db/checkpoints.sqlite"

    agent = Agent(db)

    while(not STOP_SESSION):
        # Get user input
        user_input = input("Enter a task to plan (e.g., 'Plan a 1-hour workout session') : ")
        try:
            result = agent.run(user_input, thread_id)
        except Exception as e:
            print(f"Error: {e}")

        print("\nYour Plan:\n",result["final_plan"])

        continue_session = input("\n* To continue your session, press [Enter]" +
                                "\n* To start a new session, type 'new'" +
                                "\n* To quit, type 'quit'\n" +
                                ">>> ")
        if continue_session == '':
            continue
        elif continue_session == 'new':
            thread_id = thread_db.add()
        elif continue_session == 'quit':
            STOP_SESSION = True

if __name__ == "__main__":
    main()