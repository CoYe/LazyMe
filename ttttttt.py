import autogen


config_list = [
    {
        # Let's choose the Meta's Llama 3.1 model (model names must match Ollama exactly)
        "model": "gemma3:27b-it-qat",
        # We specify the API Type as 'ollama' so it uses the Ollama client class
        "api_type": "ollama",
        "stream": False,
        "client_host": "http://localhost:11434",
        # "use_docker": False,  # Use Docker for Ollama
    }
]

assistant = autogen.AssistantAgent(
    name="Assistant",
    llm_config={"config_list": config_list},
    system_message="You are a helpful AI assistant that generates Python code."
)

user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    human_input_mode="NEVER",
    code_execution_config={"use_docker": False, "work_dir": "coding"},  # Optional: Specify a working directory
    llm_config={"config_list": config_list},
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", "").rstrip(),  # Define termination message
)

# 4. Initiate the chat
user_proxy.initiate_chat(
    assistant,
    message="Write a Python script that prints 'Hello, world!'. Save it to a file named hello.py and execute it. If the script runs successfully, print the output.",
)