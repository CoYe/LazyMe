# -*- coding: utf-8 -*-


# Example usage




from agents.llm_agent import ActionEnabledAgent


if __name__ == "__main__":
    # Initialize the agent
    agent = ActionEnabledAgent(
        model="qwq",
        system_prompt="You are a Python coding assistant. Help users write efficient code. Your responses shuold be in json format.",
    )
    
    # Process a sample query
    # response = agent.process_message("Write a simple function to calculate the factorial of a number.")
    # print(f"Agent response: {response}")
    
    # # Continue the conversation
    # response = agent.process_message("Can you modify that to handle negative numbers?")
    # print(f"Agent response: {response}")

    response = agent.process_message("Can you create C:\\Users\\Shadow\\Desktop\\text.txt file")
    print(f"Agent response: {response}")