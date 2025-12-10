//
//  algorithms - some algorithms in "Introduction to Algorithms", third edition
//  Copyright (C) 2018  lxylxy123456
//
//  This program is free software: you can redistribute it and/or modify
//  it under the terms of the GNU Affero General Public License as
//  published by the Free Software Foundation, either version 3 of the
//  License, or (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU Affero General Public License for more details.
//
//  You should have received a copy of the GNU Affero General Public License
//  along with this program.  If not, see <https://www.gnu.org/licenses/>.
//

#include "Simplex.hpp"

#include <iostream>
#include <vector>

#include "LUPSolve.hpp"
#include "utils.hpp"

using namespace algorithms;

int main(int argc, char *argv[]) {
	// n = number of buttons
	// m = 2 * number of counters
	// x[j] = how many times to press button j
	// a[i][j] = whether counter i can be activated by button j
	// a[i+m/2][j] = -a[i][j]
	// b[i] = counter i value
	// b[i+m/2] = -b[i]
	// c[j] = -1
	using T = Fraction<int>;

	// [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
	size_t n = 6;
	size_t m = 8;
	matst A {
		{6 + 1, {{1, 0}, {2, 0}, {3, 0}, {4, 0}, {5, 1}, {6, 1}}},
		{6 + 2, {{1, 0}, {2, 1}, {3, 0}, {4, 0}, {5, 0}, {6, 1}}},
		{6 + 3, {{1, 0}, {2, 0}, {3, 1}, {4, 1}, {5, 1}, {6, 0}}},
		{6 + 4, {{1, 1}, {2, 1}, {3, 0}, {4, 1}, {5, 0}, {6, 0}}},
		{6 + 5, {{1, -0}, {2, -0}, {3, -0}, {4, -0}, {5, -1}, {6, -1}}},
		{6 + 6, {{1, -0}, {2, -1}, {3, -0}, {4, -0}, {5, -0}, {6, -1}}},
		{6 + 7, {{1, -0}, {2, -0}, {3, -1}, {4, -1}, {5, -1}, {6, -0}}},
		{6 + 8, {{1, -1}, {2, -1}, {3, -0}, {4, -1}, {5, -0}, {6, -0}}},
	};
	vectst b = {
		{6 + 1, 3},
		{6 + 2, 5},
		{6 + 3, 4},
		{6 + 4, 7},
		{6 + 5, -3},
		{6 + 6, -5},
		{6 + 7, -4},
		{6 + 8, -7},
	};
	vectst c = {
		{1, -1},
		{2, -1},
		{3, -1},
		{4, -1},
		{5, -1},
		{6, -1},
	};

	for (std::size_t i = 1; i <= m; i++) {
		for (std::size_t j = 1; j <= n; j++)
			std::cout << A[n + i][j] << " ";
		std::cout << std::endl;
	}
	std::cout << std::endl;
	for (std::size_t i = 1; i <= m; i++)
		std::cout << b[n + i] << " ";
	std::cout << std::endl;
	for (std::size_t i = 1; i <= n; i++)
		std::cout << c[i] << " ";
	std::cout << std::endl;
	vectst x = Simplex(A, b, c, (T) 0);
	for (std::size_t i = 1; i <= n; i++)
		std::cout << x[i] << " ";
	std::cout << std::endl;
	for (std::size_t i = 1; i <= m; i++) {
		T s = 0;
		for (std::size_t j = 1; j <= n; j++) {
			s += A[n + i][j] * x[j];
		}
		assert(s == b[n + i]);
	}

	return 0;
}
