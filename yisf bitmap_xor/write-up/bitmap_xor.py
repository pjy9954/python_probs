# -*- coding:utf-8 -*-
import sys

target_name = 'target.bmp'
out_name = 'out.bmp'
add_name = 'add.bmp'

try:
	target = open(target_name, 'rb')
	add = open(add_name, 'rb')
	output = open(out_name, 'wb')
	sig = target.read(2)
	if sig != 'BM':
		print 'this is Not Bitmap file.'
		exit(1)
	else:
		target.seek(0)
		add.seek(0x36)
	t = target.read(0x36)
	output.write(t)
	while True:
		t = target.read(1)
		a = add.read(1)
		if t == '':
			break
		txa = chr( ~(ord(t) ^ ord(a)) & 0xff )
#		nott = chr( ~ord(t) & 0xff )
#		output.write(nott)
		output.write(txa)

	target.close()
	add.close()
	output.close()
except IOError:
	print >> sys.stderr, 'File open error'