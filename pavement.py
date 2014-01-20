# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2014 Tom Kralidis (tomkralidis@gmail.com)
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/copyleft/gpl.html>. You can also obtain it by writing
# to the Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
# MA 02111-1307, USA.
#
###############################################################################

import os

from paver.easy import task, cmdopts, needs, pushd, sh, call_task, path, info

DOCS = 'docs'


@task
def refresh_docs():
    """Build sphinx docs from scratch"""
    with pushd(DOCS):
        sh('make clean')
        sh('make html')

@task
def publish_docs(options):
    """this script publish Sphinx outputs to github pages"""
    call_task('refresh_docs')
    sh('git clone git@github.com:geopython/OWSLib.git /tmp/OWSLib')
    with pushd(DOCS):
        sh('git checkout gh-pages')
        sh('cp -rp $THIS_DIR/build/html/en/* .')
        sh('git add .')
        sh('git commit -am "Update docs"')
        sh('git push origin gh-pages')

    sh('rm -fr /tmp/OWSLib')


@task
def publish_plugin():
    pass  # TODO

@task
def upload():
    pass  # TODO


@task
def install():
    pass
