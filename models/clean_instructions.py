from pydantic import BaseModel


class CleanInstructions(BaseModel):
    code_architecture: str
    deployment_steps: str
    development_steps: str
    test_steps: str
    app_name: str
    app_description: str
    app_features: str
    app_requirements: str
    app_technologies: str
    app_ui_design: str
    app_api_integration: str
    app_security: str
    app_performance: str
    app_scalability: str
    app_maintenance: str
    app_documentation: str
    app_user_feedback: str
