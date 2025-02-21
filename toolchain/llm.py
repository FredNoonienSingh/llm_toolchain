"""Class containing methods containing  """
import json
import ollama

# pylint: disable=E0402
from .common import logger


class LLM:
    """ 
    wrapper for Ollama methods
    """
    def __init__(self,model:str):
        self.model = model

    def get_response(self,prompt:str,schema:dict=None) -> dict:
        """
        Returns the response from the Ollama model, optionally formatted as JSON
        based on a provided schema.
        Args:
            prompt: The prompt to send to the Ollama model.
            schema: (Optional) A JSON schema to enforce on the response.
        Returns:
            A dictionary containing the Ollama response.
        """
        if schema:
            try:
                response = ollama.generate(
                    model=self.model,
                    prompt=prompt,
                    format="json",
                    options={"json_schema": schema},
                )
                return json.loads(response['response'])

            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON: {e}")
                return {"error": str(e)}
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                return {"error": str(e)}

        else:
            try:
                return ollama.generate(model=self.model, prompt=prompt)
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                return {"error": str(e)}
