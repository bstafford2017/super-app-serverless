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
        "prompt": prompt,
        "max_gen_len": MAX_TOKENS_TO_SAMPLE,
        "temperature": 0.7,
    })
    response = bedrock_client.invoke_model(
        modelId=BEDROCK_MODEL_ID,
        body=body,
        accept='application/json',
        contentType='application/json'
    )
    response_body = response['body'].read().decode('utf-8')
    # Parse the Llama 4 Maverick 17B response
    try:
        result = json.loads(response_body)
        return result.get('generation', 'No results found.')
    except Exception:
        return response_body


def ask(event, context=None):
    print('Request to /ask')
    try:
        body = json.loads(event['body'])
        user_prompt = body.get("prompt")
    except Exception as e:
        print(f'Error parsing request body: {e}')
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid request body'})
        }

    if not user_prompt:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Prompt is required'})
        }

    try:
        response = query_bedrock(user_prompt)
        output = json.loads(response).get("results", [{}])[0].get("outputText", "No results found.")
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
