from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.quiver import Quiver
import numpy as np

from AbstractComplexNumber import AbstractComplexNumber
from ComplexNumber import ComplexNumber

class ComplexVector(AbstractComplexNumber):
    __origin__: ComplexNumber
    __tip__: ComplexNumber
    __qv__: Quiver

    def __init__(self, ax: Axes, origin: ComplexNumber, tip: ComplexNumber):
        # Save the axes for further use
        self.__ax__ = ax
        self.__origin__ = origin
        self.__tip__ = tip
        self.__z__ = self.__getVector__()
    
    ''' Equivalent to tip - origin '''
    def __getVector__(self) -> complex:
        return self.__tip__.getTranslate(self.__origin__.getReverse()).rect()

    ''' Updates the complex number that represents  the 2d vector given the origin and tip'''
    def __updateZ__(self, origin: ComplexNumber, tip: ComplexNumber):
        self.__origin__ = origin
        self.__tip__ = tip
        self.__z__ = self.__getVector__()

    def __updateZ_from_vector__(self, v: 'ComplexVector'):
        self.__updateZ__(v.get_Origin(), v.get_Tip())

    ''' Equivalent to translating the origin and the tip by w'''
    def getTranslate(self, translate: 'ComplexNumber') -> 'ComplexVector':
        o =  self.get_Origin().getTranslate(translate) 
        t =  self.get_Tip().getTranslate(translate)
        return ComplexVector(self.__ax__, o, t)

    ''' Translates the complex number by z '''
    def translate(self, translate: 'ComplexNumber') -> 'ComplexVector':
        v = self.getTranslate(translate)
        self.__updateZ_from_vector__(v)
        return self

    ''' Equivalent to rotate the tip around the origin by angle theta'''
    def getRotation(self, alpha: float) -> 'ComplexVector':
        # Rotate the tip by alpha
        tip = ComplexNumber.from_complex(self.__z__).rotate(alpha).translate(self.get_Origin())
        return ComplexVector(self.__ax__, self.get_Origin(), tip)

    ''' Rotate the complex number by an angle alpha '''
    def rotate(self, alpha: float) -> 'ComplexVector':
        v = self.getRotation(alpha)
        self.__updateZ_from_vector__(v)
        return self        

    ''' Return the negative vector -z equivalent to (-o, -t)'''
    def getReverse(self) -> 'ComplexVector':
        o = self.get_Origin().getReverse()
        t = self.get_Tip().getReverse()
        return ComplexVector(self.__ax__, o, t)

    ''' Return the negative complex number corresponding to z equivalent to returning -z'''
    def reverse(self):
        v = self.getReverse()
        self.__updateZ_from_vector__(v)
        return self

    ''' Returns the vector that results from amplifying the vector by a, 
        equivalent to leave the origin fix and expand the tip by a '''
    def getAmplification(self, a: float) -> 'ComplexVector':
        tip = ComplexNumber.from_complex(self.__z__).amplify(a).translate(self.__origin__)
        return ComplexVector(self.__ax__, self.get_Origin(), tip)

    ''' Amplifies the number the vector by a '''
    def amplify(self, a: float) -> 'ComplexVector':
        v = self.getAmplification(a)
        self.__updateZ_from_vector__(v)
        return self

    ''' Returns the complex number obtained by conjugating z
        Equivalent to conjugate the origin and the tip of the vector
    '''
    def getConjugate(self) -> 'ComplexVector':
        o = self.get_Origin().getConjugate()
        t = self.get_Tip().getConjugate()
        return ComplexVector(self.__ax__, o, t)

    ''' Conjugates the complex number '''
    def conjugate(self) -> 'ComplexVector':
        v = self.getConjugate()
        self.__updateZ_from_vector__(v)
        return self
    
    ''' Returns the inverse of z namely: (1/|z|, -arg(z))'''
    def getInverse(self):
        pass
    
    ''' Invert the complex number '''
    def inverse(self):
        pass

    ''' 
        Equivalent to leaving the origin fix and amplifying the tip of z by |w| and twisting z by arg(w) is equivalent to z*w = |z||w|*e(arg(z)+arg(w))
    '''
    def getAmplyTwist(self, w: 'ComplexNumber') -> 'ComplexVector':
        # Amplify and twist the vector at the origin and translate to get the tip of the vector
        tip = ComplexNumber.from_complex(self.__z__).amplyTwist(w).translate(self.get_Origin())
        return ComplexVector(self.__ax__, self.get_Origin(), tip)

    ''' Amplify z by |w| and twists z by arg(w) is equivalent to z*w = |z||w|*e(arg(z)+arg(w))'''
    def amplyTwist(self, w: 'ComplexNumber') -> 'ComplexVector':
        v = self.getAmplyTwist(w)
        self.__updateZ_from_vector__(v)
        return self

    def get_Quiver(self):
        return self.__qv__
    
    def get_Axes(self):
        return self.__ax__

    def get_Origin(self):
        return self.__origin__
    
    def get_Tip(self):
        return self.__tip__

    ''' Return the normalize vector '''
    def get_normalize_vector(self) -> 'ComplexVector':
        # Calculate the magnitude of the vector
        magnitude = abs(self.__z__)

        # Scale the vector components by the reciprocal of the magnitude
        normalized_origin = self.get_Origin().amplify(1 / magnitude)
        normalized_tip = self.get_Tip().amplify(1 / magnitude)

        # Create a new ComplexVector object with the scaled components
        return ComplexVector(self.__ax__, normalized_origin, normalized_tip)

    '''Normalizes the vector '''
    def normalize_vector(self) -> 'ComplexVector':
        v = self.get_normalize_vector()
        self.__updateZ_from_vector__(v)
        return v

    @staticmethod
    def angle_between(v1: 'ComplexVector', v2: 'ComplexVector') -> float:
        dot_product = ComplexVector.dot_product(v1, v2)
        magnitude_v1 = abs(v1.__z__)
        magnitude_v2 = abs(v2.__z__)
        return np.arccos(dot_product / (magnitude_v1 * magnitude_v2))

    @staticmethod
    def dot_product(v1: 'ComplexVector', v2: 'ComplexVector') -> float:
        # Calculate the dot product of the vectors
        dot_real = v1.__z__.real * v2.__z__.real + v1.__z__.imag * v2.__z__.imag
        return dot_real
    
    def show(self, **kArgs):
        o = self.get_Origin()
        self.__qv__ = self.get_Axes().quiver(o.real(), o.img(), self.__z__.real, self.__z__.imag, angles='xy', scale_units='xy', scale=1, **kArgs)
        return self