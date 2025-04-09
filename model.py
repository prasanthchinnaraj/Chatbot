import uuid
from datetime import datetime

class Message:
    def __init__(self, content, role="user", conversation_id=None):
        self.id = str(uuid.uuid4())
        self.content = content
        self.role = role
        self.conversation_id = conversation_id
        self.timestamp = datetime.now().isoformat()