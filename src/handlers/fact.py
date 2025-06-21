# Handler for fact endpoint
import json
from logging import setup_log, log
from bedrock_client import query_bedrock

def getFact(event, context):
    setup_log(event, context)
    log('Request to /fact')
    try:
        fact = query_bedrock("Generate a random fact.")
        return {
            'statusCode': 200,
            'body': json.dumps({'fact': fact})
        }
    except Exception as e:
        log(f'Error: {str(e)}')
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }
