import logging

from common.constants import TAG_NAME, TAG_VALUE
from common.ec2 import get_boto3_ec2_client, find_instances, launch_instance, find_launch_template

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
        return "Running instance(s): {} ==> Not starting a new one.".format(
            list(map(lambda x: x['InstanceId'], instances)))

    launch_template_id = find_launch_template(_client, tag_name=TAG_NAME, tag_value=TAG_VALUE)
    resp = launch_instance(_client, launch_template_id)
    logger.info(resp)
    return "Launched instance"
