from fpylll import IntegerMatrix, LLL, BKZ, SVP
def convert_to_mat(A, t, q):
    k = len(t)
    id_mat = []
    cnt = 0
    for i in range(k):
        row = [0]*k
        row[cnt] = 1
        cnt += 1
        id_mat.append(row)

    mat = []
    for i in range(2*k + 1):
        row = [0]*(2*k+1)
        for j in range(2*k + 1):
            if i < k and j < k:
                if i == j:
                    row[j] = q
            elif i < k and j < 2*k:
                row[j] = -A[i][j-k]
            elif i < k:
                row[j] = t[i]
            elif j >= k and i == j:
                row[j] = 1
        mat.append(row)
        return mat

def solve_svp(A, t, q):
    mat = convert_to_mat(A, t, q)
    b = IntegerMatrix(mat)

    # LLL reduction
    b1 = b
    LLL.reduction(b1)

    # BKZ reduction
    b2 = b
    BKZ.reduction(b2, o=BKZ.Param(block_size=k))

    # SVP direct
    b3 = b
    SVP.shortest_vector(b3)