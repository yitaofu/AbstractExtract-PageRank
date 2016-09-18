#!/usr/bin/env python
#-*- coding: utf-8 -*-


fileReadName = 'part-00000'
fileWriteName = fileReadName + '-Paper'

fileRead = open(fileReadName)
fileWrite = open(fileWriteName, 'w')

count = 0

for line in fileRead.readlines():
	if count == 100:
		break
	list = line.strip().split('\t')
	if len(list) != 16:
		continue
	paper = list[14]
	tempPaper = paper.replace('null', '').replace('“', '').replace('”', '').replace(' ', '')
	
	paperlist1 = tempPaper.split('。')  # 分'。'
	if len(paperlist1) == 1 and paperlist1[0] == '':
		continue	
	paperlist2 = []
	for i in range(len(paperlist1)):  # 分'！'
		if paperlist1[i] == '':
			continue
		if paperlist1[i][-3: ] != '！' and paperlist1[i][-3: ] != '？':
			paperlist1[i] = paperlist1[i] + '。'
		templist = paperlist1[i].split('！')
		if len(templist) == 1:
			paperlist2.append(templist[0])
		else:
			for j in range(len(templist)-1):
				paperlist2.append(templist[j]+'！')
			paperlist2.append(templist[len(templist)-1])
	paperlist3 = []
	for i in range(len(paperlist2)):  # 分'？'
		templist = paperlist2[i].split('？')
		if len(templist) == 1:
			paperlist3.append(templist[0])
		else:
			for j in range(len(templist)-1):
				paperlist3.append(templist[j]+'？')
			paperlist3.append(templist[len(templist)-1])
	
	if len(paperlist3) == 1 and paperlist3[0] == '':
		continue

	if len(paperlist3) == 0:
		continue

	if len(paperlist3) < 6:  # 超过五句的文本才能抽取
		continue

	count = count + 1
	out = '-----------------------' + str(count) + '--------------------------\n'
	fileWrite.write(out)

	for paperline in paperlist3:
		if paperline == '' or paperline == '，' or paperline == '。' or paperline == '！' or paperline == '？' or paperline == '；' or paperline == '“' or paperline == '”':
			continue

		while True:
			if paperline[0: 3] == '“' or paperline[0: 3] == '”' or paperline[0: 3] == '，':
				paperline = paperline[3:]
			elif paperline[0: 2] == '·':
				paperline = paperline[2:]
			elif paperline[0] == ' ':
				paperline = paperline[1:]
			elif paperline[0: 4] == '  ':
				paperline = paperline[4: ] 
			elif paperline[0: 2] == ' ':
				paperline = paperline[2: ]
			elif paperline[0: 3] == '　':
				paperline = paperline[3: ]
			else:
				break

		if paperline == '' or paperline == '，' or paperline == '。' or paperline == '！' or paperline == '？' or paperline == '；' or paperline == '“' or paperline == '”':
			continue

		paperline = paperline + '\n'
		fileWrite.write(paperline)
	fileWrite.write('-----------------------------------------------------------------\n')

	###  测试  #######################
	if count == 99:
		fileWriteTestName = 'testFile'
		fileWriteTest = open(fileWriteTestName, 'w')
		for paperline in paperlist3:
			paperline = paperline + '\n'
			fileWriteTest.write(paperline)

		fileWriteTest.close()
	##################################

fileRead.close()
fileWrite.close()
