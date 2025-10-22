import os
import json
import boto3
import traceback

S3_CLIENT = boto3.client('s3')
S3_BUCKET = os.environ.get('S3_DOCUMENTS_BUCKET', 'super-app-documents-bucket')


def document(event, context=None):
    try:
        body = event.get('body')
        if not body:
            return {"statusCode": 400, "body": json.dumps({"error": "JSON body with key is required"})}

        try:
            parsed = json.loads(body)
        except Exception:
            return {"statusCode": 400, "body": json.dumps({"error": "Invalid JSON body"})}

        key = parsed.get('key')
        if not key:
            return {"statusCode": 400, "body": json.dumps({"error": "document key is required"})}

        if not S3_BUCKET:
            return {"statusCode": 500, "body": json.dumps({"error": "DOCUMENT_BUCKET not configured"})}

        resp = S3_CLIENT.get_object(Bucket=S3_BUCKET, Key=key)
        raw = resp['Body'].read()
        # Try to decode as utf-8, fallback to base64 if binary
        try:
            content = raw.decode('utf-8')
        except Exception:
            import base64
            content = base64.b64encode(raw).decode('ascii')

        return {"statusCode": 200, "body": json.dumps({"content": content})}

    except Exception as e:
        tb = traceback.format_exc()
        return {"statusCode": 500, "body": json.dumps({"error": str(e), "trace": tb})}
