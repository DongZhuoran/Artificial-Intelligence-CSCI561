# This is homework-1-b of Hong Yu
import numpy as np

# judge whether the place of officer is right
def isok(r,c,n):
    if downslash_lookup[r - c + n - 1] or upslash_lookup[r + c] or colum_lookup[c]:
        return False
    return True


# traceback algorithm
def traceback(row,p,N,col,downslash_lookup,upslash_lookup,colum_lookup,depth):
    global Sum,Add
    flag = 0
    for j in range(row, N-p+1):
        for k in range(N):
            if isok(j,k,N):
                MaxSum = 0
                times = 0
                for i in range(N):
                    if j < Max_Sort[i] < N:
                        MaxSum = MaxSum + Max_Order[Max_Sort[i]]
                        times = times + 1
                    if times == p-1:
                        break
                if Sum < Add + MaxSum + chessboard[j][k]:
                    col[j] = k
                    flag = 1
                    Add = Add + chessboard[j][k]
                    if col.count(-1) == depth:
                        Add1 = 0
                        for l in range(N-n,N):
                            if col[l]!= -1:
                                Add1 = Add1 + chessboard[l][col[l]]
                        Sum = max(Sum,Add1)
                        # print(Sum)
                        # print(col)
                    else:
                        downslash_lookup[j - k + N - 1] = True
                        upslash_lookup[j + k] = True
                        colum_lookup[k] = True
                        traceback(j+1,p-1,N,col,downslash_lookup,upslash_lookup,colum_lookup,depth)
            if flag == 1:
                downslash_lookup[j - k + N - 1] = False
                upslash_lookup[j + k] = False
                colum_lookup[k] = False
                Add = Add - chessboard[j][k]
                flag = 0
        col[j] = -1


if __name__ == '__main__':
    # global value Sum
    Sum = 0
    # read file
    f = open("input.txt", 'r')
    str1 = f.readline()
    str2 = f.readline()
    str3 = f.readline()
    n = int(str1[0:len(str1)-1])
    p = int(str2[0:len(str2)-1])


    # make a slashboard
    downslash = [[0 for colums1 in range(n)] for row1 in range(n)]
    upslash = [[0 for colums2 in range(n)] for row2 in range(n)]
    for r in range(n):
        for c in range(n):
            downslash[r][c] = r - c + n - 1
            upslash[r][c] = r + c
    downslash_lookup = (2*n-1)*[False]
    upslash_lookup = (2*n-1)*[False]
    colum_lookup = n*[False]

    # make a chessboard
    chessboard = [[0 for colums in range(n)] for row in range(n)]
    col = [-1]*n

    # add value to chessboard
    while True:
        coordinate = f.readline()
        if not coordinate:
            break
        [x,y] = coordinate.split(',')
        y = int(y)
        x = int(x)
        chessboard[x][y] = chessboard[x][y] + 1
    f.close()


    Max_Order = n*[0]
    for i in range(n):
        Max_Order[i] = max(chessboard[i])
    Max_Sort = np.argsort(Max_Order)
    Max_Sort = Max_Sort[::-1]


    if p == 0:
        Sum = 0
    elif p == 1:
        Sum = max(Max_Order)
    else:
        Add = 0
        traceback(0,p,n,col,downslash_lookup,upslash_lookup,colum_lookup,n-p)



    # write the result to output
    # print(Sum)
    # print(chessboard)
    f = open("output.txt", 'w')
    f.write(str(Sum))
    f.close()