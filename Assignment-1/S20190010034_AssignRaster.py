from OpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from PIL import Image, ImageOps
import random

class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

class Line:
    # ax+by+c = 0 line
    def __init__(self, *args) -> None:
        point1 = args[0]
        if isinstance(args[1], float) or isinstance(args[1], int):
            self.a = args[1]
            self.b = -1
            self.c = point1.y - args[1]*point1.x
            self.slope = args[1]
        else:
            point2 = args[1]
            self.slope = (point2.y - point1.y)/float(point2.x-point1.x)
            self.c = point1.y - self.slope * point1.x
            self.b = -1
            self.a = self.slope

    @staticmethod
    def intersection(line1, line2):
        if line1.slope == line2.slope:
            return None
        x = (line1.b*line2.c - line2.b*line1.c)/float(line1.a*line2.b-line2.a*line1.b)
        y = (line1.c*line2.a - line2.c*line1.a)/float(line1.a*line2.b-line2.a*line1.b)
        return Point(x,y)

class Triangle:
    def __init__(self, point1: Point, point2: Point, point3: Point) -> None:
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
    
    @staticmethod
    def area(point1, point2, point3) -> int:
        return abs(
            point1.x * (point2.y - point3.y) + point2.x * (point3.y - point1.y) + point3.x  * (point1.y - point2.y)
        )

    def isInside(self, point: Point) -> bool:
        area = Triangle.area(self.point1, self.point2, self.point3)
        area1 = Triangle.area(self.point1, self.point2, point)
        area2 = Triangle.area(point, self.point2, self.point3)
        area3 = Triangle.area(self.point1, point, self.point3)
        return area == (area1 + area2 + area3)

class Rasterization:

    SPECIFY_COORDINATES = lambda x,y: glVertex2f(x, y)
    SWAP = lambda x,y: (y,x)

    @classmethod
    def save_png(cls, data: list, filename: str):
        image = Image.frombytes("RGB", (300,300), data)
        image = ImageOps.flip(image)
        image.save(filename, "PNG")

    @classmethod
    def BresenhamsAlgorithm(cls, point1: Point, point2: Point):
        x1,x2 = point1.x, point2.x
        y1,y2 = point1.y, point2.y

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        incx = 1 if x2>x1 else -1
        incy = 1 if y2>y1 else -1
        x,y = x1,y1
        if dx>dy:
            cls.SPECIFY_COORDINATES(x,y)
            e = 2*dy - dx
            inc1 = 2*(dy-dx)
            inc2 = 2*dy;
            i = 0
            while i<dx:
                if e>=0:
                    y+=incy
                    e+=inc1
                else:
                    e+=inc2
                x+=incx
                cls.SPECIFY_COORDINATES(x,y)
                i+=1 
        else:
            cls.SPECIFY_COORDINATES(x,y)
            e = 2*dx - dy
            inc1 = 2*(dx-dy)
            inc2 = 2*dx;
            i = 0
            while i<dy:
                if e>=0:
                    x+=incx
                    e+=inc1
                else:
                    e+=inc2
                y+=incy
                cls.SPECIFY_COORDINATES(x,y)
                i+=1
        
       

    @classmethod
    def get_points_on_line(cls, point1, point2):
        points = []
        x1,x2 = point1.x, point2.x
        y1,y2 = point1.y, point2.y

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        incx = 1 if x2>x1 else -1
        incy = 1 if y2>y1 else -1
        x,y = x1,y1
        if dx>dy:
            points.append(Point(x,y))
            e = 2*dy - dx
            inc1 = 2*(dy-dx)
            inc2 = 2*dy;
            i = 0
            while i<dx:
                if e>=0:
                    y+=incy
                    e+=inc1
                else:
                    e+=inc2
                x+=incx
                points.append(Point(x,y))
                i+=1 
        else:
            points.append(Point(x,y))
            e = 2*dx - dy
            inc1 = 2*(dx-dy)
            inc2 = 2*dx;
            i = 0
            while i<dy:
                if e>=0:
                    x+=incx
                    e+=inc1
                else:
                    e+=inc2
                y+=incy
                points.append(Point(x,y))
                i+=1
        return points

    @classmethod
    def sample_points(cls, sample_frequency):
        sample_points = []
        for _ in range(sample_frequency):
            x,y = random.randint(0,500), random.randint(0,400)
            sample_points.append(Point(x,y))
        return sample_points

    @classmethod
    def super_sampling(cls, ):
        points = []
        for _ in range(100):
            x = random.randint(1000,5000)
            points.extend(cls.sample_points(x))
        return points
                
    @classmethod
    def DrawLine(cls):

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glBegin(GL_POINTS)
        glColor(255, 255, 0)

        point1, point2 = Point(50,50), Point(350,350)
        cls.BresenhamsAlgorithm(point1, point2)
        glEnd()
        glutSwapBuffers()

    
    @classmethod
    def DrawTriangle(cls):
        point1, point2, point3 = Point(50,50), Point(250,250), Point(300,50)
        glClear(GL_COLOR_BUFFER_BIT)
        glColor(255, 255, 0)
        glBegin(GL_POINTS)

        triangle = cls.get_points_on_line(point1, point2)
        slope = (point2.y - point1.y)/float(point2.x-point1.x)
        points = cls.get_points_on_line(point1, point3)
        line = Line(point2, point3)
        triangle.extend(points)
        for point in points:
            temp_line = Line(point, slope)
            target = Line.intersection(line, temp_line)
            triangle.extend(cls.get_points_on_line(point, target))
        for point in triangle:
            cls.SPECIFY_COORDINATES(point.x, point.y)

        glEnd()
        glFlush()

    @classmethod
    def DrawAntiAliasedTriangle(cls,):
        triangle = Triangle(Point(100,100), Point(250,300), Point(400,100))

        glClear(GL_COLOR_BUFFER_BIT)
        glColor(255, 255, 0)
        glBegin(GL_POINTS)
        anti_aliased_points = cls.super_sampling()
        for point in anti_aliased_points:
            if triangle.isInside(point):
                cls.SPECIFY_COORDINATES(point.x, point.y)
        glEnd()
        glFlush()

    @classmethod
    def displayLine(cls,):
        glutInitWindowSize(300, 300)
        glutCreateWindow(b'Line')
        glutPositionWindow(0, 0)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        gluOrtho2D(0.0, 500.0, 0.0, 400.0)
        cls.DrawLine()
        data = glReadPixels(0,0,300,300,GL_RGB,GL_UNSIGNED_BYTE)
        cls.save_png(data, "line.png")
        glutDisplayFunc(cls.DrawLine)

    @classmethod
    def displayTriangle(cls,):
        glutInitWindowSize(300, 300)
        glutCreateWindow(b'Triangle')
        glutPositionWindow(301, 0)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        gluOrtho2D(0.0, 500.0, 0.0, 400.0)
        cls.DrawTriangle()
        data = glReadPixels(0,0,300,300,GL_RGB,GL_UNSIGNED_BYTE)
        cls.save_png(data, "triangle.png")
        glutDisplayFunc(cls.DrawTriangle)

    @classmethod
    def displayAntiAliasedTriangle(cls,):
        glutInitWindowSize(300, 300)
        glutCreateWindow(b'Anti Aliased Triangle')
        glutPositionWindow(601, 0)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        gluOrtho2D(0.0, 500.0, 0.0, 400.0)
        cls.DrawAntiAliasedTriangle()
        data = glReadPixels(0,0,300,300,GL_RGB,GL_UNSIGNED_BYTE)
        cls.save_png(data, "anti_aliasing.png")
        glutDisplayFunc(cls.DrawAntiAliasedTriangle)

    @classmethod
    def main(cls):
        glutInit()
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        cls.displayLine()
        cls.displayTriangle()
        cls.displayAntiAliasedTriangle()
        glutMainLoop()

Rasterization.main()
