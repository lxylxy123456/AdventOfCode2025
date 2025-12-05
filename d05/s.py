# Youtube: https://youtu.be/weU1WTDxCJI

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
	fresh = []
	ilines = iter(lines)
	while True:
		if i := next(ilines):
			fresh.append(tuple(map(int, i.split('-'))))
		else:
			break
	ing = list(map(int, ilines))
	for i in ing:
		for l, r in fresh:
			if l <= i <= r:
				s += 1
				break
	return s

def part_2(lines):
	s = 0
	fresh = []
	ilines = iter(lines)
	while True:
		if i := next(ilines):
			fresh.append(tuple(map(int, i.split('-'))))
		else:
			break
	fresh.sort()
	for l, r in fresh:
		assert l <= r
	while fresh:
		if len(fresh) >= 2:
			if fresh[0][1] >= fresh[1][0]:
				new = (fresh[0][0], max(fresh[0][1], fresh[1][1]))
				fresh.pop(0)
				fresh.pop(0)
				fresh.insert(0, new)
				continue
		s += fresh[0][1] - fresh[0][0] + 1
		fresh.pop(0)
	return s

if __name__ == '__main__':
	main()

