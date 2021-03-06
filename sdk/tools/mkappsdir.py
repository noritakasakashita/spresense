#!/usr/bin/env python3
# -*- coding: utf-8 -*-
############################################################################
# tools/mkappsdir.py
#
#   Copyright 2018 Sony Semiconductor Solutions Corporation
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of Sony Semiconductor Solutions Corporation nor
#    the names of its contributors may be used to endorse or promote
#    products derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
# OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
# AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
############################################################################

import os
import sys
import re

TOOL_DESCRIPTION = '''
Create a new application directory at the outside of sdk repository

This tool must be run on sdk directory.
'''

TEMPLATENAME = 'examples'

def replaced_copy(srcfile, dstfile, appname):
    with open(srcfile, 'r') as src:
        with open(dstfile, 'w') as dst:
            for line in src:
                l = line.replace(TEMPLATENAME, appname)
                dst.write(l)

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=TOOL_DESCRIPTION)
    parser.add_argument('dirname', metavar='<dir name>', type=str,
                        help='New application directory name')
    parser.add_argument('desc', type=str, nargs="?", help='Menu description')
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='verbose messages')
    opts = parser.parse_args()

    verbose = opts.verbose

    srcdir = os.path.join('..', TEMPLATENAME)
    targetdir = os.path.join('..', opts.dirname)

    # Sanity checks

    if re.search(r'\s', opts.dirname):
        print('Any white spaces not allowed in <dir name>', file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(srcdir):
        print('examples directory not found', file=sys.stderr)
        sys.exit(2)

    try:
        os.mkdir(targetdir)
    except:
        print('%s already exists' % targetdir, file=sys.stderr)
        sys.exit(3)

    # Required files for extending application series to outside of sdk repos.

    filelist = ['LibTarget.mk', 'Makefile', 'Make.defs', 'Application.mk', '.gitignore']

    for f in filelist:
        src = os.path.join(srcdir, f)
        dst = os.path.join(targetdir, f)
        if verbose > 0:
            print('Copying file %s -> %s' % (src, dst))
        replaced_copy(src, dst, opts.dirname)

    # Finally, replace menu description

    makefile = os.path.join(targetdir, 'Makefile')

    if opts.desc:
        desc = opts.desc
    else:
        desc = opts.dirname.capitalize()

    pat = re.compile(r'MENUDESC\s*=\s*".*"')
    with open(makefile, "r") as f:
        buf = f.read()
    buf = pat.sub('MENUDESC = "%s"' % desc, buf)
    with open(makefile, "w") as f:
        f.write(buf)
