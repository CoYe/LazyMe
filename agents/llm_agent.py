#!/usr/bin/env python3
"""
Local LLM Agent using Ollama integration
This script provides a command-line interface to interact with a local LLM via Ollama.
"""

import argparse
import json
import sys
import re
from typing import Optional, List, Dict, Any

from gpt_handler.ask_ollama import OllamaHandler
from actions.actions_container import default_registry



class OllamaAgent:
    """An agent that uses Ollama to process tasks and generate responses."""
    
    def __init__(self, 
                 model: str = "llama3",
                 system_prompt: Optional[str] = None,
                 tools: Optional[List[Dict[str, Any]]] = None):
        self.ollama = OllamaHandler(model=model)
        if system_prompt:
            self.ollama.system_prompt = system_prompt
        self.tools = tools or []
        self.conversation_history = []
    
    def add_user_message(self, content: str) -> None:
        """Add a user message to the conversation history."""
        self.conversation_history.append({
            "role": "user",
            "content": content
        })
    
    def add_assistant_message(self, content: str) -> None:
        """Add an assistant message to the conversation history."""
        self.conversation_history.append({
            "role": "assistant",
            "content": content
        })
    
    def add_system_message(self, content: str) -> None:
        """Add a system message to the conversation history."""
        self.conversation_history.append({
            "role": "system",
            "content": content
        })
    
    def reset_conversation(self) -> None:
        """Reset the conversation history."""
        self.conversation_history = []
    
    def process_message(self, user_message: str) -> str:
        """Process a user message and return the agent's response.
        
        Args:
            user_message: The user's input message
            
        Returns:
            The agent's response
        """
        self.add_user_message(user_message)
        
        response = self.ollama.chat(messages=self.conversation_history)
        
        if "error" in response:
            return f"Error: {response['error']}"
        
        assistant_message = response.get("message", {}).get("content", "")
        self.add_assistant_message(assistant_message)
        
        return assistant_message


