# coding: utf-8
import json
import logging
import boto3
import uuid

# ログの設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# DynamoDB
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
persons_tbl = dynamodb.Table('persons')


def create_person(event, context):
    logger.info('headers:' + str(event['headers']))
    logger.info('body:' + event['body'])

    body = json.loads(event['body'])

    id = str(uuid.uuid4())
    persons_tbl.put_item(
        Item = {
            'id': id,
            'name': body['name'],
            'age': body['age']
        }
    )

    response = {
        "statusCode": 200,
        "body": json.dumps({
            'id': id
        })
    }

    return response


def get_person(event, context):
    logger.info('event' + str(event['pathParameters']))

    id = event['pathParameters']['id']
    res = persons_tbl.get_item(Key={'id': id})
    logger.info(f'dynamodbres = {res}')
    person = res.get('Item')

    if person is None:
        return {
            "statusCode": 404,
            "body": json.dumps({
                'message': 'Not Found'
            })
        }
    else:
        return {
            "statusCode": 200,
            "body": json.dumps(person)
        }

