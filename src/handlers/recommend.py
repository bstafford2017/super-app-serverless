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
    # Use the Converse API format for AWS Nova
    body = json.dumps({
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "inference_parameters": {
            "max_tokens": MAX_TOKENS_TO_SAMPLE,
            "temperature": 0.7
        }
    })
    response = bedrock_client.invoke_model(
        modelId=BEDROCK_MODEL_ID,
        body=body,
        accept='application/json',
        contentType='application/json'
    )
    response_body = response['body'].read().decode('utf-8')
    # Parse the Converse API response
    try:
        result = json.loads(response_body)
        # Nova returns a 'content' field in the first message of 'choices'
        return result.get('choices', [{}])[0].get('message', {}).get('content', 'No results found.')
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
