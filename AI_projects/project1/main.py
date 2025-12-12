from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_agent as create_react_agent
from dotenv import load_dotenv

load_dotenv()

@tool
def calculator(a: float, b: float) -> str:
    """Performs a simple addition of two numbers."""
    print("Tool has been called with:", a, b)
    return str(a + b)

@tool
def say_hello(name: str) -> str:
    """Returns a greeting message."""
    print("Tool has been called with:", name)
    return f"Hello, {name}!"

def main():
    model = ChatOpenAI(temperature=0) # Could add a model here and use zero temperature for deterministic responses

    tools = [calculator]
    agent_executor = create_react_agent(model, tools)

    print("Welcome! I'm your AI assistant. Type 'quit' to exit.")
    print("You can ask me to perform calculations or chat with me.")

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break

        print("\nAssistant: ", end="")
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="", flush=True)
        print()  # For a new line after the response

if __name__ == "__main__":
    main()
