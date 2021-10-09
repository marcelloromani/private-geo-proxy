import logging

from common.ec2 import get_boto3_ec2_client, find_instances

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# The boto3 EC2 client
_client = None


def lambda_handler(event, _):
    logger.info(event)

    global _client
    if _client is None:
        _client = get_boto3_ec2_client()

    instances = find_instances(_client)
    if len(instances) > 0:
        return "Running instance(s): {}".format(
            ", ".join(list(map(lambda x: x['InstanceId'], instances)))
        )
    else:
        return "No instances running."
