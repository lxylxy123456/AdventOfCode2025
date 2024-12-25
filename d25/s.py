# Youtube: https://youtu.be/keyHGEVxEEI

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

def read_input(lines):
	l = iter(lines)
	keys = []
	locks = []
	while True:
		a = []
		for i in range(7):
			a.append(next(l))
		ans = []
		if a[0] == '#####':		# Lock
			assert a[-1] == '.....'
			for i in range(5):
				ans.append(list(map(operator.itemgetter(i), a)).count('#') - 1)
			locks.append(ans)
		elif a[0] == '.....':	# Key
			assert a[-1] == '#####'
			for i in range(5):
				ans.append(list(map(operator.itemgetter(i), a)).count('#') - 1)
			keys.append(ans)
		else:
			raise ValueError
		try:
			assert next(l) == ''
		except StopIteration:
			break
	return locks, keys

def part_1(lines):
	s = 0
	locks, keys = read_input(lines)
	for i in locks:
		for j in keys:
			if all(map(lambda x, y: x + y <= 5, i, j)):
				s += 1
	return s

def part_2(lines):
	s = 0
	for i in lines:
		i
	return s

if __name__ == '__main__':
	main()

