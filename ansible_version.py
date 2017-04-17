# (c) 2017, Jon Hadfield <jon@lessknown.co.uk>
"""
Description: This lookup retrieves the ansible version. Note: Only works on Ansible 2.2 and above.

Example Usage:
{{ lookup('ansible_version') }}
"""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.release import __version__ as ansible_version


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        return [ansible_version]
