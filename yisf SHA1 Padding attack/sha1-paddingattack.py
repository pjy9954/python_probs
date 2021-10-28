from hashlib import sha256
from hashlib import sha1
import struct

#### original sha1 ####

#SHA tr functions
def f0_19(B, C, D):
    return (B & C) | ((~ B) & D)

def f20_39(B, C, D):
    return B ^ C ^ D

def f40_59(B, C, D):
    return (B & C) | (B & D) | (C & D)

def f60_79(B, C, D):
    return B ^ C ^ D

#Rotate Left Function
def _rotateLeft(x, n):
    "Rotate x (32 bit) left n bits circularly."

    return (x << n) | (x >> (32-n))

#Text To Long
def TTL(txt):
	Out=0
	for i in txt:
		Out = _rotateLeft(Out, 8)
		Out+=ord(i)
	return Out

#Generate W[0~79]
def GenW(txt):
	W=[]
	for i in range(16):
		W.append(TTL(txt[i*4:(i+1)*4]))
	for i in range(16,80):
		W.append( _rotateLeft(W[i-16]^W[i-14]^W[i-8]^W[i-3], 1) & 0xffffffffL)
	return W

#Generate digest 
def GenDigest(H):
	digest = 0
	for i in range(5):
		digest = (digest << 32) + H[i]
	return digest

#Generate HexDigest
def GenHexDigest(digest):
	HD=''
	temp = digest
	while temp!=0:
		HD = '%02x' % (temp%0x100) + HD
		temp=temp/0x100
	return HD

#Message Padding Func
def paddMsg(imsg, clen=0):
	if clen == 0:
		msglen = len(imsg)*8
	else:
		paddlen = 512 - (clen*8)%512
		msglen = len(imsg)*8 + paddlen + clen*8
	paddlen = 512 - msglen%512	#total padding length
	zpaddlen = paddlen-8-64		#zero padding length
	if zpaddlen < 0:
		zpaddlen+=512
	paddend = ''				#padding msglen
	count=0
	temp = msglen
	while temp != 0:
		paddend=chr(temp%0x100) + paddend
		temp = temp/0x100
		count+=1

	return imsg + '\x80' + '\00'*((zpaddlen/8) + 8-count) + paddend

#Text to Hex Print (Just for Debug)
def TTH (txt):
	for i in range(len(txt)):
		if i%64 == 0 and i!=0:
			print '\n\n%02X' % (ord(txt[i])),
		elif i%16 == 0 and i!=0:
			print '\n%02X' % (ord(txt[i])),
		elif i%8 == 0 and i!=0:
			print ' %02X' % (ord(txt[i])),
		else:
			print '%02X' % (ord(txt[i])),
	print

#Const of SHA
maxlen = 0xffffffffffffffff

K = [
    0x5A827999L, # ( 0 <= t <= 19)
    0x6ED9EBA1L, # (20 <= t <= 39)
    0x8F1BBCDCL, # (40 <= t <= 59)
    0xCA62C1D6L  # (60 <= t <= 79)
    ]

H = [
	0x67452301L,
	0xEFCDAB89L,
	0x98BADCFEL,
	0x10325476L,
	0xC3D2E1F0L
	]

###end of Def

imsg = 'abcdccddabcdccdd'	#user Input
print sha1(imsg).hexdigest()

msglen = len(imsg)*8
if msglen > maxlen:
	print 'input range over'
	exit(1)

txt = paddMsg(imsg)	#padding

blockCount = len(txt)/64

for i in range(blockCount):
	A = H[0]
	B = H[1]
	C = H[2]
	D = H[3]
	E = H[4]

	TEMP = 0

	W=GenW( txt[i*64:(i+1)*64] )

	for t in range(80):
		if 0 <= t and t <= 19:
			TEMP = _rotateLeft(A, 5) + f0_19(B,C,D) + E + W[t] + K[0]
			E = D
			D = C
			C = _rotateLeft(B, 30) & 0xffffffffL
			B = A
			A = TEMP & 0xffffffffL
		if 20 <= t and t <= 39:
			TEMP = _rotateLeft(A, 5) + f20_39(B,C,D) + E + W[t] + K[1]
			E = D
			D = C
			C = _rotateLeft(B, 30) & 0xffffffffL
			B = A
			A = TEMP & 0xffffffffL
		if 40 <= t and t <= 59:
			TEMP = _rotateLeft(A, 5) + f40_59(B,C,D) + E + W[t] + K[2]
			E = D
			D = C
			C = _rotateLeft(B, 30) & 0xffffffffL
			B = A
			A = TEMP & 0xffffffffL
		if 60 <= t and t <= 79:
			TEMP = _rotateLeft(A, 5) + f60_79(B,C,D) + E + W[t] + K[3]
			E = D
			D = C
			C = _rotateLeft(B, 30) & 0xffffffffL
			B = A
			A = TEMP & 0xffffffffL

	H[0] = H[0] + A & 0xffffffffL
	H[1] = H[1] + B & 0xffffffffL
	H[2] = H[2] + C & 0xffffffffL
	H[3] = H[3] + D & 0xffffffffL
	H[4] = H[4] + E & 0xffffffffL

digest = GenDigest(H)
HexDigest = GenHexDigest(digest)

#print HexDigest

###SHA1 padding attack 

#user Input start
imsg = 'admin'		#user's additional msg
olen = 13			#original messege length
osig = '7fdb7a162e4176607403b239a9d3fc75f57b5676'	#original message digest
#user Input end

#Gen New Message start

omsglen = olen*8
paddlen = 512 - omsglen%512
zpaddlen = paddlen-8-64

if zpaddlen < 0:
	zpaddlen+=512

paddend = ''
count=0
temp = omsglen 
while temp!=0:
	paddend=chr(temp%0x100) + paddend
	temp = temp/0x100
	count+=1

genmsg = '\x80' + '\x00'*((zpaddlen/8) + 8-count)+ paddend + imsg
hgenmsg = ''
for i in range(paddlen/8):
	hgenmsg = hgenmsg + '%%%02x' % ord(genmsg[i])
hgenmsg+=imsg

print 'Ext msg : '+hgenmsg
#Gen New Message end

#Gen New Digest
txt = paddMsg(imsg, olen)
#TTH(txt)

temp = int(osig, 16)
H[0] = temp >> 32*4 & 0xffffffffL
H[1] = temp >> 32*3 & 0xffffffffL
H[2] = temp >> 32*2 & 0xffffffffL
H[3] = temp >> 32*1 & 0xffffffffL
H[4] = temp & 0xffffffffL

for i in range(blockCount):
	A = H[0]
	B = H[1]
	C = H[2]
	D = H[3]
	E = H[4]

	TEMP = 0

	W=GenW( txt[i*64:(i+1)*64] )

	for t in range(80):
		if 0 <= t and t <= 19:
			TEMP = _rotateLeft(A, 5) + f0_19(B,C,D) + E + W[t] + K[0]
			E = D
			D = C
			C = _rotateLeft(B, 30) & 0xffffffffL
			B = A
			A = TEMP & 0xffffffffL
		if 20 <= t and t <= 39:
			TEMP = _rotateLeft(A, 5) + f20_39(B,C,D) + E + W[t] + K[1]
			E = D
			D = C
			C = _rotateLeft(B, 30) & 0xffffffffL
			B = A
			A = TEMP & 0xffffffffL
		if 40 <= t and t <= 59:
			TEMP = _rotateLeft(A, 5) + f40_59(B,C,D) + E + W[t] + K[2]
			E = D
			D = C
			C = _rotateLeft(B, 30) & 0xffffffffL
			B = A
			A = TEMP & 0xffffffffL
		if 60 <= t and t <= 79:
			TEMP = _rotateLeft(A, 5) + f60_79(B,C,D) + E + W[t] + K[3]
			E = D
			D = C
			C = _rotateLeft(B, 30) & 0xffffffffL
			B = A
			A = TEMP & 0xffffffffL

	H[0] = H[0] + A & 0xffffffffL
	H[1] = H[1] + B & 0xffffffffL
	H[2] = H[2] + C & 0xffffffffL
	H[3] = H[3] + D & 0xffffffffL
	H[4] = H[4] + E & 0xffffffffL

digest = GenDigest(H)
HexDigest = GenHexDigest(digest)
print 'New Digest : '+HexDigest