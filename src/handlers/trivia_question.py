
import os
import json
import boto3

# Initialize the Bedrock Runtime client
bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')

# Use Amazon Titan Text Lite v1 model
BEDROCK_MODEL_ID = 'amazon.titan-text-lite-v1'

# Reduce max tokens to further cut costs
MAX_TOKENS_TO_SAMPLE = 1250

def bedrock_query(prompt):
    response = bedrock_client.invoke_model(
        modelId=BEDROCK_MODEL_ID,
        contentType='application/json',
        accept='application/json',
        body=json.dumps({
            "inputText": prompt,
            'textGenerationConfig': {
                'maxTokenCount': MAX_TOKENS_TO_SAMPLE
            }
        })
    )
    return response['body'].read().decode('utf-8')


def generate_trivia(event, context):
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

    # Use Bedrock to generate a trivia question
    prompt = (
        f"Generate a random trivia question about {topic}. "
        "Respond in JSON with keys 'question', 'answers' (a list of 4 options), and 'correctAnswer'. "
        "Example: {\"question\": \"...\", \"answers\": [\"A\", \"B\", \"C\", \"D\"], \"correctAnswer\": \"A\"}"
    )

    try:
        response = bedrock_query(prompt)
        output = json.loads(response).get("results", [{}])[0].get("outputText", "No results found.")
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Failed to generate trivia: {str(e)}'}),
            'headers': {'Content-Type': 'application/json'}
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'response': output}),
        'headers': {'Content-Type': 'application/json'}
    }
