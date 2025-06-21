import boto3

# Initialize the Bedrock client
bedrock_client = boto3.client('bedrock', region_name='us-east-1')

# Use a smaller, less expensive model for cost savings
BEDROCK_MODEL_ID = 'anthropic.claude-instant-v1'  # Cheaper than claude-v2

# Reduce max tokens to further cut costs
MAX_TOKENS_TO_SAMPLE = 50

def query_bedrock(prompt: str):
    response = bedrock_client.invoke_model(
        modelId=BEDROCK_MODEL_ID,
        body={
            'prompt': prompt,
            'max_tokens_to_sample': MAX_TOKENS_TO_SAMPLE
        }
    )
    return response['body'].read().decode('utf-8')
