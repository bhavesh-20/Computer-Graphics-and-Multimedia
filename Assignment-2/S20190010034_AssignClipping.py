from OpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

#global declarations
topleft_x,bottomright_x,topleft_y,bottomright_y=155,370,320,190
points = []

class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def getx(self):
        return self.x
    
    def gety(self):
        return self.y

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


class SutherlandHodgeman:

    @staticmethod
    def isInside(x, y, clip_edge):
        return (clip_edge == 1 and x<bottomright_x) or (clip_edge == 2 and y>bottomright_y) or (clip_edge==3 and x>topleft_x) or (clip_edge==4 and y<topleft_y)

    @staticmethod
    def findIntersection(p: Point,s: Point,clip_edge):
        m = 0 if p.getx()==s.getx() else float(p.gety()-s.gety())/float(p.getx()-s.getx())
        c=p.gety()-m*p.getx()
        if clip_edge == 1:
            return Point(bottomright_x,m*bottomright_x+c)
        elif clip_edge == 2:
            y=bottomright_y
            x = p.getx() if m==0 else (bottomright_y-c)/m
            return Point(x,y)
        elif clip_edge == 3:
            return Point(topleft_x,m*topleft_x+c)
        else:
            y=topleft_y
            x = p.getx() if m==0 else (topleft_y-c)/m
            return Point(x,y)

    @staticmethod
    def reverseClipped(out):
        temporary = []
        for i in range(len(out)):
            temporary.append([0.0,0.0])
        while len(out)>0:
            temp = out.pop(0)
            temporary[len(out)][0] = temp.getx()
            temporary[len(out)][1] = temp.gety()

        out = []
        return temporary

    @staticmethod
    def SutherlandHodgemanAlgo(clipped, out, clip_edge):
        s=Point(clipped[-1][0],clipped[-1][1])
        for i in range(len(clipped)):
            p=Point(clipped[i][0],clipped[i][1])
            if SutherlandHodgeman.isInside(p.getx(),p.gety(),clip_edge):
                if SutherlandHodgeman.isInside(s.getx(),s.gety(),clip_edge):
                    out.insert(0, Point(p.getx(),p.gety()))
                else:
                    out.insert(0,SutherlandHodgeman.findIntersection(s,p,clip_edge))
                    out.insert(0, p)
            elif SutherlandHodgeman.isInside(s.getx(),s.gety(),clip_edge):
                out.insert(0,SutherlandHodgeman.findIntersection(s,p,clip_edge))
            s=p
        clipped=SutherlandHodgeman.reverseClipped(out)
        return clipped
            


def init():
    glClearColor(1.0,1.0,1.0,1.0);
    glMatrixMode(GL_PROJECTION);
    gluOrtho2D(0,400,0,400);

def polygon():
    global inner
    glPointSize(2);
    glClear(GL_COLOR_BUFFER_BIT);
    glColor3f(1,0,0);
    inner = [
        Point(210,160),
        Point(110,220),
        Point(210,250),
        Point(210,350),
        Point(300,250),
    ]
    drawPolygon()
    glLineStipple(1, 0xAAAA);
    glColor3f(0,0,0);
    glEnable(GL_LINE_STIPPLE);
    inner = [
        Point(155,190),
        Point(155,320),
        Point(370,320),
        Point(370,190),
    ]
    drawClipper()

def drawPolygon():
    global points
    glBegin(GL_LINE_LOOP)
    for _ in range(len(inner)):
        points.append([0.0,0.0])
    while len(inner)>0:
        temp = inner.pop(0)
        points[len(inner)][0] = temp.getx()
        points[len(inner)][1] = temp.gety()
        glVertex2i(points[len(inner)][0], points[len(inner)][1])
    glEnd()
    glFlush()

def drawClipper():
    glBegin(GL_LINE_LOOP)
    for i in range(len(inner)):
        glVertex2i(inner[i].getx(), inner[i].gety())
    glEnd()
    glFlush()
    
def clip():
    global points
    outer = []
    points = SutherlandHodgeman.SutherlandHodgemanAlgo(points,outer,1)
    points = SutherlandHodgeman.SutherlandHodgemanAlgo(points,outer,2)
    points = SutherlandHodgeman.SutherlandHodgemanAlgo(points,outer,3)
    points = SutherlandHodgeman.SutherlandHodgemanAlgo(points,outer,4)

def drawClipped():
    clip()
    glPointSize(2);
    glClear(GL_COLOR_BUFFER_BIT);
    glColor3f(1,0,0);
    glBegin(GL_LINE_LOOP)
    for i in range(len(points)):
        glVertex2f(points[i][0], points[i][1])
    glEnd()
    glFlush()

def probelmWindow():
    glutInitWindowSize(400,400);
    glutInitWindowPosition(50,100);
    glutCreateWindow("Problem statement");
    glutDisplayFunc(polygon);
    init()

def solutionWindow():
    glutInitWindowSize(400,400);
    glutInitWindowPosition(450,100);
    glutCreateWindow("Problem Solution: Clipped polygon");
    glutDisplayFunc(drawClipped);
    init()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    probelmWindow()
    solutionWindow()
    glutMainLoop()


if __name__ == "__main__":
    main()