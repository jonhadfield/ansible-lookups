# (c) 2017, Jon Hadfield <jon@lessknown.co.uk>
"""
Description: This lookup takes an AWS region and a vpc
name and returns a matching VPC ID.

Example Usage:
{{ lookup('aws_vpc_id_from_name', ('eu-west-1', 'vpc1')) }}
"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.errors import *
from ansible.plugins.lookup import LookupBase

try:
    import boto3
    import botocore
except ImportError:
    raise AnsibleError("aws_vpc_id_from_name lookup cannot be run without boto installed")


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        if isinstance(terms, basestring):
            terms = [terms]
        vpc_ids = []
        region = terms[0][0]
        vpc_names = terms[0][1]
        session = boto3.session.Session(region_name=region)
        try:
            ec2_client = session.client('ec2')
        except botocore.exceptions.NoRegionError:
            raise AnsibleError("AWS region not specified.")
        vpc_filter = [{'Name': 'tag:Name', 'Values': [vpc_names]}]
        result = ec2_client.describe_vpcs(Filters=vpc_filter)
        vpcs = result.get('Vpcs')
        if vpcs:
            vpc_ids.append(vpcs[0].get('VpcId').encode('utf-8'))
        return vpc_ids
