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

#ifndef ALGORITHMS_SQUAREMATRIXMULTIPLY
#define ALGORITHMS_SQUAREMATRIXMULTIPLY

#include <cassert>
#include <iostream>
#include <vector>

namespace algorithms {

template <typename T>
class MatrixRow: public std::vector<T> {
	public:
	MatrixRow(): std::vector<T>(std::vector<T>()) {}
	MatrixRow(const std::vector<T>& d): std::vector<T>(d) {}
	MatrixRow(typename std::vector<T>::iterator s,
				typename std::vector<T>::iterator e): std::vector<T>(s, e) {}
	MatrixRow(std::size_t c, T T0): std::vector<T>(std::vector<T>(c, T0)) {}
	MatrixRow<T> operator+(const MatrixRow<T> rhs) {
		assert(this->size() == rhs.size());
		MatrixRow<T> ans(this->size());
		for (std::size_t i = 0; i < this->size(); i++)
			ans[i] = (*this)[i] + rhs[i];
		return ans;
	}
	friend std::ostream& operator<<(std::ostream& os, const MatrixRow& rhs) {
		for (std::size_t i = 0; i < rhs.size(); i++)
			os << rhs[i] << ' ';
		return os;
	}
	MatrixRow<T> concat_h(MatrixRow<T> rhs) {
		MatrixRow<T> ans(*this);
		ans.insert(ans.end(), rhs.begin(), rhs.end());
		return ans;
	}
};

// 某些被删除的迭代器代码: 见 git doc commit 63373f4c
template <typename T>
class Matrix {
	public:
	Matrix(std::size_t r, std::size_t c, std::vector<T> d): rows(r), cols(c) {
		data.reserve(r);
		typename std::vector<T>::iterator begin = d.begin(), end = begin;
		for (std::size_t i = 0; i < r; i++) {
			end = begin + c;
			data.push_back(MatrixRow<T>(begin, end));
			begin += c;
		}
	}
	Matrix(std::size_t r, std::size_t c, T T0): rows(r), cols(c) {
		data.reserve(r);
		for (std::size_t i = 0; i < r; i++)
			data.push_back(MatrixRow<T>(c, T0));
	}
	Matrix(std::size_t r, std::size_t c): rows(r), cols(c) {
		data.reserve(r);
	}
	friend std::ostream& operator<<(std::ostream& os, const Matrix& rhs) {
		for (std::size_t i = 0; i < rhs.rows; i++)
			os << rhs.data[i] << std::endl;
		return os;
	}
	std::ostream& octave(std::ostream& os) {
		os << '[';
		for (std::size_t i = 0; i < rows; i++) {
			os << data[i];
			if (i != rows - 1)
				os << ';';
		}
		return os << ']' << std::endl;
	}
	MatrixRow<T>& operator[](std::size_t index) { return data[index]; }
	bool operator==(const Matrix<T>& rhs) const {
		return data == rhs.data;
	}
	Matrix<T> operator+(Matrix<T>& rhs) {
		Matrix<T> ans(rows, cols);
		assert(rows == rhs.rows && cols == rhs.cols);
		for (std::size_t i = 0; i < rows; i++) {
			MatrixRow<T> tmp;
			tmp.reserve(ans.cols);
			for (std::size_t j = 0; j < cols; j++)
				tmp.push_back((*this)[i][j] + rhs[i][j]);
			ans.data.push_back(tmp);
		}
		return ans;
	}
	Matrix<T> operator-(Matrix<T>& rhs) {
		Matrix<T> ans(rows, cols);
		assert(rows == rhs.rows && cols == rhs.cols);
		for (std::size_t i = 0; i < rows; i++) {
			MatrixRow<T> tmp;
			tmp.reserve(ans.cols);
			for (std::size_t j = 0; j < cols; j++)
				tmp.push_back((*this)[i][j] - rhs[i][j]);
			ans.data.push_back(tmp);
		}
		return ans;
	}
	Matrix<T> concat_h(Matrix<T> rhs) {
		assert(rows == rhs.rows);
		Matrix<T> ans(rows, cols + rhs.cols);
		for (std::size_t i = 0; i < rows; i++)
			ans.data.push_back(data[i].concat_h(rhs[i]));
		return ans;
	}
	Matrix<T> concat_v(Matrix<T> rhs) {
		assert(cols == rhs.cols);
		Matrix<T> ans(*this);
		ans.data.insert(ans.data.end(), rhs.data.begin(), rhs.data.end());
		ans.rows += rhs.rows;
		return ans;
	}
	Matrix<T> transpose() {
		Matrix<T> ans(cols, rows, 0);
		for (std::size_t i = 0; i < cols; i++)
			for (std::size_t j = 0; j < rows; j++)
				ans[i][j] = (*this)[j][i];
		return ans;
	}
	void add_row(T T0) {
		rows += 1;
		data.push_back(MatrixRow<T>(cols, T0));
	}
	void add_col(T T0) {
		cols += 1;
		for (std::size_t i = 0; i < rows; i++)
			data[i].push_back(T0);
	}
	// members
	std::size_t rows, cols;
	std::vector<MatrixRow<T>> data;
};

}

#endif
