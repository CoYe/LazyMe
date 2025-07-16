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
    system_message="""You are a helpful AI assistant who writes code and the user
executes it. Solve tasks using your python coding skills.
In the following cases, suggest python code (in a python coding block) for the
user to execute. When using code, you must indicate the script type in the code block.
You only need to create one working sample.
Do not suggest incomplete code which requires users to modify it.
Don't use a code block if it's not intended to be executed by the user. Don't
include multiple code blocks in one response. Do not ask users to copy and
paste the result. Instead, use 'print' function for the output when relevant.
Check the execution result returned by the user.

If the result indicates there is an error, fix the error.

IMPORTANT: If it has executed successfully, ONLY output 'FINISH'."""
)

user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    human_input_mode="NEVER",
    code_execution_config={"use_docker": False, "work_dir": "coding"},  # Optional: Specify a working directory
    llm_config={"config_list": config_list},
    is_termination_msg=lambda x: "FINISH" in x.get("content", "").rstrip(),  # Define termination message
)

# 4. Initiate the chat
user_proxy.initiate_chat(
    assistant,
    message="Write a Python script that prints 'Hello, world!'. Save it to a file named hello.py and execute it. If the script runs successfully, print the output.",
)