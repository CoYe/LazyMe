# -*- coding: utf-8 -*-
import autogen
from llm_handler.base_handler import BaseHandler
import autogen
from attrs import define


SYSTEM_MESSAGE = """You are a helpful AI assistant who writes code and the user
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


@define
class OllamaHandler(BaseHandler):
    workdir: str = "coding"  # Optional: Specify a working directory for code execution
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

    def handle_message(self, message: str, system_message: str | None = SYSTEM_MESSAGE) -> object:
        assistant = autogen.AssistantAgent(
        name="Assistant",
        llm_config={"config_list": self.config_list},
        system_message=system_message,  # Use the defined system message
        )

        # user_proxy = autogen.UserProxyAgent(
        #     name="User_proxy",
        #     human_input_mode="NEVER",
        #     code_execution_config={"use_docker": False, "work_dir": self.workdir},  # Optional: Specify a working directory
        #     llm_config={"config_list": self.config_list},
        #     is_termination_msg=lambda x: "FINISH" in x.get("content", "").rstrip(),  # Define termination message
        # )

        # # 4. Initiate the chat
        # response = user_proxy.initiate_chat(
        #     assistant,
        #     message=message,
        # )
        response = assistant.initiate_chat(
            message=message,
            recipient=autogen.ConversableAgent("Ask Ollama", system_message=system_message),  # Use the defined system message
        )
        return response

    def handle_code_message(self, message: str, system_message: str | None = SYSTEM_MESSAGE) -> object:
        assistant = autogen.AssistantAgent(
        name="Assistant",
        llm_config={"config_list": self.config_list},
        system_message=system_message,  # Use the defined system message
        )

        user_proxy = autogen.UserProxyAgent(
            name="User_proxy",
            human_input_mode="NEVER",
            code_execution_config={"use_docker": False, "work_dir": self.workdir},  # Optional: Specify a working directory
            llm_config={"config_list": self.config_list},
            is_termination_msg=lambda x: "FINISH" in x.get("content", "").rstrip(),  # Define termination message
        )

        # 4. Initiate the chat
        response = user_proxy.initiate_chat(
            assistant,
            message=message,
        )
        return response
