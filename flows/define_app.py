from flows.base_flow import BaseFlow

SYSTEM_MESSAGE = """You are a helpful AI assistant who helps clients to define architecture and structural components of the software application.
You will use best practices in software design and architecture. 
You will only ask questions that are necessary to understand the requirements. 
Please respond in JSON format.

IMPORTANT: once complete, ONLY output 'FINISH'."""


class DefineAppFlow(BaseFlow):

    def execute(self, input: str):
        """
        Execute the flow to define the application.
        This method should be implemented to handle the specific logic for defining the app.
        """
        # Placeholder for actual implementation
        print(f"Defining application with input: {input}")
        # Here you would typically call the LLM API to get the app definition

        response = self.llm_handler.handle_message(
            message=f"Please ask me as less questions as possible regarding this input to build a new app or edit existing feature: {input}",
            system_message=SYSTEM_MESSAGE
        )
        answers = ""
        return response
