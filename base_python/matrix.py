from __future__ import division
from functools import wraps
from math import cos, sin, pi

def make_translate( x, y, z ):
    matrix = new_matrix()
    ident(matrix)
    matrix[0][3] = x
    matrix[1][3] = y
    matrix[2][3] = z
    return matrix

def make_scale( x, y, z ):
    matrix = new_matrix()
    ident(matrix)
    matrix[0][0] = x
    matrix[1][1] = y
    matrix[2][2] = z
    return matrix

def deg_to_radians(function):
    @wraps(function)
    def convert(degree_measure):
        return function((pi / 180) * degree_measure)
    return convert

@deg_to_radians
def make_rotX( theta ):
    matrix = new_matrix()
    ident(matrix)
    matrix[1][1] = cos(theta)
    matrix[1][2] = sin(theta)
    matrix[2][1] = -sin(theta)
    matrix[2][2] = cos(theta)
    return matrix

@deg_to_radians
def make_rotY( theta ):
    matrix = new_matrix()
    ident(matrix)
    matrix[0][0] = cos(theta)
    matrix[0][3] = -sin(theta)
    matrix[3][0] = sin(theta)
    matrix[3][3] = cos(theta)
    return matrix

@deg_to_radians
def make_rotZ( theta ):
    matrix = new_matrix()
    ident(matrix)
    matrix[0][0] = cos(theta)
    matrix[0][1] = sin(theta)
    matrix[1][0] = -sin(theta)
    matrix[1][1] = cos(theta)
    return matrix

def print_matrix( matrix ):
    s = ''
    for r in range( len( matrix[0] ) ):
        for c in range( len(matrix) ):
            s+= str(matrix[c][r]) + ' '
            s+= '\n'
            print s

def ident( matrix ):
    for r in range( len( matrix[0] ) ):
        for c in range( len(matrix) ):
            if r == c:
                matrix[c][r] = 1
            else:
                matrix[c][r] = 0

def scalar_mult( matrix, s ):
    matrix[:] = [[s * matrix[row][col] for col in xrange(len(matrix[row]))] for row in xrange(len(matrix))]
            
def tranpose(matrix):
    new_matrix = [[matrix[row][col] for row in xrange(len(matrix))] for col in xrange(len(matrix[0]))]
    return new_matrix

#m1 * m2 -> m2
def matrix_mult( m1, m2 ):
    m2_tranposed = tranpose(m2)
    
    for i in xrange(len(m1)):
        for j in xrange(len(m2_tranposed)):
            m2[i][j] = sum([(elem1 * elem2) for elem1, elem2 in zip(m1[i], m2_tranposed[j])])
            
def new_matrix(rows = 4, cols = 4):
    m = []
    for c in range( cols ):
        m.append( [] )
        for r in range( rows ):
            m[c].append( 0 )
    return m
