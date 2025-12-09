import os
from strands.models import BedrockModel

BEDROCK_MODEL_ID = os.environ.get('BEDROCK_MODEL_ID', 'us.amazon.nova-micro-v1:0')
REGION = os.environ.get('AWS_REGION', 'us-east-1')

model = BedrockModel(model_id=BEDROCK_MODEL_ID, region=REGION)
