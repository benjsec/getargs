#!c:\python\python.exe
#!/usr/local/bin/python

"""MODULE:  getargs
Generalized option handling for Python programs.

USAGE

    from getargs import *

    Set the variable 'progname' to sys.argv[0];
    define any functions you may need in the arglist;

    create an argument list  of the form

    arglist = (
	( 'i', 0, "An integer argument", None ),
	( 'f', 0.0, "A Float argument", 3.14159 ),
	...
    )

    Instantiate a class arguments variable:

	xarg = arguments ( '-', arglist )
    
    Call the xarg.getargs() method:

	progname, sys.argv = xarg.getargs ( sys.argv )

    To query an option, use the value() method:

	if xarg.value ( 'i' ) != None :
	    do something. ...
    
    Boolean options have only two possible values, 1 or 0; if two or more
    options are mutually exclusive, it is the programmer's responisibility
    to see that the exclusivity is maintained, using the setvalue() method:

	if xarg.value ( 'j' ) :
	    xarg.setvalue ( 'g', 0 )

ARGLIST FIELDS
    Arglist fields are:

    ( key, type, docstring, value, mode )

    where:
	key = A single letter or a fullword used to find the option in sys.argv
	type = one of:
	    None  == A boolean option; these keys take no arguments;
	    0j    == Numeric flag option; each repetition of the keyletter
		increments the flagvalue;
	    0     == Requires an integer argument;
	    0L    == Requires a long integer argument (may end in 'L';
	    0.0   == Requires a floating point argument; integer,
		but not long, strings are converted into floats;
	    nofile = Requires a filename argument, or one of "stdin", "stdout" or "stderr";
	    nofunc = Value must be a valid function; takes no arguments;
	    ()    == Requires a list of arguments, usually of the form
		'a b c d e', which is returned as a tuple
	    []    == Requires a list of arguments, usually of the form
		'a b c d e', which is returned as a list
	docstring = String that represents the hint the user sees, as in:
	    "Print a help message and exit"
	value = The default value; if this is not provided, None will be used.
	mode = Used for file options only; provides the second argument to open();
	    defaults to "r".

    SINGLE LETTER OPTIONS
	Single letter options that take arguments (non-boolean) may do so in one of
	two ways, either immediately following the keyletter ('-i29') or following
	a space ('-i 29').  The choice is the user's, not the programmer's.

    LONG OPTIONS
	Long options that take arguments (non-boolean) may do so in one of two ways,
	either separated by a space ('-integer 29') or separated by a separator
	character, by default the '=' sign ('-integer=29').  Again, the choice is
	left to the user, not the programmer.

    LIST AND TUPLE ARGUMENTS
	Options that require list or tuple arguments need such an argument in the
	form of a list, which probably needs to be quoted.  By default, the list
	has the form

	    'a b c d e f'
	
	but by using the setsep() method the programmer can have it be of the form

	    'a,b,c,d,e,f'
	
	for example.

    ORDER
	The order of options is not significant.  You cannot tell if one option has been
	set on the command line before another; this should not be a problem.

    CASE
	The case of options is significant; 'i' and 'I' are different options, and so
	are '-integer' and '-Integer' (and also '-inTegeR').  However, on long options,
	the user only needs to provide sufficient information in order to set or toggle
	an option.  The matching algorithm searches for whatever substring the user
	provides; if the substring matches more than one option, then it looks first for
	an _exact_ match.  Failing that, it will match the _longest_ option name it
	can for the substring provided.  I.e., if there are two options -h and -help,
	and the user types '-he', then the option matched will be -help.

    FILE OPTIONS
	The type of these is determined by matching against the value 'nofile',
	which is defined to be the same as the value returned by 'open("/dev/null", "r")'; if 
	users are on a PC or on a Mac, they won't have "/dev/null", so "nul" is used instead.

    DETERMINING IF AN OPTION HAS APPEARED ON THE COMMAND LINE
	If the programmer provides a default value other than None, then there is no
	way to tell if the option appeared on the command line.  However, if the
	default value is None, then the value () method will return non-None if and
	only if the user put it in the command line.  This even works for boolean
	options, since the only way for one to be set this way is in the arglist;
	all other methods set the value to either 0 or 1.

    VARIABLE
	The only variable in the getargs module is 'nofile', which is used only to
	find the type of file options.

    FUNCTIONS
	Functions provided by the getargs module are:

	    nofunc()	Provided to find the type of function options.
	    isnumber()	Used to determine if a string can be converted into an
		integer; the string can contain only digits or '-' or '+'.
	    islong()	Same as isnumber(), except the string can also contain
		the letter 'L'.
	    isfloat()	The string contains digits, a period, signs or the letters
		'e' or 'E'.
	    manpage()	Returns the __doc__ attribute for the getargs module.

    CLASS
	The only class provided by getargs is class arguments.

    METHODS
	The methods provided by the arguments class are:

	    __init__ ( self, c = '-', a = ( ) ) : where
		c = switch character for options.
		a = an arglist as defined above.
	    __del__ ( self ) :
		closes any open files.
	    __repr__ ( self ) :
		Returns a string that can be used to display short
		help to the user.
	    options ( self ) :
		Returns a string of option letters or option words, suitably
		separated if need be, for use in a "Usage" message.
	    argtype ( self, let ) :
		Returns a string representing the argument type expected
		by the option.  This can be one of:
		    "#" for integers and longs;
		    "#.#" for floats;
		    "<file>" for filenames for file options;
		    "<list>" for lists and tuples;
		    "" for everything else.
		This method is used in __repr__.
	    has_key ( self, let ) :
		Returns 1 if the option key let was defined in the arglist,
		or 0 if it has not.
	    additem ( self, let, typ, str, v = None, mode = "r" ) :
		Adds a new option and fields to an existing arguments
		class variable, where:
		    let   = The option letter or word;
		    type  = the type (0, 0L, etc.)
		    v     = default value;
		    mode  = second argument to open().
		Used internally; you shouldn't ordinarily need to use this.
	    type ( self, let ) :
		Returns either the type of option ("<type 'dictionary'>", etc.)
		or None if there is no such option.
	    value ( self, let ) :
		Returns either the value of the option (0, 49L, etc.) or None
		if there is no such option.
	    mode ( self, let ) :
		Returns either the mode to be used in opening the file or None
		if there is no such option.
	    file ( self, let ) :
		If there is no such option, returns None.  Otherwise, returns
		the filename, the mode, and the file pointer (fname,mode,fp);
		the file pointer is either None, in which case the open()
		method needs to be called, or an already open file pointer
		which may be used directly.
	    open ( self, let ) :
		If this is a file option and the option exists, performs an open()
		on the filename using the stored mode.  Returns None if the option
		doesn't exist or if open() returns None.
	    close ( self, let ) :
		If this is a valid option and the file pointer is open, fflushes it
		and closes it.  There is no return value.  Automatically called
		by the __del__ method, so you don't always need to do this.
	    docstring ( self, let ) :
		Returns the docstring, if there is one and if let is a valid option.
	    len ( self ) :
		Returns the number of options currently defined.
	    keys ( self ) :
		Returns a _sorted_ list of the options.  If there are no options
		currently defined, returns None.
	    longest ( self ) :
		Returns 0 or the len() of the longest option string.
	    longestargtype ( self ) :
		Returns 0 or the len() of the longest argtype string used by the
		current set of options.
	    switchchar ( self ) :
		Returns the switch character, which is '-' by default.
	    setswitch ( self, let ) :
		Sets the switch character (the option lead-in character)
		to let:  on PCs, for example, you could set this to '/'.
	    sepchar ( self ) :
		Returns the list separator character, which is ' ' by default.
	    setsep ( self, c ) :
		Sets the list separator character to c; a good alternate for
		this might be ','.
	    parenchar ( self ) :
		Returns the character used to separate option letters or
		words from their docstrings when building the __repr__ string.
	    setsep ( self, c ) :
		Sets the option separator character to c; for example, setting this
		to ']' would result in

		    -h] Help

		instead of

		    -h) Help
	    eqchar ( self ) :
		Returns the character that separates long options from their values,
		which is set to '=' by default.
	    seteq ( self, c ) :
		Sets the long option value separator character to c; it's not a good
		idea to set this to ' '.
	    setvalue ( self, c, v ) :
		If c is a valid option, this method checks the type of v with the
		required type of c.  The value indicated by v may not be None.
		Attempting to set an improper value prints an error message and
		otherwise does nothing.
	    setargs ( self, list ) :
		If list is a list of the form ( ( let, type, docstring, ... ), ... ),
		then setargs() runs through the outer list and uses the elements of the
		inner lists as parameters to the additem() method.
	    matchlongarg ( self, m ) :
		It's better not to use this; it's used internally by the getargs()
		method, where the context is set correctly.  What it does is look
		through all the options to see if it can make a match with m; not
		all characters have to match exactly.  If m is 'long', for example,
		and there are options 'l', 'lo' and 'longest', then matchlongarg()
		will return 'longest' as its best choice.  The return value can
		then be used as an option key in, say, setvalue().
	    getargs ( self, argv ) :
		This is the interface between the option list (well, actually a
		dictionary of dictionaries) and the program's command line.
		The proper way to use this method is (for example):

		    xarg = arguments ( '-', arglist )
		    progname, sys.argv = xarg.getargs ( sys.argv )
		
		After which sys.argv[ 0 ] and all options between argv[ 0 ]
		and the first non-option argument will be consumed, leaving
		the program responsible for any remaining command-line
		parameters.  Values of any of the options may be obtained
		through the value() method.

    HISTORICAL NOTE
	I first built a version of getargs() in C many years ago, but
	I no longer support the C version; I never released it because
	I was never satisfied with it, and because it was much too
	delicate for public performance.  Also, because it was written
	in C (not C++), it could be very complicated to use.  The Python
	version cures all those problems, although I recognize that
	it's probably more complicated than some people would like.
	I'm always open to simplification suggestions.

    BUGS AND SPECIAL CONSIDERATIONS
	Functions referred to in arglist must be defined before the arglist.
	The program name (progname) must be defined (as in "progname =
	sys.argv[ 0 ]") before you can use it in any function referred to
	in the arglist.  Such functions are called as soon as they are
	found in the command line.

	While there is no way to tell if any option has been set before
	any other option, the parser does proceed in a linear manner; i.e.,
	"-out foo -help" would actually set the "-out" value "foo" before
	the "-help" function was called.  Not that there's much utility in
	that.

	Report any bugs found to "ivanlan@callware.com".  Report any
	infelicitous grammar or language errors in this __doc__
	attribute to the same place.

	Thank you for using getargs().
    COPYRIGHT
	Copyright 1994, 1995, 1996, 1997, 1998 by Ivan Van Laningham.
	All rights reserved.
	License granted to anyone for non-commercial use, as long as
	this copyright notice and the author's name are included in
	any modifications, and such modifications are reported to
	the author for consideration in future releases.

    VERSION
	Version 1.3,  12.19.6.11.6  13 Kimi  14 Yax  G1  11:11:01
"""
#
# Copyright 1994, 1995, 1996, 1997, 1998
# by Ivan Van Laningham
# All Rights Reserved.
#

