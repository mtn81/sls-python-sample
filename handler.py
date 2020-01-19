# coding: utf-8
import json
import logging
import boto3
import uuid
import os

# ログの設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# DynamoDB
logger.info('DYNAMO_URL:' + str(os.environ.get('DYNAMO_URL')))
dynamodb = (lambda url: 
    boto3.resource('dynamodb') if url is None 
    else boto3.resource('dynamodb', endpoint_url=url)
)(os.environ.get('DYNAMO_URL'))

#dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
#dynamodb = boto3.resource('dynamodb')
persons_tbl = dynamodb.Table('persons')


def create_person(event, context):
    logger.info('context:' + str(context))
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

