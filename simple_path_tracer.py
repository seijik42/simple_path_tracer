# -*- coding: utf-8 -*-

import math
import random

PI = math.pi
INF = 1E6 # とても大きい数字
EPS = 1E-6 # とても小さい数字
MAX_DEPTH = 5 # 光線の最大反射・屈折深さ

REFLECTION_TYPE = {
    'DIFFUSE': 0,
    'SPECULAR': 1,
    'REFRACTION': 2,
}

def clamp(x):
    "値を0から1の間に収める関数"
    if x < 0:
        return 0
    elif x > 1:
        return 1
    else:
        return x


class Vector():
    "3次元のベクトルを表すクラス"

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, vec_b):
        return Vector(self.x+vec_b.x, self.y+vec_b.y, self.z+vec_b.z)

    def __sub__(self, vec_b):
        return Vector(self.x-vec_b.x, self.y-vec_b.y, self.z-vec_b.z)

    def __mul__(self, scalar):
        return Vector(self.x*scalar, self.y*scalar, self.z*scalar)

    def __div__(self, scalar):
        return Vector(self.x/scalar, self.y/scalar, self.z/scalar)

    def get_length_squared(self):
        return (self.x**2 + self.y**2 + self.z**2)

    def get_length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def dot(self, vec_b):
        "内積を計算して返す関数"
        return (self.x*vec_b.x + self.y*vec_b.y + self.z*vec_b.z)

    def cross(self, vec_b):
        "外積を計算して返す関数"
        return Vector(
            (self.y*vec_b.z - self.z*vec_b.y),
            (self.z*vec_b.x - self.x*vec_b.z),
            (self.x*vec_b.y - self.y*vec_b.x),
        )

    def multiply(self, vec_b):
        return Vector(
            self.x * vec_b.x,
            self.y * vec_b.y,
            self.z * vec_b.z,
        )

    def normalize(self):
        "法線ベクトルを計算して返す関数"
        return Vector(self.x, self.y, self.z) / self.get_length()


class Color(Vector):
    "r,g,bを3次元のベクトルx,y,zにマッピングして表すクラス"
    pass

BACKGROUND_COLOR = Color(0.0, 0.0, 0.0)

class Ray():
    "光線を表現するクラス"
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

class Sphere():
    "球を表現するクラス"

    def __init__(
        self, radius, position, emission, color, reflection_type,
    ):
        self.radius = radius
        self.position = position
        self.emission = emission
        self.color = color
        self.reflection_type = reflection_type

    def intersect(self, ray):
        "球と光線が交差したとき、交差場所への距離を返す"
        origin_to_position = self.position - ray.origin
        b = origin_to_position.dot(ray.direction)
        det = b**2 - origin_to_position.dot(origin_to_position) + self.radius**2
        if det >= 0.0:
            sqrt_det = math.sqrt(det)
            t1 = b - sqrt_det
            t2 = b + sqrt_det
            if t1 > EPS:
                return t1
            elif t2 > EPS:
                return t2
        return 0.0

# シーンをすべて球で構成する
spheres = [
    Sphere(1E5, Vector( 1E5+1,40.8,81.6), Color(), Color(0.75, 0.25, 0.25), REFLECTION_TYPE['DIFFUSE']),# 左
    Sphere(1E5, Vector(-1E5+99,40.8,81.6),Color(), Color(0.25, 0.75, 0.25), REFLECTION_TYPE['DIFFUSE']),# 右
    Sphere(1E5, Vector(50,40.8, 1E5),     Color(), Color(0.75, 0.75, 0.75), REFLECTION_TYPE['DIFFUSE']),# 奥
    Sphere(1E5, Vector(50,40.8,-1E5+250), Color(), Color(),                 REFLECTION_TYPE['DIFFUSE']),# 手前
    Sphere(1E5, Vector(50, 1E5, 81.6),    Color(), Color(0.75, 0.75, 0.75), REFLECTION_TYPE['DIFFUSE']),# 床
    Sphere(1E5, Vector(50,-1E5+81.6,81.6),Color(), Color(0.75, 0.75, 0.75), REFLECTION_TYPE['DIFFUSE']),# 天井
    Sphere(20.0,Vector(65,20  ,20),       Color(), Color(0.25, 0.25, 0.75), REFLECTION_TYPE['DIFFUSE']),# 青球
    Sphere(16.5,Vector(27,16.5,47),       Color(), Color(0.99, 0.99, 0.99), REFLECTION_TYPE['SPECULAR']),# 鏡
    Sphere(16.5,Vector(77,16.5,78),       Color(), Color(0.99, 0.99, 0.99), REFLECTION_TYPE['REFRACTION']),#ガラス
    Sphere(15.0, Vector(50.0, 90.0, 81.6),Color(12,12,12), Color(),        REFLECTION_TYPE['DIFFUSE']),#照明
]