class ActionEnabledAgent(OllamaAgent):
    """An agent that can perform actions based on LLM responses."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.action_registry = default_registry
        self.enable_actions = True
        
        # Add system message about available actions
        actions_desc = "You can use the following actions:\n"
        for name, desc in self.action_registry.list_actions().items():
            actions_desc += f"- {name}: {desc}\n"
            
        self.add_system_message(
            "You are a helpful assistant with the ability to perform actions. "
            "When appropriate, you can perform actions by using the format: "
            "{{action_name: parameters}}. " 
            f"{actions_desc}\n"
            "Always format action calls in triple backtick code blocks with json format."
        )
    
    def set_enable_actions(self, enable: bool):
        """Enable or disable action execution."""
        self.enable_actions = enable
        
    def process_message(self, user_message: str) -> str:
        """Process a user message, detect and execute actions in the response."""
        # Add the user message to the conversation history
        self.add_user_message(user_message)
        
        # Get the LLM's response
        response = self.ollama.chat(messages=self.conversation_history)
        
        if "error" in response:
            return f"Error: {response['error']}"
        
        assistant_message = response.get("message", {}).get("content", "")
        
        # Process any action calls in the response
        if self.enable_actions:
            assistant_message = self._process_actions(assistant_message)
        
        # Add the processed message to conversation history
        self.add_assistant_message(assistant_message)
        
        return assistant_message
    
    def _process_actions(self, message: str) -> str:
        """Process and execute actions in the message."""
        # Match code blocks that might contain action calls
        code_block_pattern = r"```(?:json)?\s*([\s\S]+?)```"
        
        def process_match(match):
            code_block = match.group(1).strip()
            try:
                # Try to parse as JSON to check if it's an action call
                action_data = json.loads(code_block)
                
                # Check if any key in the data matches an action name
                key = action_data.get("action_type")
                if not key or key not in self.action_registry.list_actions():
                    for key in action_data.keys():
                        if key in self.action_registry.list_actions():
                            break
                
                params = action_data[key]
                
                # Execute the action
                result = self.action_registry.execute_action(key, **params if isinstance(params, dict) else params)
                
                # Format the result
                result_str = json.dumps(result, indent=2)
                return f"```json\n{code_block}\n```\n\nAction result:\n```json\n{result_str}\n```"
                
                # If no action matched, return the original code block
                return match.group(0)
            except json.JSONDecodeError:
                # Not a valid JSON, return the original code block
                return match.group(0)
            except Exception as e:
                # Handle other errors
                return f"{match.group(0)}\n\nError executing action: {str(e)}"
        
        # Replace action calls with action results
        return re.sub(code_block_pattern, process_match, message)


def parse_args():
    parser = argparse.ArgumentParser(description="Local LLM Agent using Ollama")
    parser.add_argument(
        "--model", 
        default="llama3", 
        help="Model to use (default: llama3)"
    )
    parser.add_argument(
        "--system-prompt", 
        default=None,
        help="Custom system prompt to use"
    )
    parser.add_argument(
        "--single-query",
        default=None,
        help="Run a single query and exit"
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List available models and exit"
    )
    parser.add_argument(
        "--disable-actions",
        action="store_true",
        help="Disable executing actions"
    )
    
    return parser.parse_args()


def setup_agent(args) -> ActionEnabledAgent:
    """Set up the Ollama agent with the provided configuration."""
    system_prompt = args.system_prompt
    if not system_prompt:
        system_prompt = (
            "You are a helpful AI assistant. "
            "Answer questions concisely and accurately. "
            "If you don't know something, say so rather than making up information."
        )
    
    agent = ActionEnabledAgent(
        model=args.model,
        system_prompt=system_prompt
    )
    
    if args.disable_actions:
        agent.set_enable_actions(False)
        
    return agent


def list_available_models():
    """List all available models in the Ollama instance."""
    handler = OllamaHandler()
    models = handler.list_models()
    
    if not models:
        print("No models found or couldn't connect to Ollama server.")
        return
    
    print("\nAvailable models:")
    print("-----------------")
    for model in models:
        print(f"• {model['name']}")
        if model.get('size'):
            print(f"  Size: {model['size']}")
        if model.get('modified_at'):
            print(f"  Modified: {model['modified_at']}")
        print()


def interactive_mode(agent: ActionEnabledAgent):
    """Run the agent in interactive mode."""
    print(f"Local LLM Agent (using {agent.ollama.model})")
    print("Type 'exit', 'quit', or Ctrl+C to exit")
    print("Type 'reset' to reset the conversation")
    actions_status = "enabled" if agent.enable_actions else "disabled"
    print(f"System actions are {actions_status}")
    print("-----------------------------------------")
    
    try:
        while True:
            user_input = input("\n> ")
            
            if user_input.lower() in ("exit", "quit"):
                break
            
            if user_input.lower() == "reset":
                agent.reset_conversation()
                print("Conversation reset.")
                continue
            
            if not user_input.strip():
                continue
                
            print("\nThinking...", end="", flush=True)
            response = agent.process_message(user_input)
            # Clear the "Thinking..." text
            print("\r" + " " * 10 + "\r", end="")
            print(f"{response}")
            
    except KeyboardInterrupt:
        print("\nExiting...")


def main():
    args = parse_args()
    
    if args.list_models:
        list_available_models()
        return
        
    # Set up the agent
    try:
        agent = setup_agent(args)
    except Exception as e:
        print(f"Error setting up agent: {str(e)}")
        print("Make sure Ollama is installed and running on your system.")
        print("You can install Ollama from: https://ollama.com/download")
        sys.exit(1)
    
    # Run in single query mode if specified
    if args.single_query:
        response = agent.process_message(args.single_query)
        print(response)
        return
    
    # Otherwise, run in interactive mode
    interactive_mode(agent)


if __name__ == "__main__":
    main()