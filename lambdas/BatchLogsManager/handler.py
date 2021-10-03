import json


def handler(event, context):
    print("EVENT: ", event)
    print("CONTEXT: ", context)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