def get_intersect_obj(spheres, ray):
    "シーンと交際するか判定する"
    n = len(spheres)
    distance = INF
    obj_id = -1
    for i in range(n):
        d = spheres[i].intersect(ray)
        if 0.0 < d < distance:
            distance = d
            obj_id = i
    return (obj_id, distance)

def _calc_diffuse(obj, depth, hitpoint, orienting_normal, russian_roulette_probability):
    "diffuseマテリアルにおけるradianceの計算"
    w = orienting_normal
    if math.fabs(w.x > 0.1):
        u = Vector(0.0, 1.0, 0.0).cross(w).normalize()
    else:
        u = Vector(1.0, 0.0, 0.0).cross(w).normalize()
    v = w.cross(u)
    r1 = 2 * PI * random.random()
    r2 = random.random()
    r2s = math.sqrt(r2)
    direction = (u * math.cos(r1) * r2s + v * math.sin(r1) * r2s + w * math.sqrt(1.0 - r2)).normalize()
    return obj.emission + obj.color.multiply(
        radiance(Ray(hitpoint, direction), depth+1) / russian_roulette_probability
    )


def _calc_specular(ray, obj, depth, hitpoint, normal, russian_roulette_probability):
    "specularマテリアルにおけるradianceの計算"
    return obj.emission + obj.color.multiply(
        radiance(Ray(hitpoint, ray.direction - normal * 2.0 * normal.dot(ray.direction)), depth+1) / russian_roulette_probability
    )

def _calc_refraction(ray, obj, depth, hitpoint, normal, orienting_normal, russian_roulette_probability):
    "reflactionマテリアルにおけるradianceの計算"
    reflection_ray = Ray(hitpoint, ray.direction - normal * 2.0 * normal.dot(ray.direction))
    # 光線がオブジェクトから出ようとしているのか入ろうとしているのかを調べる
    into = normal.dot(orienting_normal) > 0.0
    # 屈折の方向を計算
    NC = 1.0
    NT = 1.5
    nnt = NC / NT if into else NT / NC
    ddn = ray.direction.dot(orienting_normal)
    cos2t = 1.0 - nnt**2 * (1.0 - ddn**2)

    if (cos2t < 0.0):
        # 全反射
        return obj.emission + obj.color.multiply(
            radiance(reflection_ray, depth + 1)
        ) / russian_roulette_probability
    tdir = ray.direction * nnt - normal * (1.0 if into else -1.0) * (ddn * nnt + math.sqrt(cos2t))

    # Schlickの近似式
    r0 = (NT - NC)**2 / (NT + NC)**2
    c = 1.0 - (-ddn if into else tdir.dot(normal))
    re = r0 + (1.0 - r0) * c**5
    tr = 1.0 - re
    probability = 0.25 + 0.5 * re

    # 一定以上光線を追跡したら、屈折と反射のどちらかに追跡を絞る
    if (depth > 2):
       if random.random() < probability:
            return obj.emission + obj.color.multiply(
                radiance(reflection_ray, depth + 1) * re
            ) / probability / russian_roulette_probability
       else:
            return obj.emission + obj.color.multiply(
                radiance(Ray(hitpoint, tdir), depth + 1) * tr
            ) / (1.0 - probability) / russian_roulette_probability
    else:
        # 屈折と反射の療法を追跡
        return obj.emission + obj.color.multiply(
            radiance(reflection_ray, depth+1) * re + radiance(Ray(hitpoint, tdir), depth + 1) * tr
        ) / russian_roulette_probability



