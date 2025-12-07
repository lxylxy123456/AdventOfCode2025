# Youtube: https://youtu.be/mgtnIJb2N6k

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
	cur = [lines[0].index('S')]
	for i in lines[1:]:
		n = set()
		for j in cur:
			if i[j] == '^':
				assert j > 0 and j < len(i) - 1
				n.add(j - 1)
				n.add(j + 1)
				s += 1
			else:
				n.add(j)
		cur = list(n)
	return s

def part_2(lines):
	s = 0
	cur = {lines[0].index('S'): 1}
	for i in lines[1:]:
		n = defaultdict(int)
		for j, v in cur.items():
			if i[j] == '^':
				assert j > 0 and j < len(i) - 1
				n[j - 1] += v
				n[j + 1] += v
				s += 1
			else:
				n[j] += v
		cur = n
	return sum(cur.values())

if __name__ == '__main__':
	main()

