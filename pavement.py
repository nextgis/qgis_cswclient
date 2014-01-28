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

from paver.easy import task, cmdopts, needs, pushd, sh, call_task, path, \
    info, options, Bunch

BASEDIR = path('.').dirname()
USERDIR = os.path.join(os.path.expanduser('~'), 'MetaSearch-dist')

options(
    base=Bunch(
        home=BASEDIR,
        docs=path('%s/docs' % BASEDIR),
        plugin=path('%s/plugin/MetaSearch' % BASEDIR),
        install=path('%s/.qgis2/python/plugins/MetaSearch' % USERDIR),
        tmp=path(path('%s/MetaSearch-dist' % USERDIR))
    ),
    ui=Bunch(
        qt_bin='/c/OSGeo4W/bin',
        ui_files=[
            'cswclientdialogbase.ui',
            'cswresponsedialogbase.ui',
            'managecswconnectionsdialogbase.ui',
            'newcswconnectiondialogbase.ui'
        ]
    )
)


@task
def build_qt_files():
    """build ui and resource files"""
    os.system('/c/OSGeo4W/bin/pyrcc4 -o %s/resources.py %s/resources.qrc' % (options.base.plugin, options.base.plugin))
    for ui_file in options.ui.ui_files:
        ui_file_basename = os.path.splitext(ui_file)[0]
        os.system('/c/OSGeo4W/bin/pyuic4 -o %s/ui/%s.py %s/ui/%s.ui' % (options.base.plugin, ui_file_basename, options.base.plugin, ui_file_basename))


@task
def install():
    """install plugin into QGIS environment"""

    #call_task('build_qt_files')

    options.base.install.rmtree()
    shutil.copytree(options.base.plugin, options.base.install)


@task
def refresh_docs():
    """Build sphinx docs from scratch"""
    with pushd(options.base.docs):
        sh('make clean')
        sh('make html')


@task
def publish_docs():
    """this script publish Sphinx outputs to github pages"""

    call_task('refresh_docs')
    sh('git clone git@github.com:geopython/OWSLib.git %s' % options.base.tmp)
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
