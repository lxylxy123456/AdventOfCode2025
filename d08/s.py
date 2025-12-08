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

def dist(a, b):
	return sum(map(lambda x, y: (x - y)**2, a, b))

def part_1(lines):
	s = 0
	if len(lines) == 20:
		c = 10
	elif len(lines) == 1000:
		c = 1000
	junctions = []
	for i in lines:
		junctions.append(tuple(map(int, i.split(','))))
	conns = []
	for index, i in enumerate(junctions):
		for jndex, j in enumerate(junctions[:index]):
			conns.append((dist(i, j), index, jndex))
	conns.sort()
	ufs = list(range(len(junctions)))
	def find(x):
		if (y := ufs[x]) != x:
			ufs[x] = find(y)
		return ufs[x]
	def union(x, y):
		ufs[find(x)] = find(y)
	for _, i, j in conns[:c]:
		union(i, j)
	groups = Counter()
	for i in range(len(ufs)):
		groups[find(i)] += 1
	return functools.reduce(operator.mul, map(lambda x: x[1], groups.most_common(3)))

def part_2(lines):
	s = 0
	if len(lines) == 20:
		c = 10
	elif len(lines) == 1000:
		c = 1000
	junctions = []
	for i in lines:
		junctions.append(tuple(map(int, i.split(','))))
	conns = []
	for index, i in enumerate(junctions):
		for jndex, j in enumerate(junctions[:index]):
			conns.append((dist(i, j), index, jndex))
	conns.sort()
	ufs = list(range(len(junctions)))
	def find(x):
		if (y := ufs[x]) != x:
			ufs[x] = find(y)
		return ufs[x]
	def union(x, y):
		fx = find(x)
		fy = find(y)
		ufs[fx] = fy
		return fx != fy
	count = 0
	for _, i, j in conns:
		count += int(union(i, j))
		if count == len(lines) - 1:
			return junctions[i][0] * junctions[j][0]

if __name__ == '__main__':
	main()

