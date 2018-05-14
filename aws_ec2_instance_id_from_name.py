# (c) 2015, Jon Hadfield <jon@lessknown.co.uk>
"""
Description: This lookup takes an AWS region and a 'Name' tag
value of an ec2 instance and returns the instance id.

Example Usage:
{{ lookup('aws_ec2_instance_id_from_name', ('eu-west-1', 'server1') }}
"""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import *
from ansible.plugins.lookup import LookupBase

try:
    import boto3
    import botocore
except ImportError:
    raise AnsibleError("aws_ec2_instance_id_from_name lookup cannot be run without boto installed")

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        region = terms[0][0]
        instance_name = terms[0][1]

        session=boto3.session.Session(region_name=region)
        try:
            ec2_client=session.client('ec2')
        except botocore.exception.NoRegionError:
            raise AnsibleError("AWS region not specified")

        instance_filter=[{'Name':'tag:Name', 'Values': [instance_name]}]

        result=ec2_client.describe_instances(Filters=instance_filter)

        if result and result.get('Reservations'):
            return [result.get('Reservations')[0].get('Instances')[0].get('InstanceId').encode('utf-8')]
        return None
