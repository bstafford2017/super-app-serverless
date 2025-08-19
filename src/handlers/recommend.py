# Handler for fact endpoint
import boto3
import json
import os
from datetime import datetime
import traceback


# Initialize the Bedrock Runtime client
bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')

# Use Amazon Nova Micro model
BEDROCK_MODEL_ID = os.environ.get('BEDROCK_MODEL_ID', '')

# Reduce max tokens to further cut costs
MAX_TOKENS_TO_SAMPLE = 100

def query_bedrock(prompt: str):
    body = json.dumps({
        "max_tokens": MAX_TOKENS_TO_SAMPLE,
        "temperature": 0.7,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}],
            }
        ],
    })
    response = bedrock_client.invoke_model(
        modelId=BEDROCK_MODEL_ID,
        body=body,
        accept='application/json',
        contentType='application/json'
    )
    response_body = response['body'].read().decode('utf-8')
    # Parse the response
    try:
        result = json.loads(response_body)
        # Try to extract content from the response
        content = result.get("content", [])
        if isinstance(content, list) and len(content) > 0 and isinstance(content[0], dict):
            return content[0].get("text", "No results found.")
        return "No results found."
    except Exception:
        return response_body


def recommend(event, context=None):
    print('Request to /recommend')

    try:
        body = json.loads(event['body'])
        topic = body.get("topic")
    except Exception as e:
        print(f'Error parsing request body: {e}')
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid request body'})
        }

    if not topic:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Topic is required'})
        }

    try:
        prompt = f"You're a quirky trivia master. Tell me a fun fact about {topic}. Make it short and surprising."
        output = query_bedrock(prompt)
        return {
            'statusCode': 200,
            'body': json.dumps({'response': output})
        }
    except Exception as e:
        print(f'Error: {str(e)}')
        traceback.print_exc()
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }
