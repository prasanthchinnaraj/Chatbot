import uuid
import logging
from groq import Groq
from conversationRepository import ConversationRepository



# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self, api_key):
        try:
            self.client = Groq(api_key=api_key)
            self.model = "llama-3.1-8b-instant"
            self.repository = ConversationRepository("data/conversations.json")
            logger.info("Chat service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize chat service: {str(e)}")
            raise
    
    def process_message(self, message):
        try:
            if not message.conversation_id:
                message.conversation_id = str(uuid.uuid4())
                logger.info(f"Created new conversation with ID: {message.conversation_id}")
            else:
                logger.info(f"Using existing conversation with ID: {message.conversation_id}")
            
            # Retrieve conversation history
            history = self.repository.get_conversation(message.conversation_id)
            
            # Prepare messages for the model
            formatted_history = self._format_history(history)
            
            # Add user message to formatted history
            formatted_history.append({"role": "user", "content": message.content})
            
            # Call Groq API
            try:
                logger.info(f"Sending request to Groq API with model: {self.model}")
                response = self.client.chat.completions.create(
                    messages=formatted_history,
                    model=self.model,
                    temperature=0.7,
                    max_tokens=1024
                )
                
                # Extract response text
                assistant_message = response.choices[0].message.content
                logger.info("Successfully received response from Groq API")
                
            except Exception as e:
                logger.error(f"Groq API error: {str(e)}")
                assistant_message = "I'm sorry, I encountered an issue while processing your request. Please try again later."
                
            # Store the conversation
            self.repository.add_message(message.conversation_id, "user", message.content)
            self.repository.add_message(message.conversation_id, "assistant", assistant_message)
            
            return {
                "response": assistant_message,
                "conversation_id": message.conversation_id,
                "model": self.model
            }
            
        except Exception as e:
            logger.error(f"Error in process_message: {str(e)}")
            raise
    
    def _format_history(self, history):
        try:
            formatted_history = []
            for msg in history:
                formatted_history.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            return formatted_history
        except Exception as e:
            logger.error(f"Error formatting history: {str(e)}")
            # Return empty history if there's an error
            return []
    
    def get_all_conversations(self):
        try:
            return self.repository.get_all_conversations()
        except Exception as e:
            logger.error(f"Error getting all conversations: {str(e)}")
            raise
    
    def get_conversation(self, conversation_id):
        try:
            return self.repository.get_conversation(conversation_id)
        except Exception as e:
            logger.error(f"Error getting conversation {conversation_id}: {str(e)}")
            raise