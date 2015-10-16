# (c) 2015, Jon Hadfield <jon@lessknown.co.uk>
"""
Description: This lookup retrieves the numerical id of the AWS account that
matches the discovered credentials. You might want to use this to check that
Ansible is going to manage the correct account before you run any tasks.

Example Usage:
{{ lookup('aws_account_id') }}
"""
from ansible import errors
try:
    import boto
except ImportError:
    raise AnsibleError("aws_account_id lookup cannot be run without boto installed")
try:
    import simplejson as json
except ImportError:
    import json
from six.moves import urllib


class LookupModule(object):
    def __init__(self, basedir=None, **kwargs):
                                self.basedir = basedir

    def run(self, **kwargs):
        try:
            iam_conn = boto.connect_iam()
            return [iam_conn.get_user().arn.split(':')[4]]
        except:
            response = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/iam/info/')
            response_content = response.read()
            json_output = json.loads(response_content)
            arn = json_output.get('InstanceProfileArn')
            return [arn.split(':')[4]]
