#!/usr/local/bin/python
#!c:\python\python.exe

#
# Copyright 1998
# by Ivan Van Laningham
# All Rights Reserved.
#

import sys
# import os
# import time
# import math
# import string

# from getargs import *
import getargs


if __name__ == "__main__":
    progname = sys.argv[0]

    def printversion(l=0):
        print "Version 1.%s" % (l)

    def man(l=0):
        print getargs.manpage()
        sys.exit(0)

    def helpPig(l=0):
        print "%s:  Usage %s any old gunk" % (progname, xarg.options())
        print xarg,
        print "I'm Porky Pig"
        sys.exit(0)

    def helpHog(l=0):
        print xarg,
        print "I'm a HAWG!"

    arglist = (
        ("v", getargs.nofunc, "Function (print version)", printversion),
        ("M", getargs.nofunc, "Man page", man),
        ("-manual", getargs.nofunc, "Man page", man),
        ("i", 0, "Integer", None),
        ("f", 0.0, "Float", None),
        ("+snorgle", "", "A Fubar String", None),
        ("tuple", (), "Nameless tuple", None),
        ("q", None, "None test", None),
        ("list", [], "Nameless list", None),
        ("h", getargs.nofunc, "Help", helpPig),
        ("hogs", getargs.nofunc, "Help", helpHog),
        ("qln", 0L, "Funky Long", None),
        (
            "-longarg",
            None,
            "Boolean long argument",
        ),  # Adding leading - provides --longarg syntax. ...
        ("-output", getargs.nofile, "the output file", "/tmp/dogbone"),
        (
            "-longest",
            None,
            "Boolean long argument",
        ),  # Adding leading - provides --longarg syntax. ...
        (
            "-longerlongerandlonger",
            0,
            "Integer long argument",
            None,
        ),  # Adding leading - provides --longarg syntax. ...
    )
    xarg = getargs.arguments("-", arglist)
    progname, argv = xarg.getargs(sys.argv)
    helpHog()

    q = xarg.keys()
    for ii in q:
        print ii, xarg.value(ii)

    o = 0
    for n in range(len(argv)):
        print o, argv[n]
        o = o + 1

    assert xarg['longest'] is None
    assert xarg['list'] is None
