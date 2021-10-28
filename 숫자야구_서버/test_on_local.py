# -*- coding:utf-8 -*-
from random import *
import time 

PORT = 3389
prob_key = '0H_Y0U_4R3_G0D_0F_B453B411!?UNB3L13V4BL3!!'	#문제 인증키
baseball_key = ''	#숫자야구 정답
wincount = 0	#승리 카운트
hintcount = 2	#힌트 카운트

#입력값 판단용(숫자만 입력토록)
def isNumber(s):
  try:
    float(s)
    return True
  except ValueError:
    return False

#힌트출력
def Print_Hint():
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
	print 'God of baseball : Get my ORACLE! Answer Is '+result

#strike, ball 판단 및 출력함수
def Print_XsXb(user_input):
	s=0
	b=0
	for i in range(3):
		if user_input[i] in baseball_key:
			if user_input[i] == baseball_key[i]:
				s=s+1
			else:
				b=b+1
	print '%dStrike %dBall' % (s,b)
	if s == 3:
		return 1
	else:
		return 0

#정답 생성부분. 랜덤값의 3자리로 결정
def Gen_key(baseball_key):
	baseball_key=''
	while len(baseball_key) < 3:
		a = randint(0,9)
		a=str(a)
		if a not in baseball_key:
			baseball_key=baseball_key+a
	return baseball_key

#메인 프로그램
print '*+*:*+*:*+*:*+*:*+*:*+*:*+*:*+*'
print '*+*: Number Baseball Game! :*+*'
print '*+*:*+*:*+*:*+*:*+*:*+*:*+*:*+*'
print '\nInfo : Range of number is 0~9\nGoal : PentaWin\nIf you want got Hint, input HINT\nRemains of HINT : %d' % hintcount

#메인 루프
for round in range(5):	#총 5번의 라운드를 승리해야함
	baseball_key = Gen_key(baseball_key)	
	print '\nYour Winning Count : %d' % wincount
	
	#라운드 시작부분 한 라운드에는 총 5번의 기회가 있음
	i=0
	while i != 5:	
		print '\ninput your number (take %d/5, %d round) ' % (i+1, round+1)
		user_input = raw_input('input>>')
		#유저 입력값 검증(잘못된 값일경우 disconnect
		if len(user_input) != 3 or not isNumber(user_input):
			if user_input == 'HINT':
				if hintcount != 0:
					Print_Hint()
					hintcount=hintcount-1
					print '\nRemains of HINT : %d' % hintcount
				else:
					print 'No more HINT.. Sorry.\bDisconnect'
					exit(1)
				continue
			else:
				print 'Wrong Input.\nU Must Input 3Number (ex. 451)\nDisconnect'
				exit(1)
		elif Print_XsXb(user_input):
			wincount=wincount+1
			print 'Good! You Win!\n'
			break
		i=i+1
	#라운드 종료
	print '\n*** %d Round is End. ***' % (round+1)
	if wincount != round+1:	#승리하지 못할경우 게임종료
		print 'Oh... You Faild\nDisconnect'
		exit(1)

#5번의 라운드를 모두 승리했을경우 키 표시
#print '\nYour Winning Count : %d' % wincount
print 'GreatJob! Key is '+prob_key