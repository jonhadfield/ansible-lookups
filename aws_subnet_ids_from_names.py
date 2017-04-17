# (c) 2017, Jon Hadfield <jon@lessknown.co.uk>
"""
Description: This lookup takes an AWS region and a list of one or more
subnet names and returns a list of matching subnet ids.

Example Usage:
{{ lookup('aws_subnet_ids_from_names', ('eu-west-1', ['subnet1', 'subnet2'])) }}
"""
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.errors import *
from ansible.plugins.lookup import LookupBase

try:
    import boto3
    import botocore
except ImportError:
    raise AnsibleError("aws_subnet_ids_from_names lookup cannot be run without boto installed")


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        if isinstance(terms, basestring):
            terms = [terms]
        subnet_ids = []
        region = terms[0][0]
        subnet_names = terms[0][1]
        session = boto3.session.Session(region_name=region)
        try:
            ec2_client = session.client('ec2')
        except botocore.exceptions.NoRegionError:
            raise AnsibleError("AWS region not specified.")
        subnet_filter = [{'Name': 'tag:Name', 'Values': subnet_names}]
        result = ec2_client.describe_subnets(Filters=subnet_filter)
        subnets = result.get('Subnets')
        if subnets:
            for subnet in subnets:
                subnet_ids.append(subnet.get('SubnetId').encode('utf-8'))
        return subnet_ids
