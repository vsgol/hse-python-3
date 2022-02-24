from functools import reduce


class Array:
    def __init__(self, array):
        self.__array = list(array)

    def __len__(self):
        return self.__array.__len__()

    def __iter__(self):
        return self.__array.__iter__()

    def __getitem__(self, key):
        return self.__array[key]

    def __setitem__(self, key, value):
        self.__array[key] = value

    def __add__(self, other):
        if len(other) != len(self):
            raise ValueError('Arrays should be the same length')
        return Array(map(lambda x, y: x + y, self, other))

    def __mul__(self, other):
        if len(other) != len(self):
            raise ValueError('Arrays should be the same length')
        return Array(map(lambda x, y: x * y, self, other))

    def __matmul__(self, other):
        return reduce(lambda x, y: x + y, self * other)

    def __str__(self):
        return '[' + ', '.join(map(str, self.__array)) + ']'

    def __eq__(self, other):
        if isinstance(other, Array):
            return self.__array == other.__array
        else:
            return False


class Matrix:
    def __init__(self, matrix):
        self.__matrix = [Array(row) for row in matrix]
        self.__rows = self.__matrix.__len__()
        self.__columns = self.__matrix[0].__len__()

    def __iter__(self):
        return self.__matrix.__iter__()

    @property
    def rows(self):
        return self.__rows

    @property
    def columns(self):
        return self.__columns

    @property
    def shape(self):
        return self.__rows, self.__columns

    @property
    def T(self):
        return Matrix(list(zip(*self.__matrix)))

    def __add__(self, other):
        if self.shape != other.shape:
            raise ValueError('Dimensions of the matrices should match')
        return Matrix(list(map(lambda x, y: x + y, self, other)))

    def __mul__(self, other):
        if self.shape != other.shape:
            raise ValueError('Dimensions of the matrices should match')
        return Matrix([x * y for x, y in zip(self, other)])

    def __matmul__(self, other):
        if self.rows != other.columns:
            raise ValueError(
                'Number of columns in the first matrix should be equal to the number of rows in the second matrix')

        return Matrix(
            list(map(
                lambda row: Array(map(row.__matmul__, other.T)),
                self
            ))
        )

    def write(self, file_name):
        with open(file_name, "w") as file:
            file.write(self.__str__())

    def __str__(self):
        return '[\n\t' + ',\n\t'.join(map(str, self)) + ',\n]'

    def __eq__(self, other):
        if isinstance(other, Matrix):
            return all(map(lambda x, y: x == y, self, other))
        else:
            return False

    def __hash__(self):
        """
        Вычисляет производящую последовательности элементов по модулю простого числа
        """
        mod = 10 ** 9 + 7
        x = 10 ** 4 + 7
        current = 1
        res = 0
        for row in self.__matrix:
            for el in row:
                res = (res + el * current) % mod
                current = (current * x) % mod
        return int(res)
