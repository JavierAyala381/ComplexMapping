from typing import Any, Callable, Literal
from matplotlib import animation, pyplot as plt
from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import Arc, Circle
from matplotlib.quiver import Quiver
from matplotlib.widgets import Slider
import numpy as np

from AbstractComplexNumber import AbstractComplexNumber
from ComplexNumber import ComplexNumber
from ComplexVector import ComplexVector
from AbstractComplexPlane import AbstractComplexPlane

class ComplexPlane(AbstractComplexPlane):

    ## Complex mapping constructor
    def __init__(self, mapTitle: str, xDomain: np.ndarray, yDomain: np.ndarray):
        # Instantiate the figure and the axis
        fig, ax = plt.subplots()

        # Call the abstract class constructor
        super().__init__(fig, ax, mapTitle, np.array([xDomain, yDomain]))

        # Set plot metadata
        self.__ax__.set(
            facecolor="black",
            
            xlim=(xDomain[0],xDomain[-1]),
            ylim=(yDomain[0],yDomain[-1]),
        )

        # adding vertical line in data co-ordinates 
        plt.axvline(0, c='white') 
        
        # adding horizontal line in data co-ordinates 
        plt.axhline(0, c='white') 

        # Show the plot grid
        plt.grid(color='#127ca3')
        self.__ax__.legend()
    
    ''' draws vertical lines separated by the interval'''
    def drawVLines(self, interval: int) -> LineCollection:
        x: np.ndarray = self.getxDom()
        y: np.ndarray = self.getyDom()
        xDomain = np.linspace(x[0], x[-1], interval)
        return plt.vlines(
            x = xDomain, 
            ymin = y[0], 
            ymax = y[-1],
           colors = 'purple',
           label = 'vline_multiple - full height')
    
    """
        Draws horizontal lines
    """
    def drawHLines(self, interval: int) -> LineCollection:
        x: np.ndarray = self.getxDom()
        y: np.ndarray = self.getyDom()
        yDomain = np.linspace(y[0], y[-1], interval)
        return plt.hlines(
            y = yDomain,
            xmin = x[0],
            xmax = x[-1],
            color = 'blue',
            label = 'hline_multiple - full lenght' 
        )

    """ Draws the unit circle in the plane """
    def drawUnitCircle(self, **kArgs):
        self.drawCircle(ComplexNumber(0,0), 1, **kArgs)

    """ Draws a circle of radius r in the given origin """
    def drawCircle(self, center: ComplexNumber, radius: float, **kwargs): 
        circle1 = Circle(xy=(center.real(), center.img()), radius=radius, **kwargs)
        self.__ax__.add_patch(circle1)

    def updatePoint(self, z:ComplexNumber, line: Line2D, tracePrint) -> Line2D:
        ''' 
            Updates the point z in the complex plane by:
            a) Stack the current position of z to the its past position form the line trajectory, if tracePrint is set to true
            b) Sets the data to a single point, if TracePrint is set to false
        '''
        if tracePrint:
            current_position = (z.real(), z.img())

            # Update the trajectory with the current position
            x_data, y_data = line.get_data()
            x_data = np.append(x_data, current_position[0])
            y_data = np.append(y_data, current_position[1])
            line.set_data(x_data, y_data)
        else:
            line.set_data(z.real(), z.img())
        return line
    
    def __update_abstract_complex_number__(self, num: int, v: AbstractComplexNumber, func: Callable[[int, AbstractComplexNumber], AbstractComplexNumber], tracePrint) -> (tuple[Quiver] | tuple[Line2D]):
        ''' Define the update function to update the quiver plot for each frame 
            Updates the quiver 
        '''
        w = func(num, v)
        if isinstance(w, ComplexVector):
            qv = w.get_Quiver()
            ax = w.get_Axes()
            if tracePrint and ax:
               tip = w.get_Tip()
               tip.setAxes(ax)
               tip.show(color='b', marker='o', markersize=1)
               line = tip.get_Line()
               self.updatePoint(tip, line, tracePrint)
            qv.set_offsets((w.get_Origin().real(), w.get_Origin().img()))
            qv.set_UVC(w.real(), w.img())
            return qv,
        elif isinstance(w, ComplexNumber):
            line = v.get_Line()
            return self.updatePoint(w, line, tracePrint),
        else:
            # Handle the case where neither ComplexVector nor ComplexNumber is returned
            raise ValueError("Unexpected type returned by the function")

    def animate(self, v: AbstractComplexNumber, func: Callable[[int, AbstractComplexNumber], AbstractComplexNumber], frames: int, tracePrint=False, **animArgs):
        ''' Animates a vector by applying a transformation to it
            :params ComplexVector v the complex Vector to animate 
            :params func the mathematical function that describes the operation to perform upon v
            ... other animation arguments
        '''
        anim = animation.FuncAnimation(
            self.getFigure(), 
            self.__update_abstract_complex_number__, 
            frames=frames, 
            fargs=(v, func, tracePrint), 
            interval=50, **animArgs)
        return anim
    
    def transform(self, v: np.ndarray, T: Callable[[ComplexNumber], ComplexNumber]) -> np.ndarray:
        '''
            Transforms the given np array and transforms it by T
            :param T represents the transformation to apply to all members of v
        '''
        return ComplexNumber.map(v, lambda i,z: T(z))
    
    def tracePointPath(self, points: np.ndarray):
        # Paint the first element in the linespace of complex numbers and return the line
        line = points[0].setAxes(self.getAxes()).show(color='g', marker='o', markersize=4).get_Line()

        def updateFromLine(num: int, z_linespace, line: Line2D, trace):
            '''
                param: num is the frame number
                param: z is the linespace with all the numbers to plot
            '''
            return self.updatePoint(z_linespace[num], line, trace),
    
        anim = animation.FuncAnimation(
            self.getFigure(),
            updateFromLine,
            fargs=(points, line, False),
            frames=len(points), 
            interval=500
        )

        return anim

    def tracePath(self, func, range: np.ndarray, tracePrint=False):
        ''' 
            Animates an abstract complex number so that if follows the path defined by func
            :param func should return the y value of the path to follow
            :param range the domain of func represents the x values
        '''

        # Apply the function to each value in the range linspace
        image: np.ndarray = func(range)

        # Retrieve the coordinates of the points to plot
        coordinates = np.column_stack((range, image))

        # Create the linespace of complex numbers
        z_linespace: np.ndarray = ComplexNumber.from_np_ndarray(coordinates)

        # Paint the first element in the linespace of complex numbers and return the line
        line = z_linespace[0].setAxes(self.getAxes()).show(color='g', marker='o', markersize=4).get_Line()

        # Updates the line
        def updateFromLine(num: int, z_linespace, line: Line2D, trace):
            '''
                param: num is the frame number
                param: z is the linespace with all the numbers to plot
            '''
            return self.updatePoint(z_linespace[num], line, trace),

        # Create the animation
        anim = animation.FuncAnimation(
            self.getFigure(),
            updateFromLine,
            fargs=(z_linespace, line, tracePrint),
            frames=len(range), 
            interval=500
            )
        
        return anim, z_linespace