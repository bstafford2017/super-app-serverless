# Handler for fact endpoint
import boto3
import json
from datetime import datetime
import traceback

# Initialize the Bedrock Runtime client
bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')

# Use Amazon Titan Text Lite v1 model
BEDROCK_MODEL_ID = 'amazon.titan-text-lite-v1'

# Reduce max tokens to further cut costs
MAX_TOKENS_TO_SAMPLE = 100

def query_bedrock(prompt: str):
    body = json.dumps({
        'inputText': prompt,
        'textGenerationConfig': {
            'maxTokenCount': MAX_TOKENS_TO_SAMPLE
        }
    })
    response = bedrock_client.invoke_model(
        modelId=BEDROCK_MODEL_ID,
        body=body,
        accept='application/json',
        contentType='application/json'
    )
    return response['body'].read().decode('utf-8')


def ask(event, context=None):
    print('Request to /ask')
    try:
        body = json.loads(event['body'])
        user_prompt = body.get("prompt")
    except Exception as e:
        print(f'Error parsing request body: {e}')
        return {
            'statusCode': 400,
            'body': {'error': 'Invalid request body'}
        }

    if not user_prompt:
        return {
            'statusCode': 400,
            'body': {'error': 'Prompt is required'}
        }

    try:
        response = query_bedrock(user_prompt)
        output = json.loads(response).get("results", [{}])[0].get("outputText", "No results found.")
        return {
            'statusCode': 200,
            'body': {'response': output}
        }
    except Exception as e:
        print(f'Error: {str(e)}')
        traceback.print_exc()
        return {
            'statusCode': 500,
            'body': {'error': 'Internal server error'}
        }
