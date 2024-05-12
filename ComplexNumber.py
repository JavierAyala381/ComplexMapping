import cmath
from typing import Callable

from matplotlib.axes import Axes
import numpy as np

from AbstractComplexNumber import AbstractComplexNumber

class ComplexNumber(AbstractComplexNumber):
    def __init__(self, x: float, y: float, axes = None, polar=False):
        '''
        Creates a complex number.

        Parameters:
            x (float): Real part if polar is False, otherwise the magnitude of the complex number.
            y (float): Imaginary part if polar is False, otherwise the argument (angle in radians) of the complex number.
            polar (bool, optional): Specifies whether the coordinates are in polar form. Defaults to False.
        '''
        z: complex | None
        if(polar):
            z = cmath.rect(x, y)    
        else:  
            z = complex(x,y)

        ''' Assign an axes if present'''
        if(axes):  
            self.__ax__ = axes
            
        # Call the constructor super class
        super().__init__(z)

    def setAxes(self, ax: Axes):
        ''' Sets the axes if provided '''
        self.__ax__ = ax
        return self

    ''' Creates a complex number class from a complex number type'''
    @staticmethod
    def from_complex(z: complex) -> 'ComplexNumber':
        return ComplexNumber(z.real, z.imag)
    
    @staticmethod
    def from_np_ndarray(coordinates: np.ndarray) -> np.ndarray:
        ''' Returns a numpy array of complex number given a numpy array of coordinates in the form
            c(x,y)
        '''
        return np.fromiter((ComplexNumber(c[0],c[1]) for c in coordinates), dtype=ComplexNumber)
    
    def getPower(self, n: float) -> 'ComplexNumber':
        ''' Returns the complex number obtainer by raising z to n'''
        return ComplexNumber.from_complex(ComplexNumber.pow(self.__z__, n))

    def power(self, n: float) -> 'ComplexNumber':
        self.setZ(self.getPower(n).rect())
        return self

    def getTranslate(self, translate: 'ComplexNumber') -> 'ComplexNumber':
        ''' Returns the complex number obtain by translating the z by w'''
        z = ComplexNumber.add(self.__z__, translate.rect())
        return self.from_complex(z)

    ''' Translates the complex number by z '''
    def translate(self, translate: 'ComplexNumber') -> 'ComplexNumber':
        self.setZ(self.getTranslate(translate).rect())
        return self

    ''' Returns the complex number obtainer by translating the z by alpha'''
    def getRotation(self, alpha: float) -> 'ComplexNumber':
        z = ComplexNumber.rot(self.__z__, alpha)
        return ComplexNumber.from_complex(z)

    ''' Rotate the complex number by an angle alpha '''
    def rotate(self, alpha: float) -> 'ComplexNumber':
        self.setZ(self.getRotation(alpha).rect())
        return self
    
    ''' Return the complex number result of reverse of z = -z'''
    def getReverse(self) -> 'ComplexNumber':
        return ComplexNumber.from_complex(complex(-1*self.real(), -1*self.img()))

    ''' Reverse the number equivalent to -z'''
    def reverse(self) -> 'ComplexNumber':
        self.setZ(self.getReverse().rect())
        return self

    ''' Returns the number obtained by amplifying z by a'''
    def getAmplification(self, a: float) -> 'ComplexNumber':
        z = ComplexNumber.amp(self.__z__, a)
        return ComplexNumber.from_complex(z)

    ''' Amplifies the number by a '''
    def amplify(self, a: float) -> 'ComplexNumber':
        self.setZ(self.getAmplification(a).rect())
        return self

    ''' Returns the complex number obtained by conjugating z'''
    def getConjugate(self) -> 'ComplexNumber':
        z =  ComplexNumber.conj(self.__z__)
        return ComplexNumber.from_complex(z)

    ''' Conjugates the complex number '''
    def conjugate(self) -> 'ComplexNumber':
        self.setZ(self.getConjugate().rect())
        return self
    
    ''' Returns the inverse of z namely: (1/|z|, -arg(z))'''
    def getInverse(self) -> 'ComplexNumber':
        z = ComplexNumber.inv(self.__z__)
        return ComplexNumber.from_complex(z)
    
    ''' Invert the complex number '''
    def inverse(self) -> 'ComplexNumber':
        self.setZ(ComplexNumber.inv(self.__z__))
        return self

    def getAmplyTwist(self, w: 'ComplexNumber') -> 'ComplexNumber':
        ''' Returns the complex number obtained by amplifying z by |w| and twisting z by arg(w) is equivalent to z*w = |z||w|*e(arg(z)+arg(w))'''
        z = ComplexNumber.multiply(self.rect(), w.rect())
        return ComplexNumber.from_complex(z)
    
    def amplyTwist(self, w: 'ComplexNumber') -> 'ComplexNumber':
        ''' Amplify z by |w| and twists z by arg(w) is equivalent to z*w = |z||w|*e(arg(z)+arg(w))'''
        self.setZ(self.getAmplyTwist(w).rect())
        return self
    
    def show(self, **kArgs):
        if(self.__ax__):
            self.__line__, = self.__ax__.plot(self.__z__.real, self.__z__.imag, **kArgs)
        else:
            raise Exception("No complex plane attach")
        return self

    def get_Line(self):
        return self.__line__
    
    @staticmethod
    def map(complexArray: np.ndarray, function: Callable[[int, 'ComplexNumber'], 'ComplexNumber']):
        return np.fromiter((function(i,z) for i, z in enumerate(complexArray)), dtype=ComplexNumber)