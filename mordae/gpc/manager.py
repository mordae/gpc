#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from twisted.internet.threads import deferToThread
from twisted.internet import task, reactor

from uuid import uuid4

__all__ = ['Manager']


class Manager(object):
    """Persistent application logic."""

    def __init__(self):
        """Prepare the input store."""
        self.inputs = {}

    def store_input(self, inp, keep=600):
        """Store input for given period of time under a generated name."""

        name = uuid4().hex
        self.inputs[name] = inp

        reactor.callLater(keep, self.discard_input, name)

        return name

    def get_input(self, name):
        return self.inputs.get(name)

    def discard_input(self, name):
        try:
            del self.inputs[name]
        except KeyError:
            pass


# vim:set sw=4 ts=4 et:
