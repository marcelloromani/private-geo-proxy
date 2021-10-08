import logging

from common.constants import TAG_NAME, TAG_VALUE
from common.ec2 import get_boto3_ec2_client, find_instances

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# The boto3 EC2 client
_client = None


def find_launch_template() -> str:
    """
    Return the ID of the launch template with project=astropi
    """
    client = get_boto3_ec2_client()

    response = client.describe_launch_templates(
        Filters=[
            {
                'Name': f'tag:{TAG_NAME}',
                'Values': [
                    TAG_VALUE,
                ]
            },
        ],
    )
    templates = response['LaunchTemplates']
    if len(templates) == 0:
        raise ValueError('No launch template found with provided search paramters')
    if len(templates) > 1:
        raise ValueError(f'Was expecting 1 template but found {len(template)}')
    return templates[0]['LaunchTemplateId']


def run_instance(template_id):
    client = get_boto3_ec2_client()

    response = client.run_instances(
        MinCount=1,
        MaxCount=1,
        LaunchTemplate={
            'LaunchTemplateId': template_id,
        }
    )
    return response


def lambda_handler(event, _):
    logger.info(event)

    global _client
    if _client is None:
        _client = get_boto3_ec2_client()

    instances = find_instances(_client)
    if len(instances) > 0:
        return "Running instance(s): {} ==> Not starting a new one.".format(
            list(map(lambda x: x['InstanceId'], instances)))

    launch_template_id = find_launch_template()
    resp = run_instance(launch_template_id)
    logger.info(resp)
    return "Launched instance"