import sys
import os 
import time
import math
import string

# Boolean		done	    None
# Float			done	    0.0
# String		done	    ""
# File			done	    nofile
# Function		done	    nofunc
# List			done	    []
# Tuple			done	    ()
# Read-only string	no

VERSION = "Version 1.3,  12.19.6.11.6  13 Kimi  14 Yax  G1  11:11:01"

try :
    nofile = open ( "nul", "r" )
except IOError :
    try :
	nofile = open ( "/dev/null", "r" )
    except IOError :
	nofile = sys.stdin

if not nofile :
    nofile = sys.stdin

def nofunc ( ) :
    pass

def isnumber ( s ) :
    for c in s :
	if c in string.digits or c in '-+' :
	    pass
	else :
	    return 0
    return 1

def islong ( s ) :
    for c in s :
	if c in string.digits or c in '-+' or c in 'L' :
	    pass
	else :
	    return 0
    return 1

def isfloat ( s ) :
    for c in s :
	if c in string.digits or c in '-+.eE' :
	    pass
	else :
	    return 0
    return 1

class arguments :
    def __init__ ( self, c = '-', a = ( ) ) :
	self.switch = c
	self.args = { }
	self.ne = 0
	self.sep = ' '
	self.argparen = ')'
	self.argeq = '='
	if not a == ( ) :
	    self.setargs ( a )

    def __del__ ( self ) :
	k = self.keys ( )
	for l in k :
	    if self.file ( l ) :
#		print "found file ", l
		self.close ( l )

    def __repr__ ( self ) :
	if len ( self ) > 0 :
	    lflag = ""
	    tl = self.longest ( ) + 2
	    if tl > 3 :
		lflag = " "
	    tml = self.longestargtype ( )
	    tl = tl + tml
	    s = ''
	    t = self.keys ( )
	    for i in t :
		ss = self.switch
		ss = ss + i
		astr = self.argtype ( i )
		if len ( astr ) < 1 :
		    s = s + "%s%s %s" % ( string.rjust ( self.switch + i + astr, tl ), \
			self.argparen, self.docstring ( i ) )
		else :
		    s = s + "%s%s %s" % ( string.rjust ( self.switch + i + lflag + astr, tl ), \
			self.argparen, self.docstring ( i ) )
		s = s + "\n"
	    return s	
	return None

    def options ( self ) :
	k = self.keys ( )
	s = "%s" % ( self.switch )
	sp = ""
	n = 0
	if self.longest ( ) > 1 :
	    sp = self.sep
	    s = s + "<"
	for i in k :
	    if n < self.ne - 1 :
		s = s + i + sp
	    else :
		s = s + i
	    n = n + 1
	if self.longest ( ) > 1 :
	    s = s + ">"
	return s

    def argtype ( self, let ) :
	if self.args.has_key ( let ) :
	    t = self.args[ let ]
	    z = type ( t[ "type" ] )
	    if z == type ( None ) or z == type ( nofunc ) :
		return ""
	    elif z == type ( 0j ) :
		return "*"
	    elif z == type ( 0 ) or z == type ( 0L ) :
		return '#'
	    elif z == type ( 0.0 ) :
		return '#.#'
	    elif z == type ( nofile ) :
		return '<file>'
	    elif z == type ( ( ) ) or z == type ( [ ] ) :
		return '<list>'
	return ""
	
    def has_key ( self, let ) :
	return self.args.has_key ( let )

    def additem ( self, let, typ, str, v = None, mode = "r" ) :
	self.args[ let ] = { "type" : typ, "docstring" : str, "value" : v, "mode" : mode }
	self.ne = self.ne + 1

    def type ( self, let ) :
	if self.args.has_key ( let ) :
	    t = self.args[ let ]
	    return type ( t[ "type" ] )
	return None
    
    def value ( self, let ) :
	if self.args.has_key ( let ) :
	    t = self.args[ let ]
	    if type ( t[ "value" ] ) == type ( 0j ) :
		n = int ( abs ( t[ "value" ] ) )
		return n
	    else :
		return t[ "value" ]
	return None

    def mode ( self, let ) :
	if self.args.has_key ( let ) :
	    t = self.args[ let ]
	    return t[ "mode" ]
	return None

    def file ( self, let ) :
	if self.args.has_key ( let ) and self.type ( let ) == type ( nofile ) :
	    t = self.args[ let ]
	    fname = t[ "value" ]
	    mm = t[ "mode" ]
	    if t.has_key ( "fp" ) :
		fp = t[ "fp" ]
	    else :
		fp = None
	    return fname, mm, fp
	return None

    def open ( self, let ) :
	if self.args.has_key ( let ) and self.type ( let ) == type ( nofile ) :
	    t = self.args[ let ]
	    fname = t[ "value" ]
	    mm = t[ "mode" ]
	    if mm == None :
		mm = "r"
	    if t.has_key ( "fp" ) :
		return t[ "fp" ]
	    else :
		if fname == "stdin" :
		    fp = sys.stdin
		elif fname == "stdout" :
		    fp = sys.stdout
		elif fname == "stderr" :
		    fp = sys.stderr
		else :
		    fp = open ( fname, mm )
		return fp
	return None

    def close ( self, let ) :
	if self.args.has_key ( let ) and self.type ( let ) == type ( nofile ) :
	    t = self.args[ let ]
	    if t.has_key ( "fp" ) :
		fp = t[ "fp" ]
		if fp :
		    fp.fflush ( )
		    fp.close ( )
		    fp = None
#		    print "Closed file ", t[ "value" ]

    def docstring ( self, let ) :
	if self.args.has_key ( let ) :
	    t = self.args[ let ]
	    return t[ "docstring" ]
	return ""

    def __len__ ( self ) :
	return self.ne

    def keys ( self ) :
	if len ( self ) > 0 :
	    t = self.args.keys ( )
	    t.sort ( )
	    return t
	return None
    
    def longest ( self ) :
	if len ( self ) > 0 :
	    t = self.keys ( )
	    tl = 0
	    for i in t :
		if len ( i ) > tl :
		    tl = len ( i )
	    return tl
	return 0

    def longestargtype ( self ) :
	if len ( self ) > 0 :
	    t = self.keys ( )
	    tl = 0
	    for i in t :
		tml = len ( self.argtype ( i ) )
		if tml > tl :
		    tl = tml
	    return tl
	return 0

    def switchchar ( self ) :
	return self.switch
    
    def setswitch ( self, c ) :
	self.switch = c
    
    def sepchar ( self ) :
	return self.sep

    def setsep ( self, c ) :
	self.sep = c
    
    def parenchar ( self ) :
	return self.argparen

    def setparen ( self, c ) :
	self.argparen = c

    def eqchar ( self ) :
	return self.argeq

    def seteq ( self, c ) :
	self.argeq = c

    def setvalue ( self, c, v ) :
	if self.has_key ( c ) :
	    t = self.args[ c ]
	    if self.type ( c ) == type ( nofile ) :
		if type ( v ) == type ( "" ) :
		    t[ "value" ] = v
		else :
		    print "Value", type ( v ), "for keyletter", c, "must be", type ( "" )
	    elif self.type ( c ) == type ( None ) :
		if v :
		    t[ "value" ] = 1
		else :
		    t[ "value" ] = 0
	    elif self.type ( c ) == type ( 0j ) :
		if type ( v ) == type ( 0 ) or type ( v ) == type ( 0L ) or type ( v ) == type ( 0j ) or type ( v ) == type ( 0.0 ) :
		    t[ "value" ] = t[ "value" ] + complex ( v )
		else :
		    t[ "value" ] = t[ "value" ] + 1j
	    elif self.type ( c ) == type ( v ) :
		t[ "value" ] = v
	    else :
		print "Improper type", type ( v ), "for keyletter", c

    def setargs ( self, list ) :
	for i in list :
	    if type ( i ) == type ( ( ) ) :
		if len ( i ) > 4 :
		    self.additem ( i[ 0 ], i[ 1 ], i[ 2 ], i[ 3 ], i[ 4 ] )
		elif len ( i ) > 3 :
		    self.additem ( i[ 0 ], i[ 1 ], i[ 2 ], i[ 3 ] )
		else :
		    self.additem ( i[ 0 ], i[ 1 ], i[ 2 ] )

    def matchlongarg ( self, m ) :
	k = self.keys ( )
	kl = [ ]
	ms = 0
	tl = 0
	il = None
	ss = None
	subarg = None
	for j in k :
	    eq = string.find ( m, self.argeq )
	    if eq > 0 :
		ss = m[ : eq ]
		subarg = m[ eq + 1 : ]
	    else :
		ss = m
	    r = string.find ( j, ss )
	    if r == 0 :			# Only looking for matches at beginning. ...
		kl.append ( j )
		ms = ms + 1


#	print kl
	if ms == 1 :
	    if subarg :
		return ( kl[ 0 ], subarg )
	    else :
		return kl[ 0 ]
	elif ms > 1 :
	    for ll in kl :
		if m == ll :		# We look first for an exact match. ...
		    il = ll
		    break
	    else :			# Otherwise, look for the *longest* possible match. ...
		for ll in kl :
		    if len ( ll ) > tl :
			tl = len ( ll )
			il = ll
	    if il != None :
		if subarg :
		    return ( il, subarg )
		else :
		    return il
	return None

    def getargs ( self, argv ) :
	pn = argv[ 0 ]
	argv = argv[ 1 : ]
	n = len ( argv )
	contflag = 0
	if n > 0 :
	    for i in argv :
		if contflag :
		    contflag = contflag - 1
		    continue
		if i[ 0 ] == self.switch :
#
# -----------Long Arguments--------------------------------------------------------------------
#
#  Allows either '-longarg value' OR '-longarg=value'.
		    if self.longest ( ) > 1 :
			subarg = None
			myi = i[ 1 : ]
			txa = self.matchlongarg ( myi )
			if txa and type ( txa ) == type ( ( ) ) :
			    let = txa[ 0 ]
			    subarg = txa[ 1 ]
			else :
			    let = txa
			if let :
			    t = self.args[ let ]

# -----------Boolean---------------------------------------------------------------------------
			    if self.type ( let ) == type ( None ) :
			        self.setvalue ( let, 1 )
			    elif self.type ( let ) == type ( 0j ) :
				print "Long argument can't do autoincrementing; keyword %s, type %s" % ( let, self.type ( let ) )
