from flows.define_app import DefineAppFlow
from flows.define_app_arch import DefineAppArchFlow
from flows.define_deployment_steps import DefineAppDeployFlow
from flows.define_steps import DefineAppDevStepsFlow
from flows.define_test_steps import DefineAppDevTestStepsFlow
from gpt_handler.ask_gpt import GPTHandler


class BUILDer:
    def __init__(self):
        self.__api = GPTHandler()

    def build(self, input):
        define_app_flow = DefineAppFlow(self.__api)
        define_app_arch_flow = DefineAppArchFlow(self.__api)
        define_app_deploy_flow = DefineAppDeployFlow(self.__api)
        define_app_dev_steps_flow = DefineAppDevStepsFlow(self.__api)
        define_app_dev_test_steps_flow = DefineAppDevTestStepsFlow(self.__api)
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
    Builder.build()
