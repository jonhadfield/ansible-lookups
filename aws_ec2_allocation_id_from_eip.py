# (c) 2015, Jon Hadfield <jon@lessknown.co.uk>
"""
Description: This lookup takes an AWS region and an elastic ip address
and returns the allocation id.

Example Usage:
{{ lookup('aws_ec2_allocation_id_from_eip', ('eu-west-1', '54.54.54.54') }}
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
    raise AnsibleError("aws_ec2_allocation_id_from_eip lookup cannot be run without boto installed")

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        region = terms[0][0]
        public_ip = terms[0][1]
        session=boto3.session.Session(region_name=region)

        try:
            ec2_client=session.connect('ec2')
        except botocore.exception.NoRegionError:
            raise AnsibleError("AWS region not specified")

        ip_filter=[{'Name': 'public-ip', 'Values': [public_ip]}]

        result=ec2_client.describe_addresses(Filders=ip_filter)

        if result and result.get('Addresses'):
            return [result.get('Addresses')[0].get('AllocationId').encode('utf-8')]
        return None