# -----------Integer---------------------------------------------------------------------------
			    elif self.type ( let ) == type ( 0 ) :
				if subarg :
				    i = subarg
				else :
				    argv = argv[ 1 : ]
				    if argv :
					i = argv[ 0 ]
				    else :
					i = None
				if i and isnumber ( i ) :
				    tv = string.atoi ( i )
				    self.setvalue ( let, tv )
				    if not subarg :
					argv = argv[ 1 : ]
					if argv and argv[ 0 ] :
					    i = argv[ 0 ]
					else :
					    i = None
					contflag = 1
				else :
				    print "Missing value for keyword %s, type %s" % ( let, self.type ( let ) )
# -----------Long------------------------------------------------------------------------------
			    elif self.type ( let ) == type ( 0L ) :
				if subarg :
				    i = subarg
				else :
				    argv = argv[ 1 : ]
				    if argv :
					i = argv[ 0 ]
				    else :
					i = None
				if i and islong ( i ) :
				    if string.rfind ( i, 'L' ) :
					t = i[ : -1 ]
				    else :
					t = i
				    tv = string.atol ( t )
				    self.setvalue ( let, tv )
				    if not subarg :
					argv = argv[ 1 : ]
					if argv and argv[ 0 ] :
					    i = argv[ 0 ]
					else :
					    i = None
					contflag = 1
				else :
				    print "Missing value for keyword %s, type %s" % ( let, self.type ( let ) )
# -----------Float-----------------------------------------------------------------------------
			    elif self.type ( let ) == type ( 0.0 ) :
				if subarg :
				    i = subarg
				else :
				    argv = argv[ 1 : ]
				    if argv :
					i = argv[ 0 ]
				    else :
					i = None
				if i and isfloat ( i ) :
				    tv = string.atof ( i )
				    self.setvalue ( let, tv )
				    if not subarg :
					argv = argv[ 1 : ]
					if argv and argv[ 0 ] :
					    i = argv[ 0 ]
					else :
					    i = None
					contflag = 1
				else :
				    print "Missing value for keyword %s, type %s" % ( let, self.type ( let ) )
# -----------String----------------------------------------------------------------------------
			    elif self.type ( let ) == type ( "" ) :
				if subarg :
				    i = subarg
				else :
				    argv = argv[ 1 : ]
				    if argv :
					i = argv[ 0 ]
				    else :
					i = None
				if i :
				    self.setvalue ( let, i )
				    if not subarg :
					argv = argv[ 1 : ]
					if argv and argv[ 0 ] :
					    i = argv[ 0 ]
					else :
					    i = None
					contflag = 1
				else :
				    print "Missing value for keyword %s, type %s" % ( let, self.type ( let ) )
# -----------File------------------------------------------------------------------------------
			    elif self.type ( let ) == type ( nofile ) :
				if subarg :
				    i = subarg
				else :
				    argv = argv[ 1 : ]
				    if argv :
					i = argv[ 0 ]
				    else :
					i = None
				if i :
				    self.setvalue ( let, i ) # Store the filename
				    if not subarg :
					argv = argv[ 1 : ]
					if argv :
					    i = argv[ 0 ]
					else :
					    i = None
					contflag = 1
				else :
				    print "Missing value for keyword %s, type %s" % ( let, self.type ( let ) )
# -----------Lists-----------------------------------------------------------------------------
			    elif self.type ( let ) == type ( [ ] ) :
				if subarg :
				    i = subarg
				else :
				    argv = argv[ 1 : ]
				    if argv :
					i = argv[ 0 ]
				    else :
					i = None
				if i :
				    tlist = string.splitfields ( i, self.sep )
				    self.setvalue ( let, tlist ) # Store the list
				    if not subarg :
					argv = argv[ 1 : ]
					if argv :
					    i = argv[ 0 ]
					else :
					    i = None
					contflag = 1
				else :
				    print "Missing value for keyword %s, type %s" % ( let, self.type ( let ) )
# -----------Tuples----------------------------------------------------------------------------
			    elif self.type ( let ) == type ( ( ) ) :
				if subarg :
				    i = subarg
				else :
				    argv = argv[ 1 : ]
				    if argv :
					i = argv[ 0 ]
				    else :
					i = None
				if i :
				    tlist = tuple ( string.splitfields ( i, self.sep ) )
				    self.setvalue ( let, tlist ) # Store the tuple
				    if not subarg :
					argv = argv[ 1 : ]
					if argv :
					    i = argv[ 0 ]
					else :
					    i = None
					contflag = 1
				else :
				    print "Missing value for keyword %s, type %s" % ( let, self.type ( let ) )
