# Youtube: https://youtu.be/fDAw3lO2u2Q

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
	m = defaultdict(list)
	for i in lines:
		s, ds = i.split(':')
		ds = ds.split()
		m[s] = ds
	def dfs(x):
		if x == 'out':
			return 1
		ans = 0
		for i in m[x]:
			ans += dfs(i)
		return ans
	s = dfs('you')
	return s

def part_2(lines):
	s = 0
	m = defaultdict(list)
	for i in lines:
		s, ds = i.split(':')
		ds = ds.split()
		m[s] = ds
	# Reverse m
	n = defaultdict(list)
	for k, v in m.items():
		for i in v:
			n[i].append(k)
	# Topological sort
	o = []
	visited = set()
	def dfs1(x):
		if x in visited:
			return
		visited.add(x)
		for i in n[x]:
			dfs1(i)
		o.append(x)
	dfs1('out')
	# DP
	def build_dp(src):
		ans = defaultdict(int)
		ans[src] = 1
		for i in o:
			for j in m[i]:
				ans[j] += ans[i]
		return ans
	dp_s = build_dp('svr')
	dp_d = build_dp('dac')
	dp_f = build_dp('fft')
	sdfo = (dp_s['dac'] * dp_d['fft'] * dp_f['out'])
	sfdo = (dp_s['fft'] * dp_f['dac'] * dp_d['out'])
	s = sdfo + sfdo
	return s

if __name__ == '__main__':
	main()

