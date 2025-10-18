import json

def handler(event, context):
    """Simple test function"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'message': 'Netlify Python function works!',
            'event': event
        })
    }
