# -*- coding:utf-8 -*-
import sys

original_name = 'origin.bmp'
out_name = 'out.bmp'
diff_name = 'diff.bmp'

try:
	origin = open(original_name, 'rb')
	diff = open(diff_name, 'rb')
	out = open(out_name, 'wb')

	diff.seek(0x36)
	o = origin.read(0x36)
	out.write(o)
	while True:
		o = origin.read(1)
		d = diff.read(1)
		if o == '':
			break
		oxd = chr( (ord(o) ^ ord(d)) & 0xff )
#		oxd = chr( ord(o) | ord(d) & 0xff )
		out.write(oxd)

	origin.close()
	diff.close()
	out.close()
except IOError:
	print >> sys.stderr, 'File open error'