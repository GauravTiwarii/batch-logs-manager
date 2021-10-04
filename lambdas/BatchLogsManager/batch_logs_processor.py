import csv
import boto3

TOTAL_VALID_COLUMNS = 6


def get_s3_object_attributes_from_event(event):
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]
    return bucket_name, key


def process_batch_logs(bucket_name, batch_log_file_name):
    print("Processed batch logs")

    s3_resource = boto3.resource('s3')
    s3_object = s3_resource.Object(bucket_name, batch_log_file_name)

    data = s3_object.get()['Body'].read().decode('utf-8').splitlines()

    batch_logs = csv.reader(data)
    headers = next(batch_logs)
    print('headers: %s' % headers)
    for batch_log in batch_logs:
        if len(batch_log) < 6 or len(batch_log) > 6:
            log_error("Error: InvalidRow. Total Missing/Extra Fields : " + abs(len(line) - TOTAL_VALID_COLUMNS))
        else:
            if validate(batch_log):
                print(batch_log)
                print(batch_log[0], batch_log[1], batch_log[2], batch_log[3], batch_log[4], batch_log[5])

    print(bucket_name)
    print(batch_log_file_name)


def validate(batch_log):
    if validate_batch_reference(batch_reference=batch_log[0]):
        return True

    return False


def validate_batch_reference(batch_reference):
    if not batch_reference.isalnum():
        log_error("Invalid Batch Reference : Batch Reference must be alphanumeric.")
        return False
    if not len(batch_reference) == 20:
        log_error("Invalid Batch Reference : Batch Reference length must be 20.")
        return False

    return True


def log_error(error):
    print(error)
