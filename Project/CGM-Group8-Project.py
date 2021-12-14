import math
from OpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

PI = 3.14159265 # constant
ballRadius = 0.2 # ball's radius
ballX, ballY = 0.0, 0.0 # ball's ccenter position (x,y)
ballXMax, ballXMin, ballYMax, ballYMin = 0,0,0,0 # ball's center bounds
xSpeed, ySpeed = 0.02, 0.005 # ball's speed along x-axis and y-axis
refreshMillis = 30 # refresh period in milliseconds

clipAreaXLeft, clipAreaXRight, clipAreaYBottom, clipAreaYTop = 0, 0, 0, 0 # for projection

# the display function
def display():
    global ballX, ballY, xSpeed, ySpeed, ballXMax, ballXMin, ballYMax, ballYMin # global variables are used
    glClear(GL_COLOR_BUFFER_BIT) # clear the color buffer
    glMatrixMode(GL_MODELVIEW) # model transformation and view transformation mode.
    glLoadIdentity() # loads identity matrix to the model-view matrix
    glTranslatef(ballX, ballY, 0.0)
    glBegin(GL_TRIANGLE_FAN) # using triangle fan to draw the circle
    # glColor3f(1.0, 1.0, 1.0)
    glColor3f(0.785,0.785,0.785) # somewhat white color
    glVertex2f(0.0, 0.0) # center

    numSegments = 50
    # triangle fan for 360 degrees to make a circle
    for i in range(numSegments+1):
        # used to create football like texture
        if i%10 == 1:
            glColor3f(0.0,0.0,0.0)
        else:
            glColor3f(1.0, 1.0, 1.0)
        angle = i*2.0*PI / numSegments
        glVertex2f(math.cos(angle)*ballRadius, math.sin(angle)*ballRadius)

    glEnd()
    glutSwapBuffers()

    #Animation control compute location at next refresh

    ballX += xSpeed
    ballY += ySpeed

    # check if ball exceeds the edges
    if ballX > ballXMax:
        ballX = ballXMax
        xSpeed = -xSpeed
    elif ballX < ballXMin:
        ballX = ballXMin
        xSpeed = -xSpeed
    
    if ballY > ballYMax:
        ballY = ballYMax
        ySpeed = -ySpeed
    elif ballY < ballYMin:
        ballY = ballYMin
        ySpeed = -ySpeed

# call back when window size is resized
def reshape(width, height):
    global clipAreaXLeft, clipAreaXRight, clipAreaYBottom, clipAreaYTop, ballX, ballY, xSpeed, ySpeed, ballXMax, ballXMin, ballYMax, ballYMin, ballRadius
    if height == 0:
        height = 1
    aspect = float(width/height) # compute aspect ratio of new window

    glViewport(0,0, width, height) #set viewport to cover the new window
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    #set aspect ratio of the clipping area to match with that of viewport
    if width>=height:
        clipAreaXLeft = -1.0 * aspect
        clipAreaXRight = 1.0 * aspect
        clipAreaYBottom = -1.0
        clipAreaYTop = 1.0
    else:
        clipAreaXLeft = -1.0 
        clipAreaXRight = 1.0 
        clipAreaYBottom = -1.0 / aspect
        clipAreaYTop = 1.0 / aspect
    gluOrtho2D(clipAreaXLeft, clipAreaXRight, clipAreaYBottom, clipAreaYTop)
    ballXMin, ballXMax = clipAreaXLeft + ballRadius, clipAreaXRight - ballRadius
    ballYMin, ballYMax = clipAreaYBottom + ballRadius, clipAreaYTop - ballRadius

# callback when timer expired
def Timer(value):
    global refreshMillis
    glutPostRedisplay() # calls display function again, same as if glutDisplayFunc(display)
    glutTimerFunc(refreshMillis, Timer, 0) # subsequent timer call at milliseconds

# window's properties
windowWidth, windowHeight = 640, 480
windowPosX, WindowPosY = 50, 50

if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE)
    glutInitWindowSize(windowWidth, windowHeight)
    glutInitWindowPosition(windowPosX, WindowPosY)
    glutCreateWindow("Bouncing FootBall")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutTimerFunc(0, Timer, 0)
    glClearColor(0.0, 0.0, 0.0, 1.0) # set background color to black
    glutMainLoop()