# main.py

import logging
import uuid

from agent.fantasy_agent import FantasyFootballAgent
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    agent = FantasyFootballAgent()
    thread_id = uuid.uuid4().hex  # Generate a unique session ID

    logger.info(f"Starting new session with thread_id: {thread_id}")

    print("Welcome to the Fantasy Football AI Agent!")
    print(
        "Type 'exit' to quit, 'help' for assistance, or 'reset' to start a new conversation.\n"
    )

    try:
        while True:
            user_input = input("How can I assist you?\n").strip().lower()

            if user_input in ["exit", "quit"]:
                print("Thank you for using the Fantasy Football AI Agent. Goodbye!")
                break

            elif user_input == "help":
                print("\nAvailable commands:")
                print("- 'exit' or 'quit': End the session")
                print("- 'reset': Start a new conversation")
                print("- 'help': Show this help message")
                print(
                    "You can ask about player stats, news, trade evaluations, or waiver wire recommendations.\n"
                )
                continue

            elif user_input == "reset":
                thread_id = uuid.uuid4().hex
                logger.info(f"Resetting conversation. New thread_id: {thread_id}")
                print("\nStarting a new conversation.\n")
                continue

            try:
                logger.info(f"User input: {user_input}")
                response = agent.run(
                    user_input, thread_id=thread_id, user_info="user123"
                )
                print(f"\nAssistant: {response}\n")
                logger.info(f"Assistant response: {response}")
            except Exception as e:
                logger.error(f"Error processing user input: {str(e)}")
                print(
                    "\nI apologize, but I encountered an error while processing your request. Please try again or rephrase your question.\n"
                )

    except KeyboardInterrupt:
        print("\nSession terminated by user. Goodbye!")
    except Exception as e:
        logger.critical(f"Critical error in main loop: {str(e)}")
        print(
            "\nAn unexpected error occurred. The session has been terminated. We apologize for the inconvenience."
        )
    finally:
        logger.info(f"Ending session with thread_id: {thread_id}")


if __name__ == "__main__":
    main()
