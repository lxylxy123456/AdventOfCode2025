import argparse, math, sys, re, functools, operator, itertools, heapq
from collections import defaultdict, Counter, deque
#sys.setrecursionlimit(100000000)
#A = list(map(int, input().split()))
#T = int(input())

def read_lines(f):
	while True:
		line = f.readline()
		if not line:
			break
		assert line[-1] == '\n'
		yield line[:-1]

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-1', '--one', action='store_true', help='Only part 1')
	parser.add_argument('-2', '--two', action='store_true', help='Only part 2')
	parser.add_argument('input_file', nargs='?')
	args = parser.parse_args()
	if args.input_file is not None:
		f = open(args.input_file)
	else:
		f = sys.stdin
	lines = list(read_lines(f))
	if not args.two:
		print(part_1(lines))
	if not args.one:
		print(part_2(lines))

def part_1(lines):
	s = 0
	questions = []
	for i in lines[0].split():
		questions.append([])
	for i in lines:
		for index, j in enumerate(i.split()):
			questions[index].append(j)
	for i in questions:
		if i[-1] == '*':
			o = operator.mul
		elif i[-1] == '+':
			o = operator.add
		else:
			raise Exception
		s += functools.reduce(o, map(int, i[:-1]))
	return s

def part_2(lines):
	s = 0
	op = None
	q = []
	def y():
		nonlocal op, q, s
		if op is None:
			assert not q
			return
		if op == '*':
			o = operator.mul
		elif op == '+':
			o = operator.add
		s += functools.reduce(o, map(int, filter(str.strip, q)))
		q.clear()
	for i in range(len(lines[-1])):
		if lines[-1][i] == ' ':
			pass
		elif lines[-1][i] in ('+', '*'):
			y()
			op = lines[-1][i]
		else:
			raise Exception
		q.append(''.join(map(lambda x: x[i], lines[:-1])))
	y()
		

	return s

if __name__ == '__main__':
	main()

