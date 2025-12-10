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
	print('2:', visited[joltage])
	return visited[joltage]

def part_2(lines):
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

if __name__ == '__main__':
	main()

