# Math Library
# Author: Martín España

from collections import namedtuple
from math import sin, cos, acos, asin, atan, atan2

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])

pi = 3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067
decimalPrecision = 10

# Adds points on 2 dimensional space
def add(A, B):
    if type(A) == int and type(B) == int:
        return A + B
    elif type(A) == float and type(B) == float:
        return A + B
    elif len(A) == 2 and len(B) == 2:
        return V2(A.x + B.x, A.y + B.y)
    elif len(A) == 3 and len(B) == 3:
        return V3(A.x + B.x, A.y + B.y, A.z + B.z)
    elif len(A) == 4 and len(B) == 4:
        return V4(A.x + B.x, A.y + B.y, A.z + B.z, A.w + B.w)

def subtract(A, B):
    if type(A) == int and type(B) == int:
        return A - B
    elif type(A) == float and type(B) == float:
        return A - B
    elif len(A) == 2 and len(B) == 2:
        return V2(A.x - B.x, A.y - B.y)
    elif len(A) == 3 and len(B) == 3:
        return V3(A.x - B.x, A.y - B.y, A.z - B.z)
    elif len(A) == 4 and len(B) == 4:
        return V4(A.x - B.x, A.y - B.y, A.z - B.z, A.w - B.w)

def scalarVec(scalar, vector):
    if len(vector) == 2:
        answer = V2(scalar * vector.x, scalar * vector.y)
        return answer
    elif len(vector) == 3:
        answer = V3(scalar * vector.x, scalar * vector.y, scalar * vector.z)
        return answer
    elif len(vector) == 4:
        answer = V4(scalar * vector.x, scalar * vector.y, scalar * vector.z, scalar * vector.w)
        return answer

def dot(A, B):
    if len(A) == 2 and len(B) == 2:
        return A.x * B.x + A.y * B.y
    elif len(A) == 3 and len(B) == 3:
        return A.x * B.x + A.y * B.y + A.z * B.z
    elif len(A) == 4 and len(B) == 4:
        return A.x * B.x + A.y * B.y + A.z * B.z + A.w * B.w

def dotArray(arrayOne, arrayTwo):
    if len(arrayOne) != len(arrayTwo):
        return
    
    result = 0

    for i in range(len(arrayOne)):
        result += round(arrayOne[i] * arrayTwo[i], decimalPrecision)
    
    return result

def cross(A, B):
    i = ((A.y * B.z) - (A.z * B.y))
    j = -((A.x * B.z) - (A.z * B.x))
    k = ((A.x * B.y) - (A.y * B.x))
    product = V3(i, j, k)
    return product

def magnitude(A):
    if len(A) == 2:
        return sqroot(A.x * A.x + A.y * A.y)
    elif len(A) == 3:
        return sqroot(A.x * A.x + A.y * A.y + A.z * A.z)
    elif len(A) == 4:
        return sqroot(A.x * A.x + A.y * A.y + A.z * A.z + A.w * A.w)

# def sqroot(dividend, maxPrecision = None):
    
#     if maxPrecision:
#         maxPreci = maxPrecision
#     else:
#         maxPreci = decimalPrecision

#     isImaginarian = False

#     def decimalCount(num):
#         if str(num).find(".") >= 0:
#             decimals = str(num).split(".")
#             return len(decimals[1])
#         elif str(num).find(".") < 0:
#             return 0

#     if dividend < 0:
#         dividend = abs(dividend)
#         isImaginarian = True

#     if dividend == 0:
#         return 0
#     elif 0 < abs(dividend) < 10:
#         divisor = 1.1
#     elif 10 <= abs(dividend) < 10000:
#         divisor = 10
#     elif 10000 <= abs(dividend) < 1000000:
#         divisor = 100
#     else:
#         divisor = 1000
    
#     done = False

#     while not done:
#         quotient = dividend / divisor
#         precision = min(decimalCount(quotient), decimalCount(divisor))
#         if precision > maxPreci:
#             precision = maxPreci
        
