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
    raise AnsibleError("aws_route_table_list_from_vpc_id cannot be run without boto3 installed")


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        if isinstance(terms, basestring):
            terms = [terms]

        routeTable_ids=[]

        region = terms[0][0]
        vpc_id = terms[0][1]
        session = boto3.session.Session(region_name=region)
        try:
            ec2_client = session.client('ec2')
        except botocore.exceptions.NoRegionError:
            raise AnsibleError("AWS region not specified.")

        vpc_filter = [{'Name': 'vpc-id', 'Values': vpc_id}]
        result = ec2_client.describe_route_tables(Filters=vpc_filter)
        routeTables = result.get('RouteTables')

        if (routeTables):
            for routeTable in routeTables:
                routeTable_ids.append(routeTables.get('RouteTableId').encode('utf-8'))

        return routeTable_ids
