from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from dotenv import load_dotenv
from chatService import ChatService
from model import Message
from responseFormater import format_response
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Get API key from .env file
api_key =os.getenv("MODEL_API_KEY")
if not api_key:
    logger.error("GROQ_API_KEY environment variable is not set")
    raise ValueError("GROQ_API_KEY environment variable is not set")

try:
    chat_service = ChatService(api_key)
    logger.info("Successfully initialized chat service")
except Exception as e:
    logger.error(f"Failed to initialize chat service: {str(e)}")
    raise


# This endpoint to the check running status of code.
@app.route('/health', methods=['GET'])
def health_check():

    try:
        return jsonify({"statusCode":200,"status": "healthy", "model": "Working Fine and Good"}), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({"statusCode":500,"status": "unhealthy", "error": str(e)}), 500
    

#New chat to the Chatbot or chat with chatbot service
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # Validate request
        if not request.is_json:
            logger.warning("Invalid request format: not JSON")
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.json
        if not data or 'message' not in data:
            logger.warning("Invalid request: missing message field")
            return jsonify({"error": "Message is required"}), 400
        
        user_message = data['message']
        conversation_id = data.get('conversation_id', None)
        
        logger.info(f"Received chat request with message: '{user_message[:30]}...' and conversation_id: {conversation_id}")
        
        message = Message(
            content=user_message,
            conversation_id=conversation_id
        )
        response_data = chat_service.process_message(message)
        
        # Format the response
        formatted_response = format_response(response_data)
        
        logger.info(f"Successfully processed message, returning response for conversation {response_data['conversation_id']}")
        return jsonify(formatted_response), 200
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
    

#Get complete history of chats.
@app.route('/api/conversations', methods=['GET'])
def get_conversations():
    try:
        logger.info("Retrieving all conversations")
        conversations = chat_service.get_all_conversations()
        return jsonify({"conversations": conversations}), 200
    except Exception as e:
        logger.error(f"Error retrieving conversations: {str(e)}")
        return jsonify({"error": "Failed to retrieve conversations", "details": str(e)}), 500
    
    
#Get complete history of specfic chats futher we can fetch the user based chats if required.
@app.route('/api/conversations/<conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    try:
        logger.info(f"Retrieving conversation {conversation_id}")
        conversation = chat_service.get_conversation(conversation_id)
        if not conversation:
            logger.warning(f"Conversation {conversation_id} not found")
            return jsonify({"error": "Conversation not found"}), 404
        return jsonify({"conversation": conversation}), 200
    except Exception as e:
        logger.error(f"Error retrieving conversation {conversation_id}: {str(e)}")
        return jsonify({"error": f"Failed to retrieve conversation {conversation_id}", "details": str(e)}), 500

if __name__ == "__main__":
    logger.info("Starting ChatBot Service..")
    app.run(debug=True, host='0.0.0.0', port=5000)