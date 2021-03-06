# -*- coding: utf-8 -*-
###########################################################################
# Copyright (c), The AiiDA team. All rights reserved.                     #
# This file is part of the AiiDA code.                                    #
#                                                                         #
# The code is hosted on GitHub at https://github.com/aiidateam/aiida_core #
# For further information on the license, see the LICENSE.txt file        #
# For further information please visit http://www.aiida.net               #
###########################################################################
"""User param type for click."""
from __future__ import absolute_import
import click

from aiida.cmdline.utils.decorators import with_dbenv


class UserParamType(click.ParamType):
    """
    The user parameter type for click.   Can get or create a user.
    """
    name = 'user'

    def __init__(self, create=False):
        """
        :param create: If the user does not exist, create a new instance (unstored).
        """
        self._create = create

    @with_dbenv()
    def convert(self, value, param, ctx):
        from aiida.orm.backend import construct_backend

        backend = construct_backend()
        results = backend.users.find(email=value)

        if not results:
            if self._create:
                return backend.users.create(email=value)
            else:
                self.fail("User '{}' not found".format(value), param, ctx)
        elif len(results) > 1:
            self.fail("Multiple users found with email '{}': {}".format(value, results))

        return results[0]

    @with_dbenv()
    def complete(self, ctx, incomplete):  # pylint: disable=unused-argument,no-self-use
        """
        Return possible completions based on an incomplete value

        :returns: list of tuples of valid entry points (matching incomplete) and a description
        """
        from aiida.orm.backend import construct_backend

        backend = construct_backend()
        users = backend.users.find()

        return [(user.email, '') for user in users if user.email.startswith(incomplete)]
