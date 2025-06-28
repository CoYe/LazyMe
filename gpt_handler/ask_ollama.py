# -*- coding: utf-8 -*-
import requests
from attrs import define
from typing import Dict, Any, List, Optional


@define
class OllamaHandler:
    """Handler for interacting with Ollama API for local LLM inference."""
    
    base_url: str = "http://localhost:11434/api"
    model: str = "qwq"  # Default model
    system_prompt: str = "You are a helpful assistant that provides accurate and concise responses."
    
    def __post_init__(self):
        # Verify Ollama is running
        self._check_ollama_status()
    
    def _check_ollama_status(self) -> bool:
        """Checks if Ollama service is running."""
        try:
            response = requests.get(f"{self.base_url}/tags")
            if response.status_code == 200:
                available_models = [model["name"] for model in response.json().get("models", [])]
                print(f"Ollama is running. Available models: {', '.join(available_models)}")
                return True
            else:
                print(f"Ollama returned status code: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("Could not connect to Ollama. Please ensure Ollama is running on localhost:11434")
            return False
    
    def list_models(self) -> List[Dict[str, Any]]:
        """Lists all available models in the Ollama instance."""
        response = requests.get(f"{self.base_url}/tags")
        if response.status_code == 200:
            return response.json().get("models", [])
        else:
            print(f"Failed to list models: {response.status_code}")
            return []
    
    def generate_response(self, prompt: str, model: Optional[str] = None) -> str:
        """Generate a response from the LLM.
        
        Args:
            prompt: The prompt to send to the model
            model: Optional model override
            
        Returns:
            The model's response as a string
        """
        model_to_use = model or self.model
        
        data = {
            "model": model_to_use,
            "prompt": prompt,
            "system": self.system_prompt,
        }
        
        try:
            response = requests.post(f"{self.base_url}/generate", json=data)
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            else:
                print(f"Error generating response: {response.status_code}")
                return f"Error: Failed to get response from Ollama (status code {response.status_code})"
        except Exception as e:
            print(f"Exception during API call: {str(e)}")
            return f"Error: {str(e)}"

    def chat(self, 
             messages: List[Dict[str, str]], 
             model: Optional[str] = None, 
             stream: bool = False) -> Dict[str, Any]:
        """Have a conversation with the LLM using chat format.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            model: Optional model override
            stream: Whether to stream the response
            
        Returns:
            The complete response from the model
        """
        model_to_use = model or self.model
        
        data = {
            "model": model_to_use,
            "messages": messages,
            "stream": stream,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
            }
        }
        
        try:
            response = requests.post(f"{self.base_url}/chat", json=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error in chat: {response.status_code}")
                return {"error": f"Failed to get chat response (status code {response.status_code})"}
        except Exception as e:
            print(f"Exception during chat API call: {str(e)}")
            return {"error": str(e)}

