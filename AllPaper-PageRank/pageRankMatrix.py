#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import math

################################  计算相似矩阵  ####################################

###  计算TFISF  ###################
def calTFISF(norMatrix):
	totalRow = len(norMatrix)
	totalCol = len(norMatrix[0])
	sentNum = 0
	wordVector = np.zeros(totalCol) # 初始化每个词在多少句子出现的个数
	tfisfMatrix = np.zeros([len(norMatrix), len(norMatrix[0])])
 
	for row in range(totalRow):
		sentNum = sentNum + 1
		wordCount = 0  # 每行的总词数
		for col in range(totalCol):
 			wordCount = wordCount + norMatrix[row][col]

		for col in range(totalCol):
 			tfisfMatrix[row][col] = float(norMatrix[row][col]) / wordCount  # 计算TF
 			if int(norMatrix[row][col]) != 0:
				wordVector[col] = wordVector[col] + 1  # 计算每个词在多少个句子中出现过
	for i in range(len(wordVector)):
		wordVector[i] = math.log(totalRow / wordVector[i])  # 计算ISF
	tfisfMatrix = tfisfMatrix * wordVector  # 计算TF-ISF

	return tfisfMatrix

###  计算句子之间相似性  #########
def cosSim(sentVector1, sentVector2):
	def numer(sent1, sent2):
		numerSum = 0.0
		for i in range(len(sent1)):
			numerSum = numerSum + sent1[i] * sent2[i]
		return numerSum

	def denom(sent1, sent2):
		denomSum = 0.0
		denomSum1 = 0.0
		denomSum2 = 0.0
		for i in range(len(sent1)):
			denomSum1 = denomSum1 + sent1[i] * sent1[i]
		for i in range(len(sent2)):
			denomSum2 = denomSum2 + sent2[i] * sent2[i]
		denomSum = math.sqrt(denomSum1) * math.sqrt(denomSum2)
		return denomSum

	return numer(sentVector1, sentVector2) / denom(sentVector1, sentVector2)
 

def calSentSim(tfisfMatrix):
	simMatrix = np.zeros([len(tfisfMatrix), len(tfisfMatrix)])
	count = 0
	holdValue = 0.005
	for row in range(len(tfisfMatrix)):
		for otrow in range(len(tfisfMatrix)):
			if row == otrow:
				continue
			sentVector1 = tfisfMatrix[row]
			sentVector2 = tfisfMatrix[otrow]
			simResult = cosSim(sentVector1, sentVector2)
			if simResult > holdValue:
				simMatrix[row][otrow] = simResult
			else:
				simMatrix[row][otrow] = 0

	return simMatrix

###  生成矩阵中间过程  ###########
def midProcess(norMatrix, sentList, wordDict):
	# 建立句子-词矩阵
	sentlocal = 0
	for i in range(len(sentList)):
		line = sentList[i]
		list = line.strip().split()
		for word in list:
			if word in wordDict:
				wordlocal = wordDict[word]
				norMatrix[sentlocal][wordlocal] = norMatrix[sentlocal][wordlocal] + 1
		sentlocal = sentlocal + 1

	# 计算TFISF
	tfisfMatrix = calTFISF(norMatrix)

	# 计算相似性
	simMatrix = calSentSim(tfisfMatrix)

	return simMatrix
###

###  生成矩阵  ###################
def generateMatrix(sentList, stopwordDict):
	sentNum = len(sentList)  # 句子数量
	wordDict = {}

	for i in range(len(sentList)):
		list = sentList[i].strip().split()
		for word in list:
			if word not in wordDict and word not in stopwordDict:
				wordDict[word] = 0

	# 对词进行编号
	i = 0
	for word in wordDict:
		wordDict[word] = i
		i = i + 1

	wordNum = len(wordDict)  # 词数量
	norMatrix = np.zeros([sentNum, wordNum])  # 建立全0矩阵，行：句子，列：词
	simMatrix = midProcess(norMatrix, sentList, wordDict)

	return simMatrix
###

####################################################################################

################################  计算PageRank  ####################################

alpha = 0.85

###  参数与矩阵相乘  ###
def multiGeneMatrix(gene, Matrix):
	mulmatrix = gene * Matrix

	return mulmatrix
###

###  两个矩阵相加  ###
def addMatrix(Matrix1, Matrix2):
	if len(Matrix1) != len(Matrix2):
		print '这两个矩阵无法相加...'
		return

	addmatrix = Matrix1 + Matrix2

	return addmatrix
