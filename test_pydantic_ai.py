from pydantic import BaseModel
import asyncio
import logging
import time

from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from llm_handler.ask_ollama import SYSTEM_MESSAGE
from models.clean_instructions import CleanInstructions

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pydantic_ai_debug.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Centralized timeout configuration
MODEL_TIMEOUT_SECONDS = 2300  # per-request timeout used by pydantic-ai HTTP client
OVERALL_TIMEOUT_SECONDS = MODEL_TIMEOUT_SECONDS + 120  # asyncio.wait_for safety buffer


logger.debug("Initializing Ollama model and agent...")

model_setting = ModelSettings(timeout=MODEL_TIMEOUT_SECONDS)

ollama_model = OpenAIModel(
    model_name='devstral:latest', 
    provider=OpenAIProvider(base_url='http://localhost:11434/v1'),
    settings=model_setting,
)

logger.debug(f"Created OpenAI model with base_url: http://localhost:11434/v1")
logger.debug(f"Model name: devstral:latest")
logger.debug(f"Configured timeouts -> model: {MODEL_TIMEOUT_SECONDS}s, overall: {OVERALL_TIMEOUT_SECONDS}s")

agent = Agent(
    ollama_model, 
    output_type=CleanInstructions,
    system_prompt=SYSTEM_MESSAGE
)

logger.debug("Agent created successfully with CleanInstructions output type")

async def run_with_timeout():
    """Run the agent with a timeout for large requests"""
    start_time = time.time()
    
    try:
        logger.info("Starting request to Ollama... This may take a while for large requests.")
        print("Starting request to Ollama... This may take a while for large requests.")
        
        request_text = ("Build me a website, based on python, that will work as Quali Cloudshell replacement based on Quali Torque SaaS API calls. "
            "It should have a Blueprint section where you can create a new blueprint, Sandboxes page where all the Running sandboxes are running. " 
            "It should have a Inventory page where you can see all the available resources. You should be able to create a new one here. Supported types are: Service, Resource, Abstart Resource, Application. " 
            "When you create blueprint, you should be able to add a new Service, Resource, Abstart Resource, Application to it. "
            "Sandbox is a running instance of a Blueprint. You should be able to add all the possible resources to it. "
            "You should be able to start the Sandbox by pressing Reserve button inside the Blueprint page.")
        
        logger.debug(f"Request text length: {len(request_text)} characters")
        logger.debug(f"Timeouts -> model: {MODEL_TIMEOUT_SECONDS}s; overall: {OVERALL_TIMEOUT_SECONDS}s")
        
        result = await asyncio.wait_for(
            agent.run(request_text),
            timeout=OVERALL_TIMEOUT_SECONDS
        )
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        logger.info(f"Request completed successfully in {elapsed_time:.2f} seconds!")
        print(f"Request completed successfully in {elapsed_time:.2f} seconds!")
        
        logger.debug(f"Result type: {type(result)}")
        try:
            logger.debug(f"Result length (str): {len(str(result))} characters")
        except Exception:
            logger.debug("Result length unavailable")
        
        return result
    except asyncio.TimeoutError:
        end_time = time.time()
        elapsed_time = end_time - start_time
        limit_min = OVERALL_TIMEOUT_SECONDS/60
        error_msg = (
            f"Request timed out after {elapsed_time:.2f} seconds (~{limit_min:.0f} minutes limit). "
            "Consider breaking down your request into smaller parts."
        )
        logger.error(error_msg)
        print(error_msg)
        return None
    except Exception as e:
        end_time = time.time()
        elapsed_time = end_time - start_time
        error_msg = f"Error occurred after {elapsed_time:.2f} seconds: {e}"
        logger.error(error_msg)
        logger.exception("Full exception details:")
        print(f"Error occurred: {e}")
        return None

# Run the agent with timeout
if __name__ == "__main__":
    logger.info("=== Starting Pydantic AI Ollama Agent ===")
    logger.debug("Python asyncio event loop starting...")
    
    try:
        result = asyncio.run(run_with_timeout())
        
        if result:
            logger.info("Successfully received result from agent")
            logger.debug(f"Result object: {result}")
            print("\n" + "="*50)
            print("RESULT:")
            print("="*50)
            print(result)
            print("="*50)
        else:
            logger.warning("No result received from agent")
            print("Failed to get response within timeout period")
            
    except Exception as e:
        logger.error(f"Unexpected error in main execution: {e}")
        logger.exception("Full exception details:")
        print(f"Unexpected error: {e}")
    
    logger.info("=== Pydantic AI Ollama Agent Finished ===")
