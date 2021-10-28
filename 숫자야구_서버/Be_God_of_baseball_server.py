# -*- coding:utf-8 -*-
import socket
from time import time
from SocketServer import ThreadingTCPServer, StreamRequestHandler
from random import randint

#입력값 판단용(숫자만 입력토록)
def isNumber(s):
  try:
	float(s)
	return True
  except ValueError:
	return False

#힌트출력
def Print_Hint(conn, baseball_key):
	tellnumber = randint(1,3)
	flag_no=[0,0,0]
	while tellnumber != 0:
		randnum = randint(0,2)
		if flag_no[randnum] == 0:
			flag_no[randnum] = 1
			tellnumber=tellnumber-1

	result=''
	for i in range(3):
		if flag_no[i] == 1:
			result = result+baseball_key[i]
		else:
			result = result+'X'
	conn.send('God of baseball : Get my ORACLE! Answer Is '+result+'\n')

#strike, ball 판단 및 출력함수
def Print_XsXb(conn, user_input, baseball_key):
	s=0
	b=0
	for i in range(3):
		if user_input[i] in baseball_key:
			if user_input[i] == baseball_key[i]:
				s=s+1
			else: 
				b=b+1
	conn.send('%dStrike %dBall\n' % (s,b))
	if s == 3:
		return 1
	else:
		return 0

#정답 생성부분. 랜덤값의 3자리로 결정
def Gen_key():
	baseball_key=''
	while len(baseball_key) < 3:
		a = randint(0,9)
		a=str(a)
		if a not in baseball_key:
			baseball_key=baseball_key+a
	return baseball_key

#소켓서버부분
class MyRequestHandler(StreamRequestHandler):
	def handle(self):
		prob_key = '0H_Y0U_4R3_G0D_0F_B453B411!?UNB3L13V4BL3!!'	#문제 인증키
		baseball_key = ''	#숫자야구 정답
		wincount = 0	#승리 카운트
		hintcount = 2	#힌트 카운트
		exitflag = 0	#종료플래그
		winstr = ['First', 'Double', 'Triple', 'Quadra', 'Penta']	#승리시 출력문

		print 'connection from' ,self.client_address
		conn = self.request

		conn.send('*+*:*+*:*+*:*+*:*+*:*+*:*+*:*+*\n')
		conn.send('*+*: Number Baseball Game! :*+*\n')
		conn.send('*+*:*+*:*+*:*+*:*+*:*+*:*+*:*+*\n')
		conn.send('\nInfo : Range of number is 0~9\n')
		conn.send('Goal : Penta Win!\n\n')
		conn.send('If you want got Hint of Answer , input HINT\n')
		conn.send('Remains of HINT : %d\n' % hintcount)

		#메인루프
		for round in range(5):	#총 5번의 라운드
			baseball_key = Gen_key()	#baseball_key 생성 
			conn.send('\n*** %d Round Start. Good Luck ***\n' % (round+1))

			#라운드 시작부분 한 라운드에는 총 5번의 기회가 있음
			i=0
			while i != 5:	
				#사용자안내문 출력
				conn.send('\ninput your number (take %d/5, %d round)\n' % (i+1, round+1))
				conn.send('input>>')
				start_time = int(time())
				try:
					user_input = conn.recv(1024)
					end_time = int(time())
				except :
					print 'error'
					conn.close
					print self.client_address, 'disconnected'
					exitflag = 1
					break
				
				#타임아웃일경우 연결종료
				if end_time - start_time > 1:
					print self.client_address, 'Timeout'
					conn.send('You are So Lazy! \nTime Out. Disconnect\n')
					exitflag = 1
					break

				#유저 입력이없으면 (Ctrl+C 등) 연결종료
				if not user_input:
					conn.close()
					print self.client_address, 'disconnected'
					exitflag = 1
					break

				print self.client_address, user_input	#유저 입력값 보기

				#입력값 끝에 \n가 있을경우 삭제
				if user_input[len(user_input)-1] == '\n':
					user_input = user_input.rstrip('\n')

				#유저 입력값 검증(잘못된 값일경우 disconnect)
				if len(user_input) != 3 or not isNumber(user_input):
					if user_input == 'HINT':
						if hintcount != 0:
							Print_Hint(conn, baseball_key)	#힌트함수 호출
							hintcount=hintcount-1
							conn.send('\nRemains of HINT : %d\n' % hintcount)
						else:
							conn.send('No more HINT.. Sorry.\bDisconnect\n')
							conn.close()
							print self.client_address, 'disconnected'
							exitflag = 1
							break
						continue
					else:
						conn.send('Wrong Input.\nU Must Input 3Number (ex. 451)\nDisconnect\n')
						conn.close()
						print self.client_address, 'disconnected'
						exitflag = 1
						break
				elif Print_XsXb(conn, user_input, baseball_key):	#XsXb 함수 호출
					wincount=wincount+1
					break
				i=i+1
			#라운드 종료
			if exitflag == 1:
				break
			conn.send('\n*** %d Round End. ***\n' % (round+1))
			if wincount != round+1:	#승리하지 못할경우 게임종료
				conn.send('Oh... You Failed\nDisconnect\n')
				conn.close()
				print self.client_address, 'disconnected'
				break
			else:
				conn.send('%s Win!\n\n' % winstr[wincount-1])
		
		#5번의 라운드를 모두 승리했을경우 키 표시
		if wincount == 5:
			conn.send('GreatJob! Key is '+prob_key+'\n')
			print self.client_address, 'Get Authkey. disconnected'
		conn.close()

if __name__ == '__main__':
	PORT = 3389
	server = ThreadingTCPServer( ('', PORT),MyRequestHandler)
	print 'listening on port', PORT
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		print "Server close"