# Youtube: https://youtu.be/Y85JSiWARNQ

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
	parser.add_argument('--fast', action='store_true', help='Skip part_2_bad')
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
		ans = part_2(lines)
		if not args.fast:
			assert ans == part_2_bad(lines)
		print(ans)

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
	if min(my, ny) < ay < max(my, ny):
		if min(ax, bx) < mx < max(ax, bx):
			return True
	return False

def part_2_bad(lines):
	# Solve using geometry
	s = 0
	p = []
	for i in lines:
		p.append(tuple(map(int, i.split(','))))
	# p == [(7, 1), (11, 1), (11, 7), (9, 7), (9, 5), (2, 5), (2, 3), (7, 3)]
	# p is circular. Move it such that p[0][0] is minimum.
	index, _ = min(enumerate(p), key=lambda x: (x[1][0], -x[0]))
	p = p[index:] + p[:index]
	# p == [(2, 3), (7, 3), (7, 1), (11, 1), (11, 7), (9, 7), (9, 5), (2, 5)]
	d = []
	for i in p:
		d.append([0, 0])
	# For p[0][0] and p[-1][0], we definitely want to decrease.
	# out converts direction of segment to direction to outer space.
	assert p[-1][0] == p[0][0]
	d[0][0] = d[-1][0] = -1
	if p[-1][1] < p[1][1]:
		# Clockwise
		out = {'l': 'd', 'r': 'u', 'u': 'l', 'd': 'r'}
	elif p[-1][1] > p[1][1]:
		# Counter-clockwise
		out = {'l': 'u', 'r': 'd', 'u': 'r', 'd': 'l'}
	else:
		raise ValueError
	for index, ((ix, iy), (jx, jy)) in enumerate(zip(p[:-1], p[1:])):
		assert xor(ix == jx, iy == jy)
		if iy == jy:
			if ix < jx:
				cur = 'd'
			else:
				cur = 'u'
		else:
			assert ix == jx
			if iy < jy:
				cur = 'r'
			else:
				cur = 'l'
		o = out[cur]
		if o == 'r':
			d[index][1] = d[index + 1][1] = 1
		elif o == 'l':
			d[index][1] = d[index + 1][1] = -1
		elif o == 'u':
			d[index][0] = d[index + 1][0] = -1
		elif o == 'd':
			d[index][0] = d[index + 1][0] = 1
	# d == [[-1, -1], [-1, -1], [-1, -1], [1, -1], [1, 1], [-1, 1], [-1, 1],
	#		[-1, 1]]
	f = lambda x, y: x * 10 + y
	pp = list(map(lambda x, y: tuple(map(f, x, y)), p, d))
	# pp == [(19, 29), (69, 29), (69, 9), (111, 9), (111, 71), (89, 71),
	#		 (89, 51), (19, 51)]
	p = list(map(lambda x: tuple(map(lambda x: x * 10, x)), p))
	# p == [(20, 30), (70, 30), (70, 10), (110, 10), (110, 70), (90, 70),
	#		(90, 50), (20, 50)]
	if not 'plot':
		from matplotlib import pyplot as plt
		plt.plot(list(map(operator.itemgetter(0), pp + [pp[0]])),
				 list(map(operator.itemgetter(1), pp + [pp[0]])))
		plt.plot(list(map(operator.itemgetter(0), p + [p[0]])),
				 list(map(operator.itemgetter(1), p + [p[0]])))
		plt.show()
	edge = []
	for i, j in zip(pp, pp[1:] + [pp[0]]):
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
					#print(ix, iy, jx, jy, (ax, ay, bx, by, mx, my, nx, ny))
					return False
		return True
	for index, (ix, iy) in enumerate(p):
		for (jx, jy) in p[:index]:
			if test(ix, iy, jx, jy):
				s = max(s, (abs(ix - jx) + 10) * (abs(iy - jy) + 10))
	return s // 100

###

def build_segments(nums):
	segments = []
	revmap = {}
	n = sorted(set(nums))
	n.insert(0, n[0] - 1)
	n.append(n[-1] + 1)
	prev = None
	for i in n:
		if prev and prev < i - 1:
			segments.append((prev + 1, i - 1))
		revmap[i] = len(segments)
		segments.append((i, i))
		prev = i
	return segments, revmap

def minmax(a, b):
	return min(a, b), max(a, b)

def part_2(lines):
	s = 0
	p = []
	for i in lines:
		p.append(tuple(map(int, i.split(','))))
	sx, rx = build_segments(map(operator.itemgetter(0), p))
	sy, ry = build_segments(map(operator.itemgetter(1), p))
	SX = len(sx)
	SY = len(sy)
	m = []
	for x in range(SX):
		m.append([])
		for y in range(SY):
			m[-1].append('/')
	for x, y in p:
		m[rx[x]][ry[y]] = '#'
	for (x0, y0), (x1, y1) in zip(p, p[1:] + [p[0]]):
		x0_, x1_ = minmax(rx[x0], rx[x1])
		y0_, y1_ = minmax(ry[y0], ry[y1])
		for x in range(x0_, x1_ + 1):
			for y in range(y0_, y1_ + 1):
				if m[x][y] == '/':
					m[x][y] = 'X'
	# Fill outer using BFS
	assert m[0][0] == '/'
	frontier = {(0, 0)}
	while frontier:
		x, y = frontier.pop()
		if m[x][y] != '/':
			continue
		m[x][y] = '.'
		for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
			xx = x + dx
			yy = y + dy
			if xx in range(len(m)) and yy in range(len(m[0])):
				frontier.add((xx, yy))
	# Compute inner
	for index, i in enumerate(m):
		for jndex, j in enumerate(i):
			if j == '/':
				i[jndex] = 'X'
	#print(*map(''.join, m), sep='\n')
	def test(ix, iy, jx, jy):
		x0_, x1_ = minmax(rx[ix], rx[jx])
		y0_, y1_ = minmax(ry[jy], ry[iy])
		for x in range(x0_, x1_ + 1):
			for y in range(y0_, y1_ + 1):
				if m[x][y] == '.':
					return False
		return True

	for index, (ix, iy) in enumerate(p):
		for (jx, jy) in p[:index]:
			if test(ix, iy, jx, jy):
				s = max(s, (abs(ix - jx) + 1) * (abs(iy - jy) + 1))
	return s

if __name__ == '__main__':
	main()

