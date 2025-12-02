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
	for i in ''.join(lines).split(','):
		a, b = map(int, re.fullmatch('([1-9]\d*)-([1-9]\d*)', i).groups())
		assert a < b
		for j in range(a, b + 1):
			jj = str(j)
			l = len(jj)
			if l % 2 == 0 and jj == jj[:l // 2] * 2:
				s += j
	return s

def part_2(lines):
	s = 0
	for i in ''.join(lines).split(','):
		a, b = map(int, re.fullmatch('([1-9]\d*)-([1-9]\d*)', i).groups())
		assert a < b
		for j in range(a, b + 1):
			jj = str(j)
			l = len(jj)
			for k in range(2, l + 1):
				if l % k == 0 and jj == jj[:l // k] * k:
					s += j
					break
	return s

if __name__ == '__main__':
	main()

