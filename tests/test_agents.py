import json
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'handlers'))

from ask import handler

test_cases = [
    {'prompt': 'What is the capital of France?', 'expected_agent': 'geography'},
    {'prompt': 'What is 25 multiplied by 17?', 'expected_agent': 'math'},
    {'prompt': 'Who won the NBA championship in 2023?', 'expected_agent': 'sports'},
    {'prompt': 'Explain what Python decorators are', 'expected_agent': 'technology'},
    {'prompt': 'Who painted the Mona Lisa?', 'expected_agent': 'art'},
    {'prompt': 'What are the benefits of drinking water?', 'expected_agent': 'health'},
    {'prompt': 'Tell me an interesting fact about space', 'expected_agent': 'trivia'}
]

print("Testing Multi-Agent System\n" + "="*50)

for i, test in enumerate(test_cases, 1):
    event = {'body': json.dumps({'prompt': test['prompt']})}
    
    print(f"\nTest {i}: {test['expected_agent'].upper()} Agent")
    print(f"Prompt: {test['prompt']}")
    
    response = handler(event, None)
    result = json.loads(response['body'])
    
    if response['statusCode'] == 200:
        print(f"✓ Status: SUCCESS")
        print(f"Response: {result['response'][:100]}...")
    else:
        print(f"✗ Status: FAILED")
        print(f"Error: {result.get('error')}")

print("\n" + "="*50)
print("All tests completed")
