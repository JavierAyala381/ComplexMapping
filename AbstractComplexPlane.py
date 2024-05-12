from abc import ABC, abstractmethod
from typing import Any, Callable, Literal, Union

from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.widgets import Slider
import numpy as np

from ComplexNumber import ComplexNumber


class AbstractComplexPlane(ABC):
    # Holds the figure information
    __fig__: Figure
    __ax__: Axes

    # Stores the elements of the complex plane in a dictionary
    __elements__ = {}

    # Store the interactive elements
    __interactive_elements_ = {}

    # Store the domains of the plot
    __x__: np.ndarray
    __y__: np.ndarray
    __z__: np.ndarray

    def __init__(self, fig: Figure, ax: Axes, mapTitle: str, domains: np.ndarray) -> None:
        self.__fig__ = fig
        self.__ax__ = ax

        self.__x__ = domains[0]
        self.__y__ = domains[1]
        if domains[2].any():
            self.__z__ = domains[2]

    def drawPoint(self, s: ComplexNumber, z: float | None = None, **kArgs):
        ''' Draws an n dimensional point '''
        real: float = s.real()
        imag: float = s.img()
        if(z):
            return self.__ax__.plot([real], [imag], [z], **kArgs)
        else:
            ''' Draws a point in the figure '''
            return self.__ax__.plot(real, imag, **kArgs)

    def drawLine(self, a: Union[ComplexNumber, tuple[ComplexNumber, float]], b: Union[ComplexNumber, tuple[ComplexNumber, float]], **kArgs):
        ''' Draws the line between two points '''
        if (isinstance(a, ComplexNumber) and isinstance(b, ComplexNumber)):
            self.getAxes().plot(
                [a.real(), b.real()], 
                [a.img(), b.img()], **kArgs)
        else:
            assert isinstance(a, tuple) and isinstance(b, tuple)
            self.getAxes().plot(
                [a[0].real(), b[0].real()], 
                [a[0].img(), b[0].img()], 
                [a[1], b[1]], **kArgs)

    def getxDom(self) -> np.ndarray:
        ''' Returns the x domain of the figure'''
        return self.__x__
    
    def getyDom(self) -> np.ndarray:
        ''' Returns the y domain of the figure'''
        return self.__y__
    
    def getzDom(self) -> np.ndarray:
        ''' Returns the z domain of the figure'''
        return self.__z__

    def getFigure(self) -> Figure:
        ''' Returns the figure corresponding to the plane'''
        return self.__fig__
    
    def getAxes(self) -> Axes:
        ''' Returns the Axes of the Figure'''
        return self.__ax__
    
    def refresh(self):
        ''' Refreshes and re draws the canvas '''
        self.getFigure().canvas.draw()

    def addSlider(self, name: str, min: float, max: float, init: float, update: Callable[[float],Any], orientation: Literal['horizontal', 'vertical']='horizontal') -> Slider:
        '''
            Adds a interactive slider to the plot
            param: name the name of the slider must be unique
            param: min the minimum range of the slider
            param: max the maximum range of the slider
            param: init the initial value of the slider
            param: update a function that receives the values from the slider
            param: orientation the orientation of the slider vertical or horizontal
        '''
        
        # Retrieve the figure of the plane
        fig = self.getFigure()

        # adjust the main plot to make room for the sliders
        fig.subplots_adjust(left=0.25, bottom=0.25)

        # Initialize a counter
        existing_sliders = 0
        increment = 0.04  # Adjust this value as needed

        # Iterate through the dictionary items
        for element in self.__interactive_elements_.values():
            # Check if the type is "Slider"
            if element["type"] == "Slider" and element["value"].orientation == orientation:
                # Increment the counter
                existing_sliders += 1

        if(orientation == 'horizontal'):
            # Define initial values for position and size
            left = 0.25
            bottom = 0.1
            width = 0.65
            height = 0.03

            # Calculate the increment based on the number of existing sliders
            # Adjust position and size dynamically
            bottom += existing_sliders * increment
        else:
            # Define initial values for position and size
            left = 0.1
            bottom = 0.25
            width = 0.0225
            height = 0.63

            # Adjust position and size dynamically
            left += existing_sliders * increment

        # Make a slider
        axes = fig.add_axes((left, bottom, width, height))
        slider = Slider(
            ax=axes,
            label=name,
            valmin=min,
            valmax=max,
            valinit=init,
            orientation=orientation
        )

        # register the update function with each slider
        id = slider.on_changed(update)
        print(id, id.__getstate__())

        # store the slider
        self.__interactive_elements_[name] = {
            "type": "Slider",
            "value": slider,
            "axes": axes
        }

        return slider