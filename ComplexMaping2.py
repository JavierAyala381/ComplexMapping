import cmath
import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.patches import Arc
import matplotlib.pyplot as plt
from matplotlib.quiver import Quiver
import numpy as np
import matplotlib.animation as animation

import numpy as np

from AbstractComplexNumber import AbstractComplexNumber
from ComplexNumber import ComplexNumber as cn
from ComplexPlane import ComplexPlane
from ComplexVector import ComplexVector
from ExtendedComplexPlane import ExtendedComplexPlane

#Define the complex number in z
theta = np.linspace(0, 2*np.pi, 10) # Generate values of theta from 0 to 2pi
z = np.cos(theta) + 1j * np.sin(theta)

# Define the complex transformation of z
w = z**2

# Define the domain of the plane
x = np.linspace(-1.5, 1.5)
y = np.linspace(-1.5, 1.5)
z = np.linspace(-1.5, 1.5)

# Define the Z complex Plane
zPlane = ComplexPlane("Z space", x, y)
#wPlane = ComplexPlane("W-Plane", x, y)
#ext = ExtendedComplexPlane("Ex-Plane", x, y, z)
#ext.drawPoint(cn(1,1), z=2, color='g', marker='o', markersize=5)
#ext.drawSphere(cn(0,0),1,1)
#ext.drawLine((cn(0,1),1), (cn(1,1),-1))
ext.drawPseudoSphere()

#z = cn(1, cmath.pi/2, polar=True)
#zPlane.drawZ(z, marker='o', markersize=10, label='z', markerfacecolor="green")
#zPlane.drawZ(z.getInverse().amplyTwist(cn.from_complex(complex(2,1))), marker='o', markersize=10, label='w', markerfacecolor="red")

o = cn(0.0,0.0)
t = cn(0,1)

# Draws a vector in complex plane
#cv = ComplexVector(zPlane.getAxes(), o, t).show(color='r')
# Draw a complex vector
#w = cn(1,1, axes=zPlane.getAxes()).show(color='g', marker='o', markersize=5)
#zPlane.transform(w, lambda x: x.getRotation(cmath.pi/2))

#cv.getRotation(cmath.pi/2).amplify(2).translate(o.getReverse()).show(color='g')
#cv.getConjugate().show(color='b')

#anim = zPlane.animate(cv, rot, 100, tracePrint=True)
#l = zPlane.drawHLines(1)

a_dom = np.linspace(0, 2*cmath.pi, 100)
x_dom = np.linspace(0.1, 1, 100)

# x^3 +2x +1
def x3(range):
    return np.power(range, 3) +5*np.power(range,2)+2*range + 1

def l(range):
    return range

# Returns the points in the traced path given by the domain and the function
#anim, points = zPlane.tracePath(x3, x_dom)
#line_anim, line_points = zPlane.tracePath(l,x_dom)

def rot(range):
    dom = np.full(100, cn(0,1), dtype=cn)
    return cn.map(dom, lambda i, z: z.getRotation(range[i]))


#imageW = cn(0,0,axes=wPlane.getAxes()).show(color='g', marker='o', markersize=5)
def updatePoint(delta: float, w: cn):
    w.setReal(delta)
    zPlane.updatePoint(w,w.get_Line(),True)
    zPlane.refresh()

def updateImg(delta: float, w: cn):
    w.setImg(delta)
    zPlane.updatePoint(w,w.get_Line(),True)
    zPlane.refresh()

def updateModule(mod: float, z: cn):
    z.setModule(mod)
    zPlane.updatePoint()

#realSlider = zPlane.addSlider("real",-1,1,w.real(), lambda d: updatePoint(d, w))
#imagSlider = zPlane.addSlider("imag",-1,1,w.img(), lambda d: updateImg(d, w))

def ImageUnderChange(z:cn,w:cn):
    g = z.getPower(2)
    w.setZ(g)
    wPlane.updatePoint(w, w.get_Line(), True)
    wPlane.refresh()
# Listen to the change of z
#w.onChange(lambda z: ImageUnderChange(z, imageW))

#image = rot(a_dom)
#an2 = zPlane.tracePointPath(image)
#an = w.tracePointPath(w.transform(image, lambda z: z.getPower(2)))
#line_transform = wPlane.tracePointPath(wPlane.transform(line_points, lambda z: z.getInverse().conjugate()))



# Transform the point from the traced paths
#zPlane.transform(points, lambda z: z.power(2))

#zPlane.drawUnitCircle(linestyle='--', fill=False, edgecolor='white', linewidth=2)


#wPlane.drawUnitCircle(linestyle='--', fill=False, edgecolor='white', linewidth=2)

#figC, axesC = ComplexPlane.mergeComplexPlanes(zPlane, wPlane)

# Plot some elements
#vector = zPlane.drawVector((0,0), (1,0))
#wVector = zPlane.drawVector((0,0), (1,0))

"""
zPoint, = zPlane.drawPoint(z.real[0], z.imag[0], marker='o', markersize=4, label='z', markerfacecolor="green")
wPoint, = wPlane.drawPoint(w.real[0], w.imag[0], marker='o', markersize=4, label='w=f(z)', markerfacecolor="green")
"""

#anim = zPlane.animateVector(vector=cv, func=animateQuiver, fargs=(cv, angle), frames=20)

#ani = animation.FuncAnimation(fig=figZ, func=update, frames=100, fargs=(zPoint, z), interval=100)
#ani_w = animation.FuncAnimation(fig=figW, func=update, frames=100, fargs=(wPoint, w), interval=100)

plt.show()