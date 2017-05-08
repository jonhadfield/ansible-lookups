# (c) 2017, Jon Hadfield <jon@lessknown.co.uk>
"""
Description: This lookup takes an AWS region and a list of one or more
security Group Names and returns a list of matching security Group IDs. 

Example Usage:
{{ lookup('aws_secgroup_ids_from_names', ('eu-west-1', ['nginx_group', 'mysql_group'])) }}
"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.errors import *
from ansible.plugins.lookup import LookupBase

try:
    import boto3
    import botocore
except ImportError:
    raise AnsibleError("aws_secgroup_ids_from_names lookup cannot be run without boto installed")


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        region = terms[0][0]
        group_names = terms[0][1]
        if isinstance(group_names, basestring):
            group_names = [group_names]
        session = boto3.session.Session(region_name=region)
        try:
            ec2_client = session.client('ec2')
        except botocore.exceptions.NoRegionError:
            raise AnsibleError("AWS region not specified.")
        # for group_name in group_names:
        secgroup_filter = [{'Name': 'group-name', 'Values': group_names}]
        result = ec2_client.describe_security_groups(Filters=secgroup_filter)
        groups = result.get('SecurityGroups')
        group_ids = []
        if groups:
            for group in groups:
                group_ids.append(group.get('GroupId').encode('utf-8'))
        return group_ids
