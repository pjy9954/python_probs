#!/usr/bin/env python
#
# sha1 padding/length extension attack
# by rd@vnsecurity.net
#

import sys
import base64
from shaext import shaext

if len(sys.argv) != 4:
	print "usage: %s <keylen> <original_signature> <text_to_append>"  % sys.argv[0]
	exit(0)
	
keylen = int(sys.argv[1])
orig_msg = ''#sys.argv[2]
orig_sig = sys.argv[2]
add_msg = sys.argv[3]

ext = shaext(orig_msg, keylen, orig_sig)
ext.add(add_msg)

(new_msg, new_sig)= ext.final()
		
print "new msg: " + repr(new_msg).replace("\\x", '%')
#print "base64: " + base64.b64encode(new_msg)
print "new sig: " + new_sig
