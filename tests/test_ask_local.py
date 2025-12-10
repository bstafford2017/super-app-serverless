import json
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'handlers'))

from ask import handler

event = {
    'body': json.dumps({
        'prompt': 'What is the capital of France?'
    })
}

response = handler(event, None)
print(json.dumps(json.loads(response['body']), indent=2))

# Test with conversation history
event_with_history = {
    'body': json.dumps({
        'prompt': 'What about its population?',
        'conversation_history': [
            {'role': 'user', 'content': 'What is the capital of France?'},
            {'role': 'assistant', 'content': 'The capital of France is Paris.'}
        ]
    })
}

print("\n--- Conversation History Test ---")
response_with_history = handler(event_with_history, None)
print(json.dumps(json.loads(response_with_history['body']), indent=2))
