#!/usr/bin/env python3
"""
Multi-Tool AI Agent — Entry point
"""
import argparse
from dotenv import load_dotenv
load_dotenv()

from agent.agent import Agent


def main():
    parser = argparse.ArgumentParser(description="Multi-Tool AI Agent")
    parser.add_argument("--query", "-q", type=str, help="Run a single query and exit")
    args = parser.parse_args()

    agent = Agent()

    if args.query:
        response = agent.run(args.query)
        print(response)
    else:
        print("Multi-Tool AI Agent — type 'exit' to quit\n")
        while True:
            try:
                user_input = input("You: ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ("exit", "quit"):
                    print("Goodbye.")
                    break
                response = agent.run(user_input)
                print(f"Agent: {response}\n")
            except (KeyboardInterrupt, EOFError):
                print("\nGoodbye.")
                break


if __name__ == "__main__":
    main()
