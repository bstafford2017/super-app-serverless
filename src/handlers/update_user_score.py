import os
import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMO_TABLE_NAME', 'user-scores')
table = dynamodb.Table(table_name)

def update_score(event, context):
    """
    Lambda handler to update a user's score in DynamoDB.
    Expects a JSON body with 'cognitoId' and 'score' fields.
    """

    try:
        body = json.loads(event.get('body', '{}'))
        question = body['question']
        answers = body['answers']  # Should be a list
        correct_answer = body['correctAnswer']
        user_answer = body['userAnswer']

        # Extract Cognito user sub from requestContext
        cognito_id = None
        authorizer = event.get('requestContext', {}).get('authorizer', {})
        claims = authorizer.get('claims', {})
        if isinstance(claims, str):
            # Sometimes claims may be a JSON string
            try:
                claims = json.loads(claims)
            except Exception:
                claims = {}
        cognito_id = claims.get('sub')
        if not cognito_id:
            raise ValueError('Cognito user id (sub) not found in requestContext')
    except (KeyError, ValueError, TypeError):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing or invalid request properties. Required: question, answers, correctAnswer, userAnswer, and Cognito user context.'}),
            'headers': {'Content-Type': 'application/json'}
        }

    # Determine if the user's answer is correct
    is_correct = (str(user_answer).strip().lower() == str(correct_answer).strip().lower())

    # Fetch current score and history
    try:
        response = table.get_item(Key={'cognitoId': cognito_id})
        item = response.get('Item', {})
        current_score = item.get('score', 0)
        history = item.get('history', [])
    except Exception:
        current_score = 0
        history = []

    # Update score
    if is_correct:
        current_score += 100
        result = 'correct'
    else:
        current_score -= 100
        result = 'incorrect'

    # Append to history with question/answers
    history.append({
        'question': question,
        'answers': answers,
        'correctAnswer': correct_answer,
        'userAnswer': user_answer,
        'result': result,
        'score': current_score
    })

    # Save updated score and history
    try:
        table.put_item(
            Item={
                'cognitoId': cognito_id,
                'score': current_score,
                'history': history
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Score updated successfully', 'score': current_score, 'history': history}),
            'headers': {'Content-Type': 'application/json'}
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }
