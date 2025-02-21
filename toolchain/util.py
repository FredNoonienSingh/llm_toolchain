"""utility class """
import json
import pandas as pd

#pylint: disable=E0402
from .common import logger

class Utils:
    """collection of static utility methods"""
    
    @staticmethod
    def create_dataframe_from_responses(responses:list) -> pd.DataFrame:
        """ creates dataframe from list of strings in JSON format

        Args:
            responses (list): llm outputs, strings in JSON format 

        Returns:
            pd.DataFrame: dataframe 
        """
        parsed_data = []
        for response in responses:
            try:
                response = response.strip()
                parsed_data.append(json.loads(response))
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing JSON: {e}, response: {response}")
                continue

        if parsed_data:
            return pd.DataFrame(parsed_data)
        return None

    @staticmethod
    def create_prompt(xml_data:str, txt_data:str) -> str:
        """creates prompt from xml and txt data"""
        return f"""
        TASK: Compare the following two bid descriptions and determine if they are congruent.

        X83 DESCRIPTION:
        {xml_data}

        TXT DESCRIPTION:
        {txt_data}

        INSTRUCTIONS:
        1. Analyze both descriptions carefully.
        2. Determine if the descriptions are essentially the same in terms of the offered service or product.
        3. Respond in JSON format with the following structure:
           {{
             "is_correct": true/false,
             "llm_feedback": "A concise explanation of the comparison result."
           }}
        4. "is_correct" should be true if the bids are congruent and false otherwise.
        5. "llm_feedback" should provide a brief reason for your decision.
        6. Do not include any other text in your response.
        """
