import logging

from common.ec2 import get_boto3_ec2_client, find_instances, terminate_instances

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
    if len(instances) == 0:
        msg = "No running instance(s) ==> Nothing to do"
        logger.info(msg)
        return msg

    instance_ids = list(map(lambda x: x['InstanceId'], instances))
    resp = terminate_instances(_client, instance_ids)
    logger.debug(resp)

    msg = f"Terminated instances: {instance_ids}"
    logger.info(msg)

    return msg
