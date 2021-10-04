import json
from batch_logs_processor import process_batch_logs, get_s3_object_attributes_from_event


def handler(event, context):
    print("EVENT: ", event)
    print("CONTEXT: ", context)
    bucket_name, key = get_s3_object_attributes_from_event(event)
    print("PROCESS: ", process_batch_logs(bucket_name, key))
    process_batch_logs(bucket_name, key)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
