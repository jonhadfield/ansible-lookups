# (c) 2015, Jon Hadfield <jon@lessknown.co.uk>
"""
Description: This lookup takes an AWS region and an elastic ip address
and returns the associated NAT gateway id

Example Usage:
{{ lookup('aws_ec2_nat_gateway_id_from_eip', ('eu-west-1', '54.54.54.54') }}
"""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import codecs

from ansible.errors import *
from ansible.plugins.lookup import LookupBase

try:
    import botocore
    import boto3
except ImportError:
    raise AnsibleError("aws_ec2_allocation_id_from_eip lookup cannot be run without botocore and boto3 installed")

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        region = terms[0][0]
        eip = terms[0][1]
        session = boto3.session.Session(region_name=region)
        try:
            ec2_client = session.client('ec2')
        except botocore.exceptions.NoRegionError:
            raise AnsibleError("AWS region not specified.")
        filter = [{'Name': 'state','Values': ['available']}]
        result = ec2_client.describe_nat_gateways(Filter=filter)
        nat_gateways = result.get('NatGateways')
        if nat_gateways:
            for nat_gateway in nat_gateways:
              nat_gateway_addresses = nat_gateway.get('NatGatewayAddresses')
              if nat_gateway_addresses:
                  for nat_gateway_address in nat_gateway_addresses:
                      if nat_gateway_address.get('PublicIp') == eip:
                          return [nat_gateway.get('NatGatewayId').encode('utf-8')]
