import json
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from agents import supervisor

def handler(event, context):
    try:
        body = json.loads(event['body'])
        user_prompt = body.get("prompt")
        conversation_history = body.get("conversation_history", [])
    except Exception:
        return {'statusCode': 400, 'body': json.dumps({'error': 'Invalid request body'})}

    if not user_prompt:
        return {'statusCode': 400, 'body': json.dumps({'error': 'Prompt is required'})}

    try:
        messages = conversation_history + [{"role": "user", "content": user_prompt}]
        response = supervisor(messages if conversation_history else user_prompt)
        return {
            'statusCode': 200,
            'body': json.dumps({'response': str(response)})
        }
    except Exception as e:
        print(f'Error: {str(e)}')
        return {'statusCode': 500, 'body': json.dumps({'error': 'Internal server error'})}