###

###  矩阵与向量相乘  ###
def multiMatrixVector(m, v):
	rv = np.dot(m, v)

	return rv
###

###  pagerank计算  ###
def pagerankCal(S):  # S：转移矩阵
	E = np.ones([len(S), len(S[0])])  # E矩阵
	f = np.ones(len(S))  # 特征矩阵

	f1 = multiGeneMatrix(alpha, S)
	f2 = multiGeneMatrix((1-alpha)/len(S[0]), E)
	G = addMatrix(f1, f2)  # 计算好的新转移矩阵

	# 迭代过程
	count = 0
	while (True):
		count = count + 1
		pr_next = multiMatrixVector(G, f)
		s = ''
		i = 0
		for i in range(len(pr_next)-1):
			s = s + str(round(pr_next[i], 5)) + '\t'
		s = s + str(round(pr_next[i+1], 5))
		
		#  判断当前向量与上次向量值偏差不大后，停止迭代
		judge = True
		for i in range(len(pr_next)):
			if round(f[i], 5) != round(pr_next[i], 5):
				judge = False
				break
		if judge:
			break

		f = pr_next

	return f
###

###  排序选择前N个句子  ###########
def sortAndselectSent(result, n):
	selectSent = []
	for i in range(n):
		maxscore = -1000
		local = -1
		for j in range(len(result)):
			if result[j] > maxscore:
				maxscore = result[j]
				local = j
		selectSent.append(local)
		result[local] = -1

	return selectSent
###

###  使用PageRank选择前N个句子
def extractModel(simmatrix):
	result = pagerankCal(simmatrix)

	selectRate = 0.3
	sentNum = int(len(result) * selectRate)
	if (len(result)*selectRate) > sentNum:
		sentNum = sentNum + 1
	selectSent = sortAndselectSent(result, sentNum)
	tempResult = sorted(selectSent)

	return tempResult
###

##############################################################################################

def main():
	fileReadPaperSegName = 'part-00000-PaperSeg'  # 分词文章
	fileReadPaperName = 'part-00000-Paper'  # 没分词文章
	fileReadStopName = 'stopwords.txt'  # 停用词表

	fileReadPaperSeg = open(fileReadPaperSegName)
	fileReadPaper = open(fileReadPaperName)
	fileReadStop = open(fileReadStopName)

	fileWriteResultName = fileReadPaperName + 'Result'
	fileWriteResult = open(fileWriteResultName, 'w')

	# 获取停用词表
	stopwordDict = set([])
	for word in fileReadStop.readlines():
		stopwordDict.add(word)
		
	count = 0
	sentSegList = []
	sentList = []
	for line in fileReadPaperSeg.readlines():
		sourceLine = fileReadPaper.readline()
		if line == '-----------------------------------------------------------------\n':
			if count % 1000 == 0:
				print '已经完成', count, '个句子'

			if len(sentSegList) == 1:  # 如果文章只有一个句子，不需要计算，直接输出
				out = '---------------------' + str(count) + '-------------------------\n'
				fileWriteResult.write(out)
				fileWriteResult.write(sentList[0])			
				out = '-----------------------------------------------------------------\n'
				fileWriteResult.write(out)
				sentList = []
				sentSegList = []
				continue

			simMatrix = generateMatrix(sentSegList, stopwordDict)  # 获得相似矩阵
			result = extractModel(simMatrix)


			# 写结果
			out = '---------------------' + str(count) + '-------------------------\n'
			fileWriteResult.write(out)
			for i in range(len(result)):
				fileWriteResult.write(sentList[result[i]])
			out = '-----------------------------------------------------------------\n'
			fileWriteResult.write(out)

			sentList = []
			sentSegList = []
			continue
		elif line[: 8] == '--------':
#			sentList = []
#			while True:
#				sourceLine = fileReadPaper.readline()
#				if sourceLine ==  '-----------------------------------------------------------------\n':
#					break
#				elif sourceLine[: 8] == '--------':
#					continue
#				sentList.append(sourceLine)
			count = count + 1
			continue

		sentSegList.append(line)
		sentList.append(sourceLine)


	fileReadPaper.close()
	fileReadPaperSeg.close()
	fileReadStop.close()
	fileWriteResult.close()

if __name__ == '__main__':
	main()
