import os
import json
import logging
from datetime import datetime
from threading import Lock

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ConversationRepository:
    def __init__(self, db_file="data/conversations.json"):
        self.db_file = db_file
        self.lock = Lock()  
        
        # Ensure the data directory exists
        os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
        
        # Create the file if it doesn't exist
        if not os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'w') as f:
                    json.dump({}, f)
                logger.info(f"Created new database file at {self.db_file}")
            except Exception as e:
                logger.error(f"Failed to create database file: {str(e)}")
                raise
        
        # Load existing conversations
        try:
            self._load_conversations()
            logger.info("Successfully loaded conversations from database")
        except Exception as e:
            logger.error(f"Failed to load conversations: {str(e)}")
            self.conversations = {}
    
    def _load_conversations(self):
        try:
            with self.lock, open(self.db_file, 'r') as f:
                self.conversations = json.load(f)
        except json.JSONDecodeError:
            logger.warning("Invalid JSON in database file, initializing empty database")
            self.conversations = {}
            self._save_conversations()
    
    def _save_conversations(self):
        try:
            with self.lock, open(self.db_file, 'w') as f:
                json.dump(self.conversations, f, indent=2)
            logger.info("Successfully saved conversations to database")
        except Exception as e:
            logger.error(f"Failed to save conversations: {str(e)}")
            raise
    
    def add_message(self, conversation_id, role, content):
        try:
            self._load_conversations()  
            
            if conversation_id not in self.conversations:
                self.conversations[conversation_id] = []
            
            self.conversations[conversation_id].append({
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat()
            })
            
            self._save_conversations()
            logger.info(f"Added {role} message to conversation {conversation_id}")
            
            return conversation_id
        except Exception as e:
            logger.error(f"Error adding message to conversation {conversation_id}: {str(e)}")
            raise
    
    def get_conversation(self, conversation_id):
        try:
            self._load_conversations()
            return self.conversations.get(conversation_id, [])
        except Exception as e:
            logger.error(f"Error getting conversation {conversation_id}: {str(e)}")
            return []
    
    def get_all_conversations(self):
        try:
            self._load_conversations()  
            
            result = {}
            for conv_id, messages in self.conversations.items():
                result[conv_id] = {
                    "id": conv_id,
                    "messages": messages,
                    "message_count": len(messages),
                    "created_at": messages[0]["timestamp"] if messages else None,
                    "last_updated": messages[-1]["timestamp"] if messages else None
                }
            return result
        except Exception as e:
            logger.error(f"Error getting all conversations: {str(e)}")
            return {}