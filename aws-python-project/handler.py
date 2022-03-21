import logging
import os
from aws_lambda_powertools.utilities.idempotency import (
    DynamoDBPersistenceLayer, IdempotencyConfig, idempotent_function)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = os.environ['IDEMPOTENCY_TABLE']

dynamodb = DynamoDBPersistenceLayer(table_name=TABLE_NAME)
config =  IdempotencyConfig(
    event_key_jmespath="body"
)

@idempotent_function(data_keyword_argument="message",config=config, persistence_store=dynamodb)
def message_consumer(message):
    logger.info(message)
    m = message['body'].upper()
    return m

def handler(event, context):
    for m in event['Records']:
        ret = message_consumer(message=m)
        logger.info("Consumer returned: {0}".format(ret))
