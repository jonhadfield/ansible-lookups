# (c) 2015, Jon Hadfield <jon@lessknown.co.uk>
"""
Description: This lookup takes an AWS region and a 'Name' tag value
of and ec2 instance and returns the current state.

Example Usage:
{{ lookup('aws_ec2_instance_status_from_name', ('eu-west-1', 'server1') }}
"""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

# import os
# import codecs

from ansible.errors import *
from ansible.plugins.lookup import LookupBase

try:
    # import boto
    # import boto.ec2

    import boto3
    import botocore
except ImportError:
    raise AnsibleError("aws_ec2_instance_status_from_name lookup cannot be run without boto installed")

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        region=terms[0][0]
        instance_id=terms[0][1]

        session=boto3.session.Session(region_name=region)

        try:
            ec2_client=session.client('ec2')
        except botocore.exceptions.NoRegionError:
            raise AnsibleError("AWS region not specified")

        instance_filter=[{'Name': 'instance-id', 'Values': [instance_id]}]

        result=ec2_client.describe_instance_status(InstanceIds=[instance_id])

        if result and result.get('InstanceStatuses'):
            return [result.get('InstanceStatuses')[0].get('InstanceState').get('Name').encode('utf-8')]
        return None