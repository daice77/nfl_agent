import os
from agent.fantasy_agent import FantasyFootballAgent

def main():
    agent = FantasyFootballAgent()
    print("Welcome to the Fantasy Football AI Agent!")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("How can I assist you?\n")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break

        response = agent.run(user_input)
        print(f"\n{response}\n")

if __name__ == '__main__':
    main()
