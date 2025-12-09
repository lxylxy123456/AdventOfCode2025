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
	p = []
	for i in lines:
		p.append(tuple(map(int, i.split(','))))
	for index, (ix, iy) in enumerate(p):
		for (jx, jy) in p[:index]:
			s = max(s, (abs(ix - jx) + 1) * (abs(iy - jy) + 1))
	return s

def xor(a, b):
	return not (a and b) and (a or b)

def cross(ax, ay, bx, by, mx, my, nx, ny):
	assert xor(ax == bx, ay == by)
	assert xor(mx == nx, my == ny)
	if (ax == bx) and (mx == nx):
		return False
	if (ay == by) and (my == ny):
		return False
	if (ax == bx):
		return cross(ay, ax, by, bx, my, mx, ny, nx)
	assert ay == by
	assert mx == nx
	if min(my, ny) < ay < max(mx, nx):
		if min(ax, bx) < mx < max(ax, bx):
			return True
	return False

def part_2(lines):
	s = 0
	p = []
	for i in lines:
		p.append(tuple(map(int, i.split(','))))
	edge = []
	for i, j in zip(p, p[1:] + [p[0]]):
		edge.append((i, j))
	def test(ix, iy, jx, jy):
		for (ax, ay, bx, by) in [
				(ix, iy, jx, iy),
				(ix, jy, jx, jy),
				(ix, iy, ix, jy),
				(jx, iy, jx, jy),
			]:
			if ax == bx and ay == by:
				continue
			assert xor(ax == bx, ay == by)
			for (mx, my), (nx, ny) in edge:
				assert xor(mx == nx, my == ny)
				if cross(ax, ay, bx, by, mx, my, nx, ny):
					return False
		return True
	for index, (ix, iy) in enumerate(p):
		for (jx, jy) in p[:index]:
			if test(ix, iy, jx, jy):
				print(ix, iy, jx, jy, (abs(ix - jx) + 1) * (abs(iy - jy) + 1))
				s = max(s, (abs(ix - jx) + 1) * (abs(iy - jy) + 1))
	return s

if __name__ == '__main__':
	main()