def radiance(ray, depth):
    "ray方向からの放射輝度を求める"
    obj_id, distance = get_intersect_obj(spheres, ray)
    if (distance >= INF ):
        return BACKGROUND_COLOR
    obj = spheres[obj_id]
    hitpoint = ray.origin + ray.direction * distance
    normal = (hitpoint - obj.position).normalize()
    orienting_normal = normal if normal.dot(ray.direction) < 0.0 else normal * -1.0
    # ロシアンルーレットで、追跡を打ち切るかを判断する
    russian_roulette_probability = max(obj.color.x, obj.color.y, obj.color.z)
    if depth > MAX_DEPTH:
        if random.random() >= russian_roulette_probability:
            return obj.emission
    else:
        russian_roulette_probability = 1.0

    if obj.reflection_type == REFLECTION_TYPE['DIFFUSE']:
        return _calc_diffuse(obj, depth, hitpoint, orienting_normal, russian_roulette_probability)
    elif obj.reflection_type == REFLECTION_TYPE['SPECULAR']:
        return _calc_specular(ray, obj, depth, hitpoint, normal, russian_roulette_probability)
    elif obj.reflection_type == REFLECTION_TYPE['REFRACTION']:
        return _calc_refraction(ray, obj, depth, hitpoint, normal, orienting_normal, russian_roulette_probability)

def save_ppm(filename, image, width, height):
    "ppm形式で画像を書き出す"
    COLOR_RANGE = 255
    header = "P3\n{width} {height}\n{color_range}\n".format(
        width=width, height=height, color_range=COLOR_RANGE
    )
    with open(filename, 'w') as fh:
        fh.write(header)
        for pixel in image:
            fh.write(
                '{r} {g} {b} '.format(
                    r=int(clamp(pixel.x)*255),
                    g=int(clamp(pixel.y)*255),
                    b=int(clamp(pixel.z)*255),
                )
            )

def main():
    width = 640
    height = 480

    samples = 1024

    # カメラ位置
    camera = Ray(Vector(50.0, 52.0, 295.6), Vector(0.0, -0.042612, -1.0).normalize())
    # シーン内でのスクリーンのx軸、y軸ベクトル
    screen_axis_x = Vector(width * 0.5135 / height)
    screen_axis_y = screen_axis_x.cross(camera.direction).normalize() * 0.5135
    image = [Color() for i in range(width*height)]

    for y in range(height):
        print 'pixel:', y
        for x in range(width):
            image_index = y * width + x
            # 2x2のサブピクセルサンプリング
            for sub_y in range(2):
                for sub_x in range(2):
                    # モンテカルロ法により、radianceを蓄積していく
                    accumulated_radiance = Color()
                    # サプビクセルあたり、samples数回サンプリングを行う
                    for sample in range(samples):
                        dy = sub_y / 2.0
                        dx = sub_x / 2.0
                        direction = screen_axis_x * (
                            ((sub_x+0.5+dx) / 2.0+x) / width - 0.5
                        ) + (
                            screen_axis_y * (
                                ((sub_y + 0.5 + dy) / 2.0 + y) / height - 0.5
                            )
                        ) + camera.direction
                        
                        accumulated_radiance = accumulated_radiance + radiance(
                            Ray(camera.origin + direction * 130.0, direction.normalize()), 0
                        ) / samples
                    image[image_index] = image[image_index] + accumulated_radiance
    save_ppm('output.ppm', image, width, height)


if __name__ == '__main__':
    main()