#         if round(quotient, precision) < round(divisor, precision):
#             divisor -= ((divisor - quotient) / 2)
#         elif round(quotient, precision) > round(divisor, precision):
#             divisor += ((quotient - divisor) / 2)
#         elif round(quotient, precision) == round(divisor, precision):
#             done = True
#             if isImaginarian:
#                 return str(round(quotient, precision)) + " i"
#             elif not isImaginarian:
#                 return round(quotient, precision)

def sqroot(dividend):
    return pow(dividend, 0.5)

def power(base, exp):
    # TODO 
    # This is functional but can do better
    result = 1
    while exp > 0:
        result = result * base
        exp -= 1
    return result

def normalize(vector):
    if len(vector) == 2:
        mag = sqroot(vector.x * vector.x + vector.y * vector.y)
        if mag != 0:
            unitVec = V2(vector.x / mag, vector.y / mag)
        else:
            unitVec = V2(0,0)
        return unitVec
    elif len(vector) == 3:
        mag = sqroot(vector.x * vector.x + vector.y * vector.y + vector.z * vector.z)
        if mag != 0:
            unitVec = V3(vector.x / mag, vector.y / mag, vector.z / mag)
        else:
            unitVec = V3(0,0,0)
        return unitVec
    elif len(vector) == 4:
        mag = sqroot(vector.x * vector.x + vector.y * vector.y + vector.z * vector.z + vector.w * vector.w)
        if mag != 0:
            unitVec = V4(vector.x / mag, vector.y / mag, vector.z / mag, vector.w / mag)
        else:
            unitVec = V3(0,0,0)
        return unitVec

def sine(deg):
    return round(sin(radians(deg)), decimalPrecision)

def cosine(deg):
    return round(cos(radians(deg)), decimalPrecision)

def tangent(deg):
    if cosine(deg) == 0:
        return
    else:
        return sine(deg) / cosine(deg)

def arcsine(deg):
    return asin(radians(deg))

def arccosine(deg):
    return acos(deg)

def arctangent(deg):
    return atan(radians(deg))

def arctangent2(y, x):
    return atan2(y, x)

def degrees(rad):
    return (rad * 180) / pi

def radians(deg):
    return (deg * pi) / 180

def idMatrix(dimension):
    mat = []

    if dimension > 0:
        for n in range(dimension):
            mat.append([])
            for m in range(dimension):
                if n == m:
                    mat[n].append(1)
                else:
                    mat[n].append(0)
    
    return mat

# Tries to add two matrix, returns -1 if dimensions are not correct
def addMatrix(A, B):

    # Checks the type of the params
    if type(A) != list or type(B) != list:
        return -1

    rowA = len(A)
    rowB = len(B)

    # Gets sure the matrix sent have content
    if rowA <= 0 or rowB <= 0:
        return -1
    
    colA = len(A[0])
    colB = len(B[0])

    # Gets sure the matrix dimensions are correct
    if rowA != rowB or colA != colB:
        return -1
    else:
        rows = rowA
        cols = colA
    
    result = []

    for row in range(rows):
        result.append([])
        for col in range(cols):
            result[row].append(A[row][col] + B[row][col])

    return result

def multMatrix(A, B):
    # Checks the type of the params is OK
    if type(A) != list or type(B) != list:
        return -1
    
    # Checks there is content in both matrix's rows
    if len(A) <= 0 or len(B) <= 0:
        return -1
    
    # Checks there is content in both matrix's cols
    if len(A[0]) <= 0 or len(B[0]) <= 0:
        return -1
    
    # Checks if the dimensions are correct (m x n * n x r)
    rowA = len(A)
    colA = len(A[0])
    rowB = len(B)
    colB = len(B[0])

    if colA != rowB:
        return -1

    result = []
    Btrans = transposeMatrix(B)

    for row in range(rowA):
        result.append([])
        for col in range(colB):
            result[row].append(dotArray(A[row], Btrans[col]))
    
    return result