# -----------Functions-------------------------------------------------------------------------
			    elif self.type ( let ) == type ( nofunc ) :
				mfc = self.value ( let )
				if mfc :
				    mfc ( let )
			else :
			    print "Unlisted keyword %s" % ( myi )







# -----------Single-letter Arguments-----------------------------------------------------------
		    else :
			j = 1
			for c in i[ 1 : ] :
			    if contflag :
				break
			    if self.has_key ( c ) :

#
# -----------Keyletter Arguments---------------------------------------------------------------
#
# -----------Boolean---------------------------------------------------------------------------
				if self.type ( c ) == type ( None ) :
				    self.setvalue ( c, 1 )
				elif self.type ( c ) == type ( 0j ) :
				    self.setvalue ( c, 1 )

# -----------Integer---------------------------------------------------------------------------
				elif self.type ( c ) == type ( 0 ) :
				    rs = i[ j + 1 : ]	    # Allow for keyletter itself
				    if len ( rs ) > 0 :
					tv = string.atoi ( rs )
					self.setvalue ( c, tv )
					break
				    else :
					argv = argv[ 1 : ]
					i = argv[ 0 ]
					if i and isnumber ( i ) :
					    tv = string.atoi ( i )
					    self.setvalue ( c, tv )
					    argv = argv[ 1 : ]
					    if argv and argv[ 0 ] :
						i = argv[ 0 ]
					    else :
						i = None
					    contflag = 1
					    break
					else :
					    print "Missing value for keyletter %s, type %s" % ( c, self.type ( c ) )

# -----------Long------------------------------------------------------------------------------
				elif self.type ( c ) == type ( 0L ) :
				    rs = i[ j + 1 : ]	    # Allow for keyletter itself
				    if len ( rs ) > 0 :
					tv = string.atol ( rs )
					self.setvalue ( c, tv )
					break
				    else :
					argv = argv[ 1 : ]
					i = argv[ 0 ]
					if i and islong ( i ) :
					    if string.rfind ( i, 'L' ) :
						t = i[ : -1 ]
					    else :
						t = i
					    tv = string.atol ( t )
					    self.setvalue ( c, tv )
					    argv = argv[ 1 : ]
					    if argv and argv[ 0 ] :
						i = argv[ 0 ]
					    else :
						i = None
					    contflag = 1
					    break
					else :
					    print "Missing value for keyletter %s, type %s" % ( c, self.type ( c ) )

# -----------Float-----------------------------------------------------------------------------
				elif self.type ( c ) == type ( 0.0 ) :
				    rs = i[ j + 1 : ]	    # Allow for keyletter itself
				    if len ( rs ) > 0 :
					tv = string.atof ( rs )
					self.setvalue ( c, tv )
					break
				    else :
					argv = argv[ 1 : ]
					i = argv[ 0 ]
					if i and isfloat ( i ) :
					    tv = string.atof ( i )
					    self.setvalue ( c, tv )
					    argv = argv[ 1 : ]
					    if argv and argv[ 0 ] :
						i = argv[ 0 ]
					    else :
						i = None
					    contflag = 1
					    break
					else :
					    print "Missing value for keyletter %s, type %s" % ( c, self.type ( c ) )

# -----------String----------------------------------------------------------------------------
				elif self.type ( c ) == type ( "" ) :
				    rs = i[ j + 1 : ]	    # Allow for keyletter itself
				    if len ( rs ) > 0 :
					self.setvalue ( c, rs )
					break
				    else :
					argv = argv[ 1 : ]
					i = argv[ 0 ]
					if i :
					    self.setvalue ( c, i )
					    argv = argv[ 1 : ]
					    if argv and argv[ 0 ] :
						i = argv[ 0 ]
					    else :
						i = None
					    contflag = 1
					    break
					else :
					    print "Missing value for keyletter %s, type %s" % ( c, self.type ( c ) )

# -----------File------------------------------------------------------------------------------
				elif self.type ( c ) == type ( nofile ) :
				    rs = i[ j + 1 : ]	    # Allow for keyletter itself
				    if len ( rs ) > 0 :
					self.setvalue ( c, rs ) # Store the filename
					break
				    else :
					argv = argv[ 1 : ]
					i = argv[ 0 ]
					if i :
					    self.setvalue ( c, i ) # Store the filename
					    argv = argv[ 1 : ]
					    if argv :
						i = argv[ 0 ]
					    else :
						pass
					    contflag = 1
					    break
					else :
					    print "Missing value for keyletter %s, type %s" % ( c, self.type ( c ) )

