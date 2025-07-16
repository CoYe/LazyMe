from flows.define_app import DefineAppFlow
from flows.define_app_arch import DefineAppArchFlow
from flows.define_deployment_steps import DefineAppDeployFlow
from flows.define_steps import DefineAppDevStepsFlow
from flows.define_test_steps import DefineAppDevTestStepsFlow
from llm_handler.ask_gpt import GPTHandler
from llm_handler.ask_ollama import OllamaHandler


class BUILDer:
    def __init__(self):
        self.__api = GPTHandler()

    def build(self, input: str):
        llm_handler = OllamaHandler()
        define_app_flow = DefineAppFlow(llm_handler)
        define_app_arch_flow = DefineAppArchFlow(llm_handler)
        define_app_deploy_flow = DefineAppDeployFlow(llm_handler)
        define_app_dev_steps_flow = DefineAppDevStepsFlow(llm_handler)
        define_app_dev_test_steps_flow = DefineAppDevTestStepsFlow(llm_handler)
        clarified_instructions = define_app_flow.execute(input)
        app_arch = define_app_arch_flow.execute(clarified_instructions)
        app_dev_steps = define_app_deploy_flow.execute(app_arch, clarified_instructions)
        for step in app_dev_steps:
            step.execute()

        app_dev_test_steps = define_app_dev_test_steps_flow.execute()
        for step in app_dev_test_steps:
            step.execute()

        define_app_deploy_flow.execute(app_arch)


if __name__ == "__main__":
    Builder = BUILDer()
    # How many word build can we use in a single place...
    Builder.build(input="Build me a website, based on python, that will work as Quali Cloudshell replacement based on Quali Torque SaaS API calls. "
    "It should have a Blueprint section where you can create a new blueprint, Sandboxes page where all the Running sandboxes are running. " 
    "It should have a Inventory page where you can see all the available resources. You should be able to create a new one here. Supported types are: Service, Resource, Abstart Resource, Application. " 
    "When you create blueprint, you should be able to add a new Service, Resource, Abstart Resource, Application to it. "
    "Sandbox is a running instance of a Blueprint. You should be able to add all the possible resources to it. "
    "You should be able to start the Sandbox by pressing Reserve button inside the Blueprint page.")
