import json
import cglogging as cgl
from Message import Message
from RequestRouter import RequestRouter

logger_Class = cgl.cglogging()
logger = logger_Class.setup_logging()


def lambda_handler(event, context):
    logger.debug("Received event: ")
    try:
        if 'context' not in event["body"] and 'commonParms' not in event["body"] \
                and 'domainName' not in event["body"]['context'] \
                and 'action' not in event["body"]['commonParms']:
            logger.error('Invalid message from cloudwatch: {} , error : {}'.format(event, 1))
            return Message.get_fatal_standard_message(1)

        request_action = event["body"]["commonParms"]["action"]
        logger.debug(request_action)

        return RequestRouter.router(request_action, event["body"])



    except Exception as details:
        logger.error('Exception, Unexpected error: {} , {}'.format(19002, details))
        return 19002, 'Exception, Unexpected error ', 'FATAL', 'Auto Close Handler'