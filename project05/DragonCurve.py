# This program will create a fractal dragon curve using turtle graphics.
# The results are saved as an eps.
# A dragon curve is created by recursive 90 degree angles.
from turtle import *

def draw_fractal(length, angle, level, initial_position, target, replacement, new_target, new_replacement):

    position = initial_position
   
   # Determining where the next line is drawn
    for counter in range(level):
        new_position = ''
        for character in position:
            if character == target:
                new_position += replacement
            elif character == new_target:
                new_position += new_replacement
            else:
                new_position += character
        position = new_position
       
    # Drawing the dragon curve
    for character in position:
        if character == 'F':
            forward(length)
        elif character == '+':
            right(angle)
        elif character == '-':
            left(angle)

       
if __name__ == '__main__':
    
    draw_fractal(7, 90, 10, 'FX', 'X', 'X+YF+', 'Y', '-FX-Y')
    myTurtle = turtle.Turtle()
    x = myTurtle.getscreen()
    x.getcanvas().postscript(file = "DragonCurveOutput.eps")
    
    # x.getcanvas().postscript(file = "DragonCurveOutput.svg")
    # x.getcanvas().postscript(file = "DragonCurveOutput.jpeg")
    # x.getcanvas().postscript(file = "DragonCurveOutput.png")
   
    exitonclick() # click to exit
