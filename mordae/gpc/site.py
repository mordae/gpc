#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from traceback import print_exc
from cStringIO import StringIO
from twisted.internet import reactor
from twisted.internet.threads import blockingCallFromThread

from mordae.gpc.formats import parse_input, render_output

import flask
import os
import re

__all__ = ['make_website_app']

def make_website_app(manager, debug):
    """Construct website WSGI application."""

    app = flask.Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.secret_key = os.urandom(16)
    app.debug = debug

    @app.route('/')
    def index():
        return flask.render_template('main.html')


    @app.route('/upload', methods=['POST'])
    def upload():
        if 'csv' not in flask.request.files:
            flask.flash(u'Nevybrali jste žádný soubor!')
            return flask.redirect('/')

        try:
            inp = parse_input(flask.request.files['csv'])
        except:
            print_exc()
            flask.flash(u'Nepodařilo se zpracovat vstupní soubor.')
            return flask.redirect('/')

        name = blockingCallFromThread(reactor, manager.store_input, inp, keep=1800)
        account = '%016d/%04d' % (inp.account, inp.bank)
        sequence = 0

        return flask.render_template('preview.html', **locals())

    @app.route('/process', methods=['POST'])
    def process():
        if 'name' not in flask.request.form or \
           'account' not in flask.request.form or \
           'sequence' not in flask.request.form:
            flask.flash(u'Co to proboha provádíte?!')
            return flask.redirect('/')

        name = flask.request.form['name']
        account = flask.request.form['account']
        sequence = 0

        inp = blockingCallFromThread(reactor, manager.get_input, name)
        if inp is None:
            flask.flash(u'Jejda, vstupní soubor tu už není. Příště zkuste doplnit chybějící informace rychleji...')
            return flask.redirect('/')

        try:
            sequence = int(flask.request.form['sequence'])
        except ValueError:
            flask.flash(u'Neplatné pořadové číslo. Zkuste to znovu.')
            return flask.render_template('preview.html', **locals())

        if not re.match('^[0-9]+(-[0-9]+)?/[0-9]+$', account):
            flask.flash(u'Neplatné číslo účtu. Zkuste to znovu.')
            return flask.render_template('preview.html', **locals())

        try:
            fp = StringIO()
            render_output(fp, inp, account, sequence)
            data = fp.getvalue()
        except:
            print_exc()
            flask.flash(u'Nastala chyba při zpracování souboru. Omlouváme se.')
            return flask.redirect('/')

        resp = flask.make_response(data)
        resp.headers['Content-Type'] = 'application/octet-stream'
        resp.headers['Content-Disposition'] = 'attachment; filename=account.gpc'
        return resp


    return app

# vim:set sw=4 ts=4 et:
