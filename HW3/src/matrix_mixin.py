import numbers

import numpy as np


class GetterSetterMixin:
    def __init__(self, matrix):
        self.verify(matrix)
        self.__matrix = np.asarray(matrix)

    @property
    def matrix(self):
        return self.__matrix

    @matrix.setter
    def matrix(self, matrix):
        self.verify(matrix)
        self.__matrix = matrix

    @staticmethod
    def verify(matrix):
        if not all(map(lambda x: len(x) == len(matrix[0]), matrix)):
            raise ValueError('Incorrect matrix shape')


class ShapeMixin(GetterSetterMixin):
    def __init__(self, matrix):
        super().__init__(matrix)

    @property
    def rows(self):
        if len(self.matrix) > 0:
            return self.matrix[0].__len__()

    @property
    def columns(self):
        return self.matrix.__len__()

    @property
    def T(self):
        return ShapeMixin(list(zip(*self.matrix)))

    @property
    def shape(self):
        return self.rows, self.columns


class IterableMixin(GetterSetterMixin):
    def __iter__(self):
        return self.matrix.__iter__()


class WriteableMixin(IterableMixin):
    def write(self, file_name):
        with open(file_name, "w") as file:
            file.write(self.__str__())

    def __str__(self):
        return '[\n\t' + ',\n\t'.join(map(str, self)) + ',\n]'


class MixinMatrix(np.lib.mixins.NDArrayOperatorsMixin, WriteableMixin, ShapeMixin):
    _HANDLED_TYPES = (np.ndarray, numbers.Number)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        for x in inputs + out:
            # Only support operations with instances of _HANDLED_TYPES.
            # Use ArrayLike instead of type(self) for isinstance to
            # allow subclasses that don't override __array_ufunc__ to
            # handle ArrayLike objects.
            if not isinstance(x, self._HANDLED_TYPES + (MixinMatrix,)):
                return NotImplemented

        # Defer to the implementation of the ufunc on unwrapped values.
        inputs = tuple(x.matrix if isinstance(x, MixinMatrix) else x
                       for x in inputs)
        if out:
            kwargs['out'] = tuple(
                x.matrix if isinstance(x, MixinMatrix) else x
                for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            # multiple return values
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            # no return value
            return None
        else:
            # one return value
            return type(self)(result)
