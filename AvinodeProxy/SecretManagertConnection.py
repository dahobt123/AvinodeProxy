import boto3
from botocore.exceptions import ClientError

import cglogging as cgl

logger_Class = cgl.cglogging()
logger = logger_Class.setup_logging()
user = ""
password = ""


class SecretManagerConnection:

    @classmethod
    def get_secrets(cls, key_name, region):
        logger.debug("inside getSecrets")

        errNum, errMsg, secret = 0, '', ''
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region
        )
        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=key_name
            )
            return get_secret_value_response
        except ClientError as e:
            logger.debug('Unexpected error: {0}'.format(e))
            if e.response['Error']['Code'] == 'DecryptionFailureException':
                return 8089, 'DecryptionFailureException', secret
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                return 8089, 'InternalServiceErrorException', secret
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                return 8089, 'InvalidParameterException', secret
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                return 8089, 'InvalidRequestException', secret
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                return 8089, 'ResourceNotFoundException', secret