# -*- coding: utf-8 -*-
"""Sample controller with all its actions protected."""

from pyjobsweb.lib.base import BaseController

__all__ = ['SecureController']


class SecureController(BaseController):
    """Sample controller-wide authorization"""
    pass
    # # The predicate that must be met for all the actions in this controller:
    # allow_only = has_permission(
    #     'manage',
    #     msg=l_('Only for people with the "manage" permission')
    # )
    #
    # @expose('pyjobsweb.templates.index')
    # def index(self):
    #     """Let the user know that's visiting a protected controller."""
    #     flash(_("Secure Controller here"))
    #     return dict(page='index')
    #
    # @expose('pyjobsweb.templates.index')
    # def some_where(self):
    #     """Let the user know that this action is protected too."""
    #     return dict(page='some_where')
