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
