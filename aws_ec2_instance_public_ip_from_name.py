# (c) 2015, Jon Hadfield <jon@lessknown.co.uk>
"""
Description: This lookup takes an AWS region and a 'Name' tag value
of and ec2 instance and returns the current public IP address.

Example Usage:
{{ lookup('aws_ec2_instance_public_ip_from_name', ('eu-west-1', 'server1') }}
"""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import codecs

from ansible.errors import *
from ansible.plugins.lookup import LookupBase

try:
    import boto3
    import botocore
except ImportError:
    raise AnsibleError("aws_ec2_instance_public_ip_from_name lookup cannot be run without boto3 installed")

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        region = terms[0][0]
        instance_name = terms[0][1]

        session=boto3.session.Session(region_name=region)

        try:
            ec2_client=session.client('ec2')
        except botocore.exceptions.NoRegionError:
            raise AnsibleError("AWS region must be specified")

        instance_filter=[{'Name': 'tag:Name', 'Values': [instance_name]}]

        result=ec2_client.describe_instances(Filters=instance_filter)

        result=result.get('Reservations')

        if result and result[0].get('Instances'):
            return [result[0].get('Instances')[0].get('PublicIpAddress').encode('utf-8')]
        return None
