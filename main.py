import os

import boto3
import json
from botocore.exceptions import ClientError

CASSIE_TUTORING = "cassie_tutoring"
CASSIE_TUTORING_EMAIL = os.getenv("CASSIE_TUTORING_EMAIL")

MIDIOWAVENDING = "midiowavending"
MIDIOWAVENDING_EMAIL = os.getenv("MIDIOWAVENDING_EMAIL")

OTHER_EMAIL = os.getenv("OTHER_EMAIL")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")


def get_recipient(from_company):
    if from_company == CASSIE_TUTORING:
        return CASSIE_TUTORING_EMAIL
    elif from_company == MIDIOWAVENDING:
        return MIDIOWAVENDING_EMAIL
    else:
        return OTHER_EMAIL


def lambda_handler(event, context):
    print("Incoming: " + json.dumps(event, indent=2))
    incoming_body = json.loads(event["body"])
    message = f"{incoming_body['message']}\n\nFrom Email: {incoming_body['email']} \nName: {incoming_body['name']}"
    sender = SENDER_EMAIL

    recipient = get_recipient(incoming_body["to"])

    print("===SENDING EMAIL===")
    try:
        client = boto3.client('ses', region_name="us-east-1")
        response = client.send_email(
            Destination={
                "ToAddresses": [recipient]
            },
            Message={
                "Body": {
                    "Text": {
                        "Data": message
                    }
                },
                "Subject": {
                    "Data": "Website Contact"
                }
            },
            Source=sender
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:")
        print(response['MessageId'])

    return {
        'statusCode': 200,
        'body': json.dumps({'input': event})
    }