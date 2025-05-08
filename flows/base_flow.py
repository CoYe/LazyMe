from attrs import define

from gpt_handler.ask_gpt import GPTHandler


@define
class BaseFlow:
    api: GPTHandler

    def execute(self):
        pass