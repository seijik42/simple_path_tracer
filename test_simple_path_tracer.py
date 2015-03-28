import unittest
import math
import simple_path_tracer
from simple_path_tracer import Vector, Color, Ray, Sphere

class SimplePathTracertest(unittest.TestCase):

    def test_clamp(self):
        self.assertEqual(simple_path_tracer.clamp(0.5), 0.5)
        self.assertEqual(simple_path_tracer.clamp(0.0), 0.0)
        self.assertEqual(simple_path_tracer.clamp(1), 1.0)
        self.assertEqual(simple_path_tracer.clamp(1.1), 1.0)
        self.assertEqual(simple_path_tracer.clamp(-1.0), 0.0)

class VectorTest(unittest.TestCase):

    def test_add(self):
        sum_vec = Vector(1.0, 1.0, 1.0) + Vector(2.0, 2.0, 2.0)
        self.assertEqual(sum_vec.x, 3.0)
        self.assertEqual(sum_vec.y, 3.0)
        self.assertEqual(sum_vec.z, 3.0)

    def test_sub(self):
        sum_vec = Vector(2.0, 2.0, 2.0) - Vector(1.0, 1.0, 1.0)
        self.assertEqual(sum_vec.x, 1.0)
        self.assertEqual(sum_vec.y, 1.0)
        self.assertEqual(sum_vec.z, 1.0)
 
    def test_mul(self):
        sum_vec = Vector(2.0, 2.0, 2.0) * 3.0
        self.assertEqual(sum_vec.x, 6.0)
        self.assertEqual(sum_vec.y, 6.0)
        self.assertEqual(sum_vec.z, 6.0)
  
    def test_div(self):
        sum_vec = Vector(2.0, 2.0, 2.0) / 2.0
        self.assertEqual(sum_vec.x, 1.0)
        self.assertEqual(sum_vec.y, 1.0)
        self.assertEqual(sum_vec.z, 1.0)

    def test_get_length_squared(self):
        vec = Vector(2.0, 2.0, 2.0)
        self.assertEqual(vec.get_length_squared(), 12.0)

    def test_get_length(self):
        vec = Vector(2.0, 2.0, 2.0)
        self.assertEqual(vec.get_length(), math.sqrt(12.0))

    def test_dot(self):
        self.assertEqual(Vector(2.0, 2.0, 2.0).dot(Vector(1.0,1.0,1.0)), 6.0)

    def test_cross(self):
        result = Vector(0.0, 0.0, 1.0).cross(Vector(0.0,1.0,0.0))
        self.assertEqual(result.x, -1.0)
        self.assertEqual(result.y, 0.0)
        self.assertEqual(result.z, 0.0)

    def test_multiply(self):
        result = Vector(1.0, 2.0, 3.0).multiply(Vector(2.0, 2.0, 2.0))
        self.assertEqual(result.x, 2.0)
        self.assertEqual(result.y, 4.0)
        self.assertEqual(result.z, 6.0)

    def test_normalize(self):
        self.assertEqual(Vector(1.0, 1.0, 2.0).normalize().get_length(),1.0)

class ColorTest(unittest.TestCase):

    def test_init_default(self):
        color = Color()
        self.assertEqual(color.x, 0.0)
        self.assertEqual(color.y, 0.0)
        self.assertEqual(color.z, 0.0)

    def test_init(self):
        color = Color(1.0, 2.0, 3.0)
        self.assertEqual(color.x, 1.0)
        self.assertEqual(color.y, 2.0)
        self.assertEqual(color.z, 3.0)

class RayTest(unittest.TestCase):

    def test_init(self):
        origin = Vector(1.0, 1.0, 1.0)
        direction = Vector(1.0, 2.0, 3.0)
        ray = Ray(origin, direction)
        self.assertEqual(ray.origin, origin)
        self.assertEqual(ray.direction, direction)

class SphereTest(unittest.TestCase):

    def test_intersect(self):
        sphere = Sphere(1.0, Vector(0.0, 0.0, 0.0), Color(), Color(1.0, 1.0, 1.0), 1)
        ray = Ray(Vector(10.0, 0.0, 0.0), Vector(-1.0, 0.0, 0.0))
        self.assertEqual(sphere.intersect(ray), 9.0)
