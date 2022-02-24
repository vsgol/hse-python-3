import os

import numpy as np

from easy_matrix import Matrix
from matrix_mixin import MixinMatrix


def matrix_operations(dir_path, matrix):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    m1 = matrix(np.random.randint(0, 10, (10, 10)))
    m2 = matrix(np.random.randint(0, 10, (10, 10)))
    result = m1 + m2
    result.write(f"{dir_path}/matrix+.txt")
    result = m1 * m2
    result.write(f"{dir_path}/matrix*.txt")
    result = m1 @ m2
    result.write(f"{dir_path}/matrix@.txt")


def collision(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    a = Matrix([[10 ** 9 + 8, 0], [0, 1]])
    c = Matrix([[1, 0], [0, 1]])
    b = Matrix(np.random.randint(1, 50, (2, 2)))
    d = b
    ab = a @ b
    cd = c @ d
    with open(f"{dir_path}/hash.txt", "w") as f:
        f.write(f"A hash: {hash(a)}\nC hash {hash(c)}")
    a.write(f"{dir_path}/A.txt")
    b.write(f"{dir_path}/B.txt")
    c.write(f"{dir_path}/C.txt")
    d.write(f"{dir_path}/D.txt")
    ab.write(f"{dir_path}/AB.txt")
    cd.write(f"{dir_path}/CD.txt")


if __name__ == '__main__':
    np.random.seed(0)
    matrix_operations('../artifacts/easy', Matrix)
    np.random.seed(0)
    matrix_operations('../artifacts/medium', MixinMatrix)
    collision('../artifacts/hard')
