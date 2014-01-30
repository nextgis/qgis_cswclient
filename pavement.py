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
import shutil

from paver.easy import call_task, needs, options, path, pushd, sh, task, Bunch

USERDIR = os.path.join(os.path.expanduser('~'), 'MetaSearch-dist')

options(
    base=Bunch(
        home=(os.path.abspath(os.path.dirname(__file__))),
        docs=path('docs'),
        plugin=path('plugin/MetaSearch'),
        install=path('%s/.qgis2/python/plugins/MetaSearch' % USERDIR),
        tmp=path(path('%s/MetaSearch-dist' % USERDIR))
    )
)


@task
def build_qt_files():
    """build ui files"""

    for ui_file in os.listdir('plugin/MetaSearch/ui'):
        if ui_file.endswith('.ui'):
            print ui_file
            ui_file_basename = os.path.splitext(ui_file)[0]
            sh('pyuic4 -o %s/ui/%s.py %s/ui/%s.ui' % (options.base.plugin,
               ui_file_basename, options.base.plugin, ui_file_basename))


@task
@needs('build_qt_files')
def install():
    """install plugin into user QGIS environment"""

    if not hasattr(os, 'symlink'):
        options.base.install.rmtree()
        shutil.copytree(options.base.plugin, options.base.install)
        #options.base.plugin.copytree(options.base.install)
    elif not options.base.install.exists():
        options.base.plugin.symlink(options.base.install)


@task
def refresh_docs():
    """Build sphinx docs from scratch"""

    with pushd(options.base.docs):
        sh('make clean')
        sh('make html')


@task
@needs('refresh_docs')
def publish_docs():
    """this script publish Sphinx outputs to github pages"""

    sh('git clone git@github.com:geopython/MetaSearch.git %s' %
       options.base.tmp)
    with pushd(options.base.tmp):
        sh('git checkout gh-pages')
        sh('cp -rp %s/docs/build/html/en/* .' % options.base.home)
        sh('git add .')
        sh('git commit -am "Update docs"')
        sh('git push origin gh-pages')

    options.base.tmp.rmtree()


@task
def upload():
    """uploads .zip file of plugin to repository"""

    call_task('install')
