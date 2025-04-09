import logging
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

def format_response(response_data):
    try:
        formatted_response = {
            "response": response_data["response"],
            "conversation_id": response_data["conversation_id"],
            "timestamp": response_data.get("timestamp", datetime.now().isoformat())
        }
        return formatted_response
    except KeyError as e:
        logger.error(f"Missing key in response data: {str(e)}")
        # Ensure we always return something valid
        return {
            "response": response_data.get("response", "Sorry, an error occurred."),
            "conversation_id": response_data.get("conversation_id", "error"),
            "timestamp": datetime.now().isoformat(),
            "error": f"Missing data: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Error formatting response: {str(e)}")
        return {
            "response": "An error occurred while formatting the response.",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
