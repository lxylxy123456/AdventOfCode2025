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
	a = 50
	for i in lines:
		d = i[0]
		l = int(i[1:])
		if d == 'L':
			x = -l
		elif d == 'R':
			x = l
		else:
			assert 0
		a += x
		a %= 100
		s += (a == 0)
	return s

def part_2_brute_force(lines):
	s = 0
	a = 50
	for i in lines:
		d = i[0]
		l = int(i[1:])
		for i in range(l):
			if d == 'L':
				a -= 1
			elif d == 'R':
				a += 1
			else:
				assert 0
			a %= 100
			if a == 0:
				s += 1
	return s

def part_2(lines):
	s = 0
	a = 50
	for i in lines:
		d = i[0]
		l = int(i[1:])
		if d == 'L':
			x = -l
		elif d == 'R':
			x = l
		else:
			assert 0
		if a == 0 and d == 'L':
			a = 100
		a += x
		#print(i, a, (a // 100), a % 100, sep='\t')
		s += abs(a // 100)
		a %= 100
		if a == 0 and d == 'L':
			s += 1
	assert s == part_2_brute_force(lines)
	return s

if __name__ == '__main__':
	main()

