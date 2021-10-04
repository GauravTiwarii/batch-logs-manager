import csv
import boto3
from datetime import datetime

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
            log_error("Error: InvalidRow. Total Missing/Extra Fields : "
                      + str(abs(len(batch_log) - TOTAL_VALID_COLUMNS)))
        else:
            if validate(batch_log):
                print(batch_log)
                print(batch_log[0], batch_log[1], batch_log[2], batch_log[3], batch_log[4], batch_log[5])

    print(bucket_name)
    print(batch_log_file_name)


def validate(batch_log):
    if validate_batch_reference(batch_reference=batch_log[0]) \
            and validate_start(start=batch_log[1]) \
            and validate_end(end=batch_log[2]) \
            and validate_records(records=batch_log[3]) \
            and validate_pass(batch_pass=batch_log[4]) \
            and validate_message(message=batch_log[5]):
        return True

    return False


def validate_batch_reference(batch_reference):
    if not batch_reference.isalnum():
        log_error("Invalid Batch Reference value : Batch Reference must be alphanumeric.")
        return False
    if not len(batch_reference) == 20:
        log_error("Invalid Batch Reference value : Batch Reference length must be 20.")
        return False

    return True


def validate_records(records):
    if not records.isnumeric():
        log_error("Invalid Records value: Records must be numeric.")
        return False

    return True


def validate_pass(batch_pass):
    batch_pass = str(batch_pass).lower()
    if batch_pass != "true" and batch_pass != "false":
        log_error("Invalid Records value: " + batch_pass + " : Pass must be correct boolean values.")
        return False

    return True


def validate_message(message):
    try:
        message.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        log_error("Invalid message value : " + message + " : is not valid message")
        return False
    else:
        return True


def validate_start(start):
    try:
        if start != datetime.strptime(start, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%dT%H:%M:%S"):
            log_error("Invalid start datetime value : " + start + " : Format Error")
            return False
    except ValueError:
        log_error("Invalid start datetime value : " + start + " : Parse Error")
        return False

    return True


def validate_end(end):
    try:
        if end != datetime.strptime(end, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%dT%H:%M:%S"):
            log_error("Invalid end datetime value :" + end + " : Format Error")
            return False
    except ValueError:
        log_error("Invalid end datetime value : " + end + " : Parse Error")
        return False

    return True


def log_error(error):
    print(error)
