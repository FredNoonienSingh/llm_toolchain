"""common things in the toolchain """
from loguru import logger

logger.add("logs/logs.log", level="INFO", format="{time} {level} {message}")

schema: dict = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "results": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "position_id": { "type": "string", "description": "ID of the position from the XML." },
          "is_correct": { "type": "boolean", "description": "True if the offer is correct, false otherwise." },
          "llm_feedback": { "type": "string", "description": "Concise feedback from the LLM about the offer." }
        },
        "required": ["position_id", "is_correct", "llm_feedback"]
      }
    }
  },
  "required": ["results"]
}