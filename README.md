# Chat Bot Service Task

This is a Flask-based REST API service that provides a chat interface powered by a language model. The application allows users to create conversations, send messages, and retrieve conversation history.

## Features

- Create and continue conversations with an AI chat model
- Retrieve full conversation history
- Get details of specific conversations
- Health check endpoint for monitoring service status

## Prerequisites

- Python 3.7+
- Flask
- Flask-CORS
- dotenv
- Groq

## Setup



1. Install the required dependencies:

pip install -r requirements.txt


2. Create a `.env` file in the root directory with the following variables:

MODEL_API_KEY=your_api_key_here  "i have provided my api key temporarily"


## Running the Application

Start the application with:


python app.py


The service will run on `http://0.0.0.0:5000` by default in debug mode.

## API Endpoints

### Health Check

GET /health

Returns the health status of the service.

**Response Example:**

{
  "statusCode": 200,
  "status": "healthy",
  "model": "Working Fine and Good"
}


### Send a Message

POST /api/chat

Send a message to the chat service.

**Request Body:**

{
  "message": "Hello, how can you help me today?",
  "conversation_id": "optional-existing-conversation-id"
}

**Response Example:**

{
  "message": "I'm an AI assistant and I can help you with...",
  "conversation_id": "conversation-id-123",
  "timestamp": "2023-06-15T14:22:33Z"
}


### Get All Conversations

GET /api/conversations

Retrieves a list of all conversations.

**Response Example:**

{
  "conversations": [
    {
      "id": "256272f0-82a8-4e64-a1d0-7e2f5eec3caa",
      "messages": [
        {
          "role": "user",
          "content": "Hello",
          "timestamp": "2023-06-15T14:20:33Z"
        },
        {
          "role": "assistant",
          "content": "Hi there! How can I help you today?",
          "timestamp": "2023-06-15T14:20:35Z"
        }
      ]
    }
  ]
}

### Get Specific Conversation

GET /api/conversations/256272f0-82a8-4e64-a1d0-7e2f5eec3caa

Retrieves details of a specific conversation.

**Response Example:**
{
    "conversation": [
        {
            "content": "Hello, what is 1+1",
            "role": "user",
            "timestamp": "2025-04-09T20:25:01.545881"
        },
        {
            "content": "The answer to 1 + 1 is 2.",
            "role": "assistant",
            "timestamp": "2025-04-09T20:25:01.554143"
        },
        {
            "content": "Hello, what is 1+3",
            "role": "user",
            "timestamp": "2025-04-09T20:25:56.840454"
        },
        {
            "content": "The answer to 1 + 3 is 4.",
            "role": "assistant",
            "timestamp": "2025-04-09T20:25:56.842222"
        },
        {
            "content": "Hello, what is google?",
            "role": "user",
            "timestamp": "2025-04-09T23:08:51.834984"
        },
        {
            "content": "Google can refer to different things, but the most well-known ones are:\n\n1. Google LLC: A multinational technology company specializing in internet-related services and products, including search and online advertising technologies. It's one of the largest and most influential technology companies in the world.\n\n2. Google search: A search engine that allows users to search for information on the internet. It's the most widely used search engine, processing billions of searches every day.\n\n3. Google (the search engine's original name): Initially, Google was a research project called \"Backrub\" developed by Larry Page and Sergey Brin at Stanford University. They later renamed it to Google, which is a playful name inspired by the word \"googol,\" a mathematical term referring to a huge number (1 followed by 100 zeros).",
            "role": "assistant",
            "timestamp": "2025-04-09T23:08:51.838084"
        },
        {
            "content": "write a python code?",
            "role": "user",
            "timestamp": "2025-04-09T23:09:29.604276"
        },
        {
            "content": "Here's a simple example of a Python code that does a few basic things:\n\n```python\n# This is a comment - anything after the '#' symbol is ignored by the computer\n\n# Variable assignment\nname = \"John\"\nage = 30\n\n# Printing variables\nprint(\"My name is\", name)\nprint(\"I am\", age, \"years old\")\n\n# Basic math\nresult = 10 + 5\nprint(\"10 + 5 =\", result)\n\n# Asking for user input\nuser_name = input(\"What is your name? \")\nprint(\"Hello, \" + user_name + \"!\")\n\n# A simple loop\nfor i in range(5):\n    print(i)\n\n# A simple if statement\nif age > 30:\n    print(\"You are older than 30.\")\nelse:\n    print(\"You are 30 or younger.\")\n\n# A simple list\nfruits = [\"apple\", \"banana\", \"cherry\"]\nprint(fruits)\n```\n\nThis code does the following things:\n\n1. Assigns variables for a person's name and age.\n2. Prints out the person's name and age.\n3. Does some basic math and prints out the result.\n4. Asks the user for their name and prints it out.\n5. Prints out the numbers 0-4 using a for loop.\n6. Checks if the person's age is greater than 30 and prints out the result.\n7. Prints out a list of fruits.\n\nYou can save this code to a file with a `.py` extension (for example, `example.py`) and run it using a Python interpreter to see it in action.",
            "role": "assistant",
            "timestamp": "2025-04-09T23:09:29.608143"
        }
    ]
}

## Project Structure

- `app.py` - Main application file with Flask routes
- `chatService.py` - Service for handling chat logic
- `model.py` - Data models
- `responseFormater.py` - Helper to format responses
- `conversationRepository.py` - temp database processer

## Error Handling

The application includes comprehensive error handling with appropriate HTTP status codes and detailed error messages. All errors are logged with timestamps for troubleshooting.

## Environment Variables

- `MODEL_API_KEY` - API key for the language model service

## Logging

The application uses Python's built-in logging module to log information, warnings, and errors with timestamps.
