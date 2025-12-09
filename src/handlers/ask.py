import json
import sys
import os
import logging

# Add paths for Lambda environment
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, '/var/task')

from agents import supervisor

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.info("Received request to /ask endpoint")
    
    try:
        body = json.loads(event['body'])
        user_prompt = body.get("prompt")
        conversation_history = body.get("conversation_history", [])
        logger.info(f"Conversation history length: {len(conversation_history)}")
    except Exception as e:
        logger.error(f"Failed to parse request body: {str(e)}")
        return {'statusCode': 400, 'body': json.dumps({'error': 'Invalid request body'})}

    if not user_prompt:
        logger.warning("Request missing prompt")
        return {'statusCode': 400, 'body': json.dumps({'error': 'Prompt is required'})}

    try:
        messages = conversation_history + [{"role": "user", "content": user_prompt}]
        logger.info("Invoking supervisor agent")
        response = supervisor(messages if conversation_history else user_prompt)
        logger.info("Supervisor agent completed successfully")
        return {
            'statusCode': 200,
            'body': json.dumps({'response': str(response)})
        }
    except Exception as e:
        logger.error(f'Error processing request: {str(e)}', exc_info=True)
        return {'statusCode': 500, 'body': json.dumps({'error': 'Internal server error'})}

