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

from paver.easy import task, cmdopts, needs, pushd, sh, call_task, path, info

BASEDIR = os.path.abspath(os.path.dirname(__file__))
PLUGINDIR = os.path.join(BASEDIR, 'plugin', 'MetaSearch')

DOCS = os.path.join(BASEDIR, 'docs')

TMPDIR = os.path.join(os.path.expanduser('~'), 'MetaSearch-dist')

QT_BIN = '/c/OSGeo4W/bin'
PYUIC4 = os.path.join(QT_BIN, 'pyuic4')
PYRCC4 = '%s/pyrcc4' % QT_BIN

UI_FILES = [
    'cswclientdialogbase.ui',
    'cswresponsedialogbase.ui',
    'managecswconnectionsdialogbase.ui',
    'newcswconnectiondialogbase.ui',
]


@task
def build_qt_files():
    """build ui and resource files"""
    os.system('/c/OSGeo4W/bin/pyrcc4 -o %s/resources.py %s/resources.qrc' % (PLUGINDIR, PLUGINDIR))
    for ui_file in UI_FILES:
        ui_file_basename = os.path.splitext(ui_file)[0]
        os.system('/c/OSGeo4W/bin/pyuic4 -o %s/ui/%s.py %s/ui/%s.ui' % (PLUGINDIR, ui_file_basename, PLUGINDIR, ui_file_basename))


@task
def install():
    """install plugin into QGIS environment"""

    #call_task('build_qt_files')

    src = os.path.join(PLUGINDIR, 'ext-libs')

    dst = os.path.join(os.path.expanduser('~'), '.qgis2',
                       'python', 'plugins', 'MetaSearch')

    shutil.rmtree(dst, True)
    shutil.copytree(src, dst)


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
    sh('git clone git@github.com:geopython/OWSLib.git %s' % TMPDIR)
    with pushd(TMPDIR):
        sh('git checkout gh-pages')
        sh('cp -rp %s/docs/build/html/en/* .' % BASEDIR)
        sh('git add .')
        sh('git commit -am "Update docs"')
        sh('git push origin gh-pages')

    sh('rm -fr %s' % TMPDIR)


@task
def upload():
    """uploads .zip file of plugin to repository"""
    call_task('install')