# -----------Lists-----------------------------------------------------------------------------
				elif self.type ( c ) == type ( [ ] ) :
				    rs = i[ j + 1 : ]	    # Allow for keyletter itself
				    if len ( rs ) > 0 :
					tlist = string.splitfields ( rs, self.sep )
					self.setvalue ( c, tlist ) # Store the list
					break
				    else :
					argv = argv[ 1 : ]
					i = argv[ 0 ]
					if i :
					    tlist = string.splitfields ( i, self.sep )
					    self.setvalue ( c, tlist ) # Store the list
					    argv = argv[ 1 : ]
					    if argv :
						i = argv[ 0 ]
					    else :
						pass
					    contflag = 1
					    break
					else :
					    print "Missing value for keyletter %s, type %s" % ( c, self.type ( c ) )

# -----------Tuples----------------------------------------------------------------------------
				elif self.type ( c ) == type ( ( ) ) :
				    rs = i[ j + 1 : ]	    # Allow for keyletter itself
				    if len ( rs ) > 0 :
					tlist = tuple ( string.splitfields ( rs, self.sep ) )
					self.setvalue ( c, tlist ) # Store the tuple
					break
				    else :
					argv = argv[ 1 : ]
					i = argv[ 0 ]
					if i :
					    tlist = tuple ( string.splitfields ( i, self.sep ) )
					    self.setvalue ( c, tlist ) # Store the tuple
					    argv = argv[ 1 : ]
					    if argv :
						i = argv[ 0 ]
					    else :
						pass
					    contflag = 1
					    break
					else :
					    print "Missing value for keyletter %s, type %s" % ( c, self.type ( c ) )

# -----------Functions-------------------------------------------------------------------------
				elif self.type ( c ) == type ( nofunc ) :
				    mfc = self.value ( c )
				    if mfc :
					mfc ( c )
			    else :
				print "Unlisted keyletter %s" % ( c )
			    j = j + 1

		    if contflag :
			continue
		    argv = argv[ 1 : ]
		else :
		    break
	return pn, argv

def manpage ( ) :
    return __doc__

if __name__ == "__main__" :
    def printversion ( l ) :
	print "Version 1.%s" % ( l )
    def Printversion ( l ) :
	print "Version %s" % ( VERSION )

    arglist = (
	( 'g', None, "Gregorian style", 1 ),	# Boolean
	( 'j', None, "Julian style", 0 ),		# Boolean
	( 'y', None, "Print full year", 0 ),	# Boolean
	( '0', None, "Print first quarter of year", 0 ),	# Boolean
	( '1', None, "Print second quarter of year", 0 ),	# Boolean
	( '2', None, "Print third quarter of year", 0 ),	# Boolean
	( '3', None, "Print fourth quarter of year", 0 ),	# Boolean
	( 'i', 0j,   "Increment me", 0 ),	# Autoincrementer
	( 'c', 0,    "Changeover", 1582 ),	# Integer
	( 'L', 0L,    "Changeover", 1752L ),	# Long
	( 'F', 0.0,    "Float v", 3.14159 ),	# Float
	( 's', "",    "String v", "I'm a little teapot" ),	# String
	( 'f', nofile,    "File v", "/tmp/dogshit", "wb" ),	# File
	( 'a', [ ],    "List v", ( 'baa', 'baa', 'baa' ) ),	# List
	( 't', ( ),    "Tuple v", ( 'fee', 'fie', 'foe', 'fum' ) ),	# Tuple
	( 'v', nofunc,    "Function (print version)", printversion ),	# Function
	( 'V', nofunc,    "Function (print getsargs version)", Printversion ),	# Function

	)
    xarg = arguments ( '/', arglist )
    xarg.setsep ( ',' )
    print "sep is", xarg.sep
    progname, sys.argv = xarg.getargs ( sys.argv )
    if len ( sys.argv ) > 0 :
	print "Arguments left:", len ( sys.argv ), sys.argv
    else :
	print "Usage:", progname, "<options> <month> <year>\n", xarg

    x = xarg.keys ( )
    fp = xarg.open ( 'f' )
    oldstdout = sys.stdout
    sys.stdout = fp
    for i in x :
	t = xarg.value ( i )
	if xarg.file ( i ) :
	    print i, "value is", xarg.file ( i )
	else :
	    print i, "value is", t
    sys.stdout = oldstdout
    print type ( nofile )

    xarg = 0

