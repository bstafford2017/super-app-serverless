from handlers.ask import handler
import json

event = {
	'body': json.dumps({
		'prompt': 'What is the capital of France?',
		'conversation_history': []
	})
}

print(handler(event, None))