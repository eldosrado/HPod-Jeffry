import math
import numpy


class vector(object):
    __slots__ = ('x', 'y', 'z')

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def angle(self, vec):
        return math.acos(self.dot(vec))

    def cross(self, vec):
        x = ((self.y * vec.z) - (self.z * vec.y))
        y = ((self.z * vec.x) - (self.x * vec.z))
        z = ((self.x * vec.y) - (self.y * vec.x))
        return vector(x, y, z)

    def dot(self, vec):
        return float(self.x * vec.x + self.y * vec.y + self.z * vec.z)

    def zero(self):
        self.x = self.y = self.z = 0.0

    def identity(self):
        self.zero()

    def clear(self, value):
        self.x = self.y = self.z = value

    def normalize(self):
        ln = self.length()

        if ln == 0:
            return

        self.x /= ln
        self.y /= ln
        self.z /= ln

    def length(self):
        return math.sqrt((self.x**2) + (self.y**2) + (self.z**2))

    def length_squared(self):
        return (self.x * self.x) + (self.y * self.y) + (self.z * self.z)

    def as_tuple(self):
        return (self.x, self.y, self.z)

    def as_list(self):
        return [self.x, self.y, self.z]

    def as_dictionary(self):
        return {'x': self.x, 'y': self.y, 'z': self.z}

    def as_np_array(self):
        return numpy.array([self.x, self.y, self.z])

    def as_np_matrix(self):
        return numpy.matrix([self.x, self.y, self.z])

        # # Overloads ##

    def __str__(self):
        return 'vector( %.3f, %.3f, %.3f )' % ( self.x, self.y, self.z )

    def __repr__(self):
        return str(self)

    def __eq__(self, v):
        return self.x == v.x and self.y == v.y and self.z == v.z

    def __cmp__(self, v):
        return self.__eq__(v)

    def __ne__(self, v):
        return not self.__eq__(v)

    def __lt__(self, v):
        if self.x < v.x:
            return True

        if self.y < v.y:
            return True

        if self.z < v.z:
            return True

    def __le__(self, v):
        if self.x <= v.x:
            return True

        if self.y <= v.y:
            return True

        if self.z <= v.z:
            return True

    def __gt__(self, v):
        if self.x > v.x:
            return True

        if self.y > v.y:
            return True

        if self.z > v.z:
            return True

    def __ge__(self, v):
        if self.x >= v.x:
            return True

        if self.y >= v.y:
            return True

        if self.z >= v.z:
            return True

    def __add__(self, v):
        if isinstance(v, vector):
            return vector(self.x + v.x, self.y + v.y, self.z + v.z)
        else:
            return vector(self.x + v, self.y + v, self.z + v)

    def __sub__(self, v):
        if isinstance(v, vector):
            return vector(self.x - v.x, self.y - v.y, self.z - v.z)
        else:
            return vector(self.x - v, self.y - v, self.z - v)

    def __truediv__(self, v):
        if isinstance(v, vector):
            return vector(self.x / v.x, self.y / v.y, self.z / v.z)
        else:
            return vector(self.x / v, self.y / v, self.z / v)

    def __mul__(self, v):
        if isinstance(v, vector):
            return vector(self.x * v.x, self.y * v.y, self.z * v.z)
        else:
            return vector(self.x * v, self.y * v, self.z * v)

    def __neg__(self):
        return vector(-self.x, -self.y, -self.z)
