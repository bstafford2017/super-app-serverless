import json
from datetime import datetime

context = None

def setup_log(aws_event, aws_context):
    global context
    context = aws_context

def log(message=''):
    if context is None:
        raise ValueError("Context is not set. Call setup_log first.")
    aws_request_id = context.aws_request_id
    print(
        json.dumps(
            {
                "requestId": aws_request_id,
                "datetime": datetime.now().isoformat(),
                "message": message
            },
            indent=2
        )
    )
