# Youtube: https://youtu.be/lg6CRz3gV28

import argparse, math, sys, re, functools, operator, itertools, heapq
from collections import defaultdict, Counter, deque
from fractions import Fraction
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
	parser.add_argument('--test-scratch', action='store_true')
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
		print(part_2(lines, args.test_scratch))

@functools.lru_cache
def switch1(cur, press):
	ans = list(cur)
	for i in press:
		if ans[i] == '#':
			ans[i] = '.'
		else:
			assert ans[i] == '.'
			ans[i] = '#'
	return ''.join(ans)

def solve1(target, presses):
	visited = {}
	border = deque([('.' * len(target), 0)])
	while target not in visited:
		a, d = border.popleft()
		if a in visited:
			continue
		visited[a] = d
		for i in presses:
			border.append((switch1(a, i), d + 1))
	return visited[target]

def part_1(lines):
	s = 0
	for i in lines:
		_target, *_presses, _joltage = i.split()
		target = re.fullmatch('\[([\.#]+)\]', _target).group(1)
		presses = []
		for i in _presses:
			_i = re.fullmatch('\(([\d,]+)\)', i).group(1)
			presses.append(tuple(map(int, _i.split(','))))
		s += solve1(target, presses)
	return s

@functools.lru_cache
def switch2(cur, press):
	ans = list(cur)
	for i in press:
		ans[i] += 1
	return tuple(ans)

def solve2(joltage, presses):
	visited = {}
	border = deque([((0,) * len(joltage), 0)])
	while joltage not in visited:
		a, d = border.popleft()
		if a in visited:
			continue
		visited[a] = d
		for i in presses:
			j = switch2(a, i)
			if any(map(lambda x, y: x > y, j, joltage)):
				continue
			border.append((j, d + 1))
	return visited[joltage]

def part_2_brute_force(lines):
	s = 0
	for i in lines:
		_target, *_presses, _joltage = i.split()
		presses = []
		for i in _presses:
			_i = re.fullmatch('\(([\d,]+)\)', i).group(1)
			presses.append(tuple(map(int, _i.split(','))))
		_j = re.fullmatch('\{([\d,]+)\}', _joltage).group(1)
		joltage = tuple(map(int, _j.split(',')))
		s += solve2(joltage, presses)
	return s

###

def int_or_fraction(s):
	try:
		return int(s)
	except ValueError:
		return Fraction(s)

def simplex_solver(n, m, A, b, c):
	ibuf = []
	ibuf.append(str(n))
	ibuf.append(str(m))
	for i in A:
		ibuf.append(' '.join(map(str, i)))
	ibuf.append(' '.join(map(str, b)))
	ibuf.append(' '.join(map(str, c)))
	i = '\n'.join(ibuf).encode()
	# TODO: make
	from subprocess import check_output
	o = check_output(['./simplex'], input=i)
	x = list(map(int_or_fraction, o.decode().split()))
	return x

def check_linear_programming(n, m, A, b, c, x):
	assert len(A) == m
	assert len(A[0]) == n
	assert len(b) == m
	assert len(c) == n
	assert len(x) == n
	#print(sum(x), x)
	for i in range(m):
		assert sum(map(operator.mul, A[i], x)) <= b[i]

def linear_programming_scratch(n, m, A, b, c):
	A = A.copy()
	b = b.copy()
	c = c.copy()
	assert c == [-1] * n
	c = [-10000] * n
	x = simplex_solver(n, m, A, b, c)
	if all(map(lambda x: type(x) == int, x)):
		return x
	# Find t = ceil(sum(x))
	su = sum(x)
	if su.as_integer_ratio()[1] == 1:
		t = int(su)
	else:
		t = int(su) + 1
		m += 1
		A.append([-1] * n)
		b.append(-t)
		x = simplex_solver(n, m, A, b, c)
		su = sum(x)
		if all(map(lambda x: type(x) == int, x)):
			return x
	#check_linear_programming(n, m, A, b, c, x)
	y = linear_programming_scipy(n, m, A, b, c)
	# TODO
	if sum(x) != sum(y):
		assert any(map(lambda x: type(x) != int, x))
	if any(map(lambda x: type(x) != int, x)):
		print()
		print(sum(x), x, sum(map(lambda x, y: x * y, x, c)))
		print(sum(y), y, sum(map(lambda x, y: x * y, y, c)))
	#return x
	return None

def linear_programming_scipy(n, m, A, b, c):
	import scipy
	A_eq = A[:m//2]
	b_eq = b[:m//2]
	c_neg = list(map(operator.neg, c))
	ans = scipy.optimize.linprog(c=c_neg, A_eq=A_eq, b_eq=b_eq, integrality=1)
	x = list(map(round, ans.x))
	#print('A', *A_eq, sep='\n')
	#print('b', b_eq)
	#print('c', c)
	#print('x', x)
	check_linear_programming(n, m, A, b, c, x)
	return x

def part_2(lines, test_scratch):
	s = 0
	for i in lines:
		_target, *_presses, _joltage = i.split()
		presses = []
		for i in _presses:
			_i = re.fullmatch('\(([\d,]+)\)', i).group(1)
			presses.append(list(map(int, _i.split(','))))
		_j = re.fullmatch('\{([\d,]+)\}', _joltage).group(1)
		joltage = list(map(int, _j.split(',')))
		# n = number of buttons
		# m = 2 * number of counters
		# x[j] = how many times to press button j
		# A[i][j] = whether counter i can be activated by button j
		# A[i+m][j] = -A[i][j]
		# b[i] = counter i value
		# b[i+m] = -b[i]
		# c[j] = -1
		n = len(presses)
		m = len(joltage) * 2
		A = []
		for i in range(len(joltage)):
			A.append([0] * n)
			A.append([0] * n)
		for index, i in enumerate(presses):
			for j in i:
				A[j][index] = 1
				A[j + len(joltage)][index] = -1
		b = list(joltage) + list(map(operator.neg, joltage))
		c = [-1] * n
		x = linear_programming_scipy(n, m, A, b, c)
		if test_scratch:
			x1 = linear_programming_scratch(n, m, A, b, c)
			assert x1 is None or sum(x) == sum(x1)
		su = sum(x)
		s += su
	return s

if __name__ == '__main__':
	main()

