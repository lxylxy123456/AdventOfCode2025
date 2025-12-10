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

using namespace algorithms;

void read_fraction(Fraction<long long int>& x) {
	long long int v;
	std::cin >> v;
	x = v;
}

int main(int argc, char *argv[]) {
	// n = number of buttons
	// m = number of counters
	// x[j] = how many times to press button j
	// a[i][j] = whether counter i can be activated by button j
	// a[i+m][j] = -a[i][j]
	// b[i] = counter i value
	// b[i+m] = -b[i]
	// c[j] = -1
	using T = Fraction<long long int>;

	size_t n, m;
	std::cin >> n >> m;
	matst A;
	for (std::size_t i = 1; i <= m; i++)
		for (std::size_t j = 1; j <= n; j++)
			read_fraction(A[n + i][j]);
	vectst b;
	for (std::size_t i = 1; i <= m; i++)
		read_fraction(b[n + i]);
	vectst c;
	for (std::size_t i = 1; i <= n; i++)
		read_fraction(c[i]);
	vectst x = Simplex(A, b, c, (T) 0);
	for (std::size_t i = 1; i <= n; i++)
		std::cout << x[i] << " ";
	std::cout << std::endl;
	return 0;
}
