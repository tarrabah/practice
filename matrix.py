import copy
import math
import operator

'''
NOTE!!!
Matrix elements indexes start with 0

'''

def limits_check(matrix, indexes):
    if (not 0 <= indexes[0] < matrix.size()[0]) or (not  0 <= indexes[1] < matrix.size()[1]):
        return False

    return True


def line_len_check(matrix, line):
    if matrix.size()[1] != len(line):
        return False
    return True


def column_len_check(matrix, column):
    if matrix.size()[0] != len(column):
        return False
    return True


class MatrixError(BaseException):
    def __init__(self, matrix1, other):
        self.matrix1 = matrix1
        self.matrix2 = other


class Matrix_index_out_of_limits(BaseException):
    def __init__(self, matrix, indexes):
        self.text = "Matrix size is " + str(matrix.size()[0]) + "x" + str(matrix.size()[1]) + ", but indexes are (" + str(indexes[0]) + ", " + str(indexes[1]) + ")"
        self.matrix = matrix
        self.indexes = indexes

    def __str__(self):
        return self.text


class Matrix_is_not_square(BaseException):
    def __init__(self, matrix):
        self.matrix = matrix
        self.text = "Given matrix " + str(matrix.size()[0]) + "x" + str(matrix.size()[1]) + " is not square"

    def __str__(self):
        return self.text


class line_size_error(BaseException):
    def __init__(self, matrix, line):
        self.matrix = matrix
        self.line = line
        self.text = "Line length is " + str(len(line)) + ", while matrix size is " + str(matrix.size()[0]) + "x" + str(matrix.size()[1])

    def __str__(self):
        return self.text


class column_size_error(BaseException):
    def __init__(self, matrix, column):
        self.matrix = matrix
        self.column = column
        self.text = "Column length is " + str(len(column)) + ", while matrix size is " + str(matrix.size()[0]) + "x" + str(matrix.size()[1])

    def __str__(self):
        return self.text


class Matrix:
    def __init__(self, elements):
        self.elements = copy.deepcopy(elements)


    def __str__(self):
        return '\n'.join(
            list(
                map(
                    lambda x: '\t'.join(
                        list(
                            map(
                                str,
                                x
                            )
                        )
                    ),
                    self.elements
                )
            )
        )


    def size(self):
        return (len(self.elements), len(self.elements[0]))


    def get_elem(self, indexes):
        if not limits_check(self, indexes):
            raise Matrix_index_out_of_limits(self, indexes)
        else:
            return self.elements[indexes[0]][indexes[1]]


    def get_minor(self, indexes):
        if not limits_check(self, indexes):
            raise Matrix_index_out_of_limits(self, indexes)
        else:
            minor = []

            for i in range(self.size()[0]):
                if i != indexes[0]:
                    minor.append(self.elements[i][:indexes[1]] + self.elements[i][indexes[1] + 1:])

            return SquareMatrix(minor.copy())


    def insert_line(self, line, index):
        if not line_len_check(self, line):
            raise line_size_error(self, line)
        elif not limits_check(self, (index, 0)):
            raise Matrix_index_out_of_limits(self, (index, 0))
        else:
            result = copy.deepcopy(self.elements)
            result[index] = line

            return type(self)(result)


    def insert_column(self, column, index):
        if not column_len_check(self, column):
            raise column_size_error(self, column)
        elif not limits_check(self, (0, index)):
            raise Matrix_index_out_of_limits(self, (0, index))
        else:
            result = copy.deepcopy(self.elements)

            for i in range(self.size()[0]):
                result[i][index] = column[i]


            return type(self)(result)


    def get_algebraic_adjunct(self, indexes):
        if not limits_check(self, indexes):
            raise Matrix_index_out_of_limits(self, indexes)
        else:
            return (self.get_minor(indexes)).get_det() * (-1) ** (sum(indexes))


    def __add__(self, other):
        if isinstance(other, type(self)) and (self.size() == other.size()):
            result = Matrix(
                list(
                    map(
                        lambda x, y:  list(
                            map(
                                lambda a: a[0] + a[1],
                                zip(
                                    x,
                                    y
                                )
                            )
                        ),
                        self.elements,
                        other.elements
                    )
                )
            )
            return result

        else:
            raise MatrixError(self, other)


    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            result = Matrix(
                list(
                    map(
                        lambda x: list(
                            map(
                                lambda z: z * other,
                                x
                            )
                        ),
                        self.elements
                    )
                )
            )
            return result


        elif isinstance(other, Matrix) and (self.size()[1] == other.size()[0]):
            mul2 = other.transposed2(other)
            res = Matrix(
                list(
                    map(
                        lambda x: list(
                            map(
                                lambda y: sum(
                                    list(
                                        map(
                                            lambda c: c[0] * c[1],
                                            list(
                                                zip(x, y)
                                            )
                                        )
                                    )
                                ),
                                mul2)
                        ),
                        self.elements
                    )
                )
            )
            return res
        else:
            raise MatrixError(self, other)


    def transpose(self):
        self.elements = list(
            map(
                list,
                zip(
                    *self.elements
                )
            )
        )
        return self


    @staticmethod
    def transposed(x):
        return Matrix(
            list(
                map(
                    list,
                    zip(
                        *x.elements
                    )
                )
            )
        )


    @staticmethod
    def transposed2(x):
        return list(
                map(
                    list,
                    zip(
                        *x.elements
                    )
                )
        )


    __rmul__ = __mul__


class SquareMatrix(Matrix):

    def __init__(self, elements):
        super().__init__(elements)

        if self.size()[0] != self.size()[1]:
            raise Matrix_is_not_square(self)


    def __pow__(self, power):
        res = Matrix(copy.deepcopy(self.elements))

        for i in range(power - 1):
            res = res * self
        return res


    def get_det(self):
        if self.size() == (1, 1):
            return self.elements[0][0]

        elif self.size() == (2, 2):
            return self.elements[0][0] * self.elements[1][1] - self.elements[0][1] * self.elements[1][0]

        else:
            det = 0
            for i in range(self.size()[1]):
                det += self.elements[0][i] * self.get_algebraic_adjunct((0, i))

            return det


    def get_invertible_matrix(self):

        line_num, col_num = self.size()

        result = []

        for i in range(line_num):
            result.append([])
            for j in range(col_num):
                result[i].append(self.get_algebraic_adjunct((i, j)))

        #print(result)
        #print(self.get_det())


        return 1 / self.get_det() * SquareMatrix(result).transpose()


    def cramers_rule(self, var_line_B):
        if not column_len_check(self, var_line_B):
            raise column_size_error(self, var_line_B)

        else:
            det_A = self.get_det()
            # print(det_A)
            if math.fabs(det_A) < 10 ** (-7):
                return []
            else:
                det_Ax = []
                x = []

                for i in range(self.size()[1]):
                    det_Ax.append(self.insert_column(var_line_B, i).get_det())
                    x.append(det_Ax[i] / det_A)

                return list(map(lambda t: [t], x))


    def invertible_matrix_solve(self, var_line_B):

        if not column_len_check(self, var_line_B):
            raise column_size_error(self, var_line_B)

        else:
            det_A = self.get_det()
            # print(det_A)
            if math.fabs(det_A) < 10 ** (-7):
                return []
            else:
                result = self.get_invertible_matrix() * Matrix(list(map(lambda x: [x], var_line_B)))
                return result.elements


    def gauss_solve(self, var_line_B):
        if not column_len_check(self, var_line_B):
            raise column_size_error(self, var_line_B)
        else:
            extended_matrix_elements = copy.deepcopy(self.elements)
            for i in range(len(var_line_B)):
                extended_matrix_elements[i].append(var_line_B[i])

            extended_matrix = Matrix(extended_matrix_elements)
            #print(extended_matrix)


            for i in range(self.size()[1] - 1): #M[i, i] - main element
                if math.fabs(extended_matrix.elements[i][i]) < 10 ** (-7):
                    for j in range(i, self.size()[0]): #searching for the first line with element != 0 in i-th column
                        if extended_matrix.elements[j][i] != 0:
                            extended_matrix.elements[i], extended_matrix.elements[j] = extended_matrix.elements[j], extended_matrix.elements[i]
                            break
                    #print("\trow shifted")
                    #print(extended_matrix)
                #print('main element:', extended_matrix.elements[i][i])
                line = copy.deepcopy(extended_matrix.elements[i])
                #print("\tline:", line)

                for j in range(i + 1, self.size()[0]):
                    if math.fabs(extended_matrix.elements[j][i]) > 10 ** (-7):
                        #print("coof:", extended_matrix.elements[j][i], '//',  extended_matrix.elements[i][i])
                        #print("line:", list(map(lambda x: operator.mul(x, extended_matrix.elements[j][i] / extended_matrix.elements[i][i]), extended_matrix.elements[i])))
                        divided_line = list(map(lambda x: operator.mul(x, extended_matrix.elements[j][i] / extended_matrix.elements[i][i]), extended_matrix.elements[i]))
                        extended_matrix.elements[j] = list(
                            map(lambda x: operator.sub(*x), zip(extended_matrix.elements[j], divided_line)))
                #print("subctraction ok")
                #print(extended_matrix)

            #TODO: check zero lines

            for i in range(self.size()[0]):
                count_zeroes = 0
                for j in range(self.size()[1]):
                    if math.fabs(extended_matrix.elements[i][j]) < 10 ** (-7):
                        count_zeroes += 1
                if count_zeroes == self.size()[0]:
                    return []

            result = [0 for _ in range(self.size()[0])]

            for i in range(self.size()[0] - 1, -1, -1):

                for j in range(self.size()[0] - 1, i, -1):
                    extended_matrix.elements[i][-1] -= extended_matrix.elements[i][j] * result[j]

                result[i] = extended_matrix.elements[i][-1] / extended_matrix.elements[i][i]
                #print(extended_matrix.elements[i][i])

            return list(map(lambda t: [t], result))




a = SquareMatrix([[4, 2, -6], [-8, -7, 1], [4, 2, -8]])
b = [5, 3, 6]
print(a.cramers_rule(b))
print(a.invertible_matrix_solve(b))
print(a.gauss_solve(b))