def scalarMultMatrix(scalar, matrix):
    # Checks the type of the params is OK
    if (type(scalar) != int and type(scalar) != float) or type(matrix) != list:
        return -1
    
    # Checks there is content in the matrix's rows
    if len(matrix) <= 0:
        return -1
    
    # Checks there is content in the matrix's cols
    if len(matrix[0]) <= 0:
        return -1

    result = []

    for row in range(len(matrix)):
        result.append([])
        for col in range(len(matrix)):
            result[row].append(round(scalar * matrix[row][col], decimalPrecision))
    
    return result


# Tries to return the matrix's transpose, else returns -1
def transposeMatrix(original):
    
    if type(original) != list:
        return -1
    if len(original) <= 0:
        return -1
    if len(original[0]) <= 0:
        return -1
    
    rowCount = len(original)
    colCount = len(original[0])

    trans = []

    for row in range(colCount):
        trans.append([])
        for col in range(rowCount):
            # Switch rows for columns
            trans[row].append(original[col][row])
    
    return trans

def isSquareMatrix(matrix):
    # Correct type
    if type(matrix) != list:
        return False
    # Correct row's content
    if len(matrix) <= 0:
        return False
    # Correct col's content
    if len(matrix[0]) <= 0:
        return False
    # Correct dimensions (must be a square matrix)
    if len(matrix) != len(matrix[0]):
        return False
    elif len(matrix) == len(matrix[0]):
        return True

def detMatrix(matrix):
    # Checks if the param sent is a square matrix
    if not isSquareMatrix(matrix):
        return
    
    # Calculates the determinant of a 2x2 matrix
    def calcTwoDim(mat):
        det = mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]
        return det

    # Find matrix's dimension
    dim = len(matrix)
    colCounter = 0

    # Matrix 1x1
    if dim == 1:
        return matrix[0][0]
    
    # Matrix 2x2
    elif dim == 2:
        return calcTwoDim(matrix)
    
    # Matrix 3x3, 4x4, 5x5, ...
    else:

        detCollection = []

        for i in range(dim):
            
            newMat = []

            for row in range(dim):
                newRow = []
                if row != 0:
                    for col in range(dim):
                        if col != colCounter:
                            newRow.append(matrix[row][col])
                    newMat.append(newRow)
            #print(newMat)
            #print("---")
            if len(newMat) == 2:
                detCollection.append(calcTwoDim(newMat))
            else:
                detCollection.append(detMatrix(newMat))
            
            colCounter += 1
        
        sign = 1
        result = 0
        
        for ind in range(dim):
            result += sign * matrix[0][ind] * detCollection[ind]
            sign = sign * -1
        
        return result

def invMatrix(matrix):
    # Checks if the param sent is a square matrix
    if not isSquareMatrix(matrix):
        return
    
    determinant = detMatrix(matrix)

    if determinant == 0:
        return

    dim = len(matrix)

    minorMatrix = []

    for r in range(dim):
        minorMatrix.append([])
        for c in range(dim):
            newMat = []
            for row in range(dim):
                newRow = []
                for col in range(dim):
                    if row != r and col != c:
                        newRow.append(matrix[row][col])
                if len(newRow) > 0:
                    newMat.append(newRow)
            minorMatrix[r].append(detMatrix(newMat))

    for row in range(dim):
        for col in range(dim):
            if (row+col)%2 == 0:
                # +
                minorMatrix[row][col] = minorMatrix[row][col] * 1
            else:
                # -
                minorMatrix[row][col] = minorMatrix[row][col] * -1
    
    cofactorMatrix = minorMatrix

    adjointMatrix = transposeMatrix(cofactorMatrix)

    inverse = scalarMultMatrix((1/determinant), adjointMatrix)

    return inverse
    
    
    


