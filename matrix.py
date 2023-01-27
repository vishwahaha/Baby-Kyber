class Matrix:
    def __init__(self, ring, elements=None):
        if elements is None:
            elements = [[]]
        self.rows = elements
        self.m = len(elements)
        self.n = len(elements[0])
        self.ring = ring
        if not self.validate_dimensions():
            raise ValueError('All rows in a matrix must be of same length')

    def get_dimensions(self):
        """
        :return: number of rows and columns in this matrix
        """
        return self.m, self.n

    def validate_dimensions(self):
        """
        Checks if the matrix is valid
        """
        return all(len(row) == self.n for row in self.rows)

    def transpose(self):
        """
        Return the transpose of this matrix
        """
        self.m, self.n = self.n, self.m
        self.rows = [list(item) for item in zip(*self.rows)]
        return self

    def __call__(self, elements):
        if not isinstance(elements, list):
            raise TypeError('Elements of matrix must be passed in a list')

        if isinstance(elements[0], list):
            for row in elements:
                if not all(isinstance(ele, self.ring.element) for ele in row):
                    raise TypeError(f'All elements of the matrix must be polynomials of the ring: {self.ring}')
            return Matrix(self.ring, elements)

        elif isinstance(elements[0], self.ring.element):
            if not all(isinstance(ele, self.ring.element) for ele in elements):
                raise TypeError(f'All elements of the matrix must be polynomials of the ring: {self.ring}')
            return Matrix(self.ring, [elements])

        else:
            raise TypeError('Elements of a matrix must be polynomials ina list of lists, from the same ring')

    def __repr__(self):
        if len(self.rows) == 1:
            return str(self.rows[0])
        max_col_width = []
        for n_col in range(self.n):
            max_col_width.append(max(len(str(row[n_col])) for row in self.rows))
        info = ']\n['.join([', '.join([f'{str(x):>{max_col_width[i]}}' for i, x in enumerate(r)]) for r in self.rows])
        return f'[{info}]'

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, item):
        return self.rows[item]

    def __eq__(self, other):
        return self.rows == other.rows

    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError('Matrices can only be added to matrices')
        if self.ring != other.ring:
            raise TypeError('Matrices must have same base ring')
        if self.get_dimensions() != other.get_dimensions():
            raise TypeError('Matrices must have same dimensions')

        new_rows = []
        for i in range(self.m):
            new_rows.append([a + b for a, b in zip(self.rows[i], other.rows[i])])
        return self(new_rows)

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        self = self + other
        return self

    def __sub__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError('Matrices can only be subtracted from matrices')
        if self.ring != other.ring:
            raise TypeError('Matrices must have same base ring')
        if self.get_dimensions() != other.get_dimensions():
            raise TypeError('Matrices must have same dimensions')
        new_rows = []
        for i in range(self.m):
            new_rows.append([a - b for a, b in zip(self.rows[i], other.rows[i])])
        return self(new_rows)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __isub__(self, other):
        self = self - other
        return self

    def __matmul__(self, other):
        """
        This is done by using '@' operator
        """
        if not isinstance(other, Matrix):
            raise TypeError('Matrices can only be multiplied to matrices')
        if self.ring != other.ring:
            raise TypeError('Matrices must have same base ring')
        if self.n != other.m:
            raise TypeError('Matrices must have same dimensions')
        result = [[sum(a * b for a, b in zip(A_row, B_col)) for B_col in zip(*other.rows)] for A_row in self.rows]
        return self(result)
