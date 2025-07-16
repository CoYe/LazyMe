from attrs import define

from llm_handler.base_handler import BaseHandler

@define
class BaseFlow:
    llm_handler: BaseHandler

    def execute(self, input: str) -> object:
        """        Execute the flow with the given input.   """
        pass