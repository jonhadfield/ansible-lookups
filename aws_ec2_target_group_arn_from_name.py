# (c) 2016, Jon Hadfield <jon@lessknown.co.uk>
"""
Description: This lookup takes an AWS region and a target group name
and returns the target group arn

Example Usage:
{{ lookup('aws_ec2_target_group_arn_from_name', ('eu-west-1', 'tgname') }}
"""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import *
from ansible.plugins.lookup import LookupBase

try:
    import botocore
    import boto3
except ImportError:
    raise AnsibleError("aws_ec2_target_group_arn_from_name lookup cannot be run without botocore and boto3 installed")

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        region = terms[0][0]
        tg_name = terms[0][1]
        session = boto3.session.Session(region_name=region)
        try:
            elbv2_client = session.client('elbv2')
        except botocore.exceptions.NoRegionError:
            raise AnsibleError("AWS region not specified.")
        result = elbv2_client.describe_target_groups(Names=[tg_name])
        target_groups = result.get('TargetGroups')
        if target_groups:
            return [target_groups[0]['TargetGroupArn'].encode('utf-8')]
