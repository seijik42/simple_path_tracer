# -*- coding: utf-8 -*-

import math

PI = math.pi
INF = float('inf')
EPS = 1E-6
MAX_DEPTH = 5

REFLECTION_TYPE = {
    'DIFFUSE': 0,
    'SPECULAR': 1,
    'REFRACTION': 2,
}

def clamp(x):
    if x < 0:
        return 0
    elif x > 255:
        return 255
    else:
        return x


class Vector():

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def add(self, vec_b):
        return Vector(self.x+vec_b.x, self.y+vec_b.y, self.z+vec_b.z)

    def sub(self, vec_b):
        return Vector(self.x-vec_b.x, self.y-vec_b.y, self.z-vec_b.z)

    def multiply(self, scalar):
        return Vector(self.x*scalar, self.y*scalar, self.z*scalar)

    def devide(self, scalar):
        return Vector(self.x/scalar, self.y/scalar, self.z/scalar)

    def get_length_squared(self):
        return (self.x**2 + self.y**2 + self.z**2)

    def get_length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def dot(self, vec_b):
        return (self.x*vec_b.x + self.y*vec_b.y + self.z*vec_b.z)

    def cross(self, vec_b):
        return Vector(
            (self.y*vec_b.z - self.y*vec_b.y),
            (self.z*vec_b.x - self.x*vec_b.z),
            (self.x*vec_b.y - self.z*vec_b.x),
        )

    def normalize(self):
        return Vector(self.x, self.y, self.z).devide(self.get_length())


class Color(Vector):
    pass

BACKGROUND_COLOR = Color(0.0, 0.0, 0.0)

class Ray():
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

class Sphere():

    def __init__(
        self, radius, position, emission, color, reflection_type,
    ):
        self.radius = radius
        self.position = position
        self.emission = emission
        self.color = color
        self.reflection_type = reflection_type

    def intersect(self, ray):
        origin_to_position = self.position - self.origin
        b = origin_to_position.dot(ray.direction)
        det = b**2 - origin_to_postion.dot(origin_postion) + self.radius**2
        if det >= 0.0:
            sqrt_det = math.sqrt(det)
            t1 = b - sqrt_dt
            t2 = b + sqrt_dt
            if t1 > EPS:
                return t1
            elif t2 > EPS:
                return t2
            else:
                return 0.0


spheres = [
    Sphere(1E5, Vector( 1E5+1,40.8,81.6), Color(), Color(0.75, 0.25, 0.25),REFLECTION_TYPE['DIFFUSE']),# 左
    Sphere(1E5, Vector(-1E5+99,40.8,81.6),Color(), Color(0.25, 0.25, 0.75),REFLECTION_TYPE['DIFFUSE']),# 右
    Sphere(1E5, Vector(50,40.8, 1e5),     Color(), Color(0.75, 0.75, 0.75),REFLECTION_TYPE['DIFFUSE']),# 奥
    Sphere(1E5, Vector(50,40.8,-1e5+170), Color(), Color(), REFLECTION_TYPE['DIFFUSE']),# 手前
    Sphere(1E5, Vector(50, 1e5, 81.6),    Color(), Color(0.75, 0.75, 0.75),REFLECTION_TYPE['DIFFUSE']),# 床
    Sphere(1E5, Vector(50,-1e5+81.6,81.6),Color(), Color(0.75, 0.75, 0.75),REFLECTION_TYPE['DIFFUSE']),# 天井
    Sphere(16.5,Vector(27,16.5,47),       Color(), Color(1,1,1).multiply(0.99), REFLECTION_TYPE['SPECULAR']),# 鏡
    Sphere(16.5,Vector(73,16.5,78),       Color(), Color(1,1,1).multiply(0.99), REFLECTION_TYPE['REFRACTION']),#ガラス
]

def save_ppm(filename, image, width, height):
    COLOR_RANGE = 255
    header = "P3\n{width} {height}\n{color_range}\n".format(
        width=width, height=height, color_range=COLOR_RANGE
    )
    with open(filename, 'w') as fh:
        fh.write(header)
        for pixel in image:
            fh.write(
                '{r} {g} {b} '.format(
                    r=int(clamp(pixel.x)),
                    g=int(clamp(pixel.y)),
                    b=int(clamp(pixel.z)),
                )
            )

def main():
    width = 320
    height = 240

    camera = Ray(Vector(50.0, 52.0, 295.6), Vector(0.0, -0.042612, -1.0).normalize())
    screen_axis_x = Vector(width * 0.5135 / height)
    screen_axis_y = screen_axis_x.cross(camera.direction).multiply(0.5135)
    image = [Color() for i in range(width*height)]

    for y in range(height):
        for x in range(width):
            image_index = y * width + x
            for sub_x in range(2):
                for sub_y in range(2):
                    dx = sub_x / 2.0
                    dy = sub_y / 2.0
                    direction = screen_axis_x.multiply(
                        ((sub_x+0.5+dx) / 2.0+x) / width - 0.5
                    ).add(
                        screen_axis_y.multiply(
                            ((sub_y + 0.5 + dy) / 2.0 + y) / height - 0.5
                        )
                    ).add(
                        camera.direction
                    )
                    image[image_index] = image[image_index]
    save_ppm('output.ppm', image, width, height)


if __name__ == '__main__':
    main()
