from fixtures.s3_event import s3_client


def test_handler(s3_client):
    print(s3_client)
    pass
