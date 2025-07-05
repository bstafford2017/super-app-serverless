
import os
import json
import boto3

# Initialize the Bedrock Runtime client
bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')

# Use Amazon Titan Text Lite v1 model
BEDROCK_MODEL_ID = 'amazon.titan-text-lite-v1'

# Reduce max tokens to further cut costs
MAX_TOKENS_TO_SAMPLE = 100

def bedrock_query(prompt, temperature=0.7):
    """
    Query AWS Bedrock with the given prompt and parameters.
    Returns the parsed JSON object from the model's response.
    """
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
    return json.loads(response).get("results", [{}])[0].get("outputText", "No results found.")


def generate_trivia(event, context):
    """
    Lambda handler to generate a random trivia question about a topic using Bedrock.
    Expects a JSON body with a 'topic' field (e.g., 'science', 'math', 'history').
    """
    # Parse topic from event
    try:
        body = json.loads(event.get('body', '{}'))
        topic = body.get('topic', 'science')
    except Exception:
        topic = 'science'

    # Use Bedrock to generate a trivia question
    prompt = (
        f"Generate a random trivia question about {topic}. "
        "Respond in JSON with keys 'question', 'answers' (a list of 4 options), and 'correctAnswer'. "
        "Example: {\"question\": \"...\", \"answers\": [\"A\", \"B\", \"C\", \"D\"], \"correctAnswer\": \"A\"}"
    )

    try:
        trivia = bedrock_query(prompt)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Failed to generate trivia: {str(e)}'}),
            'headers': {'Content-Type': 'application/json'}
        }

    return {
        'statusCode': 200,
        'body': json.dumps(trivia),
        'headers': {'Content-Type': 'application/json'}
    }
