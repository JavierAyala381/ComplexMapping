from abc import ABC, abstractmethod
import cmath
from typing import Any, Callable, Union

from matplotlib.axes import Axes


class AbstractComplexNumber(ABC):
    # Holds the complex number
    __z__: complex
    __ax__: Axes | None
    __callback__: Callable[['AbstractComplexNumber'], Any] | None

    def __init__(self, z: complex) -> None:
        # Set the empty callback 
        self.__callback__ = None
        # Set to an empty line
        self.__line__ = None
        # Set the axes to none
        self.__ax__ = None
        # Set the complex number
        self.setZ(z)

    @staticmethod
    def mod(z: complex) -> float:
        return abs(z)
    
    @staticmethod
    def arg(z: complex) -> float:
        return cmath.phase(z)

    @staticmethod
    def sub(z: complex, w: complex) -> complex:
        return AbstractComplexNumber.add(z, -w)

    @staticmethod
    def add(z: complex, w: complex) -> complex:
        return z + w
    
    @staticmethod
    def rot(z: complex, alpha: float) -> complex:
        p = cmath.polar(z)
        return cmath.rect(p[0], p[1] + alpha)
    
    @staticmethod 
    def amp(z: complex, a: float) -> complex:
        p = cmath.polar(z)
        return cmath.rect(a*p[0], p[1]) 

    @staticmethod
    def conj(z: complex) -> complex:
        return complex(z.real, -1*z.imag)

    @staticmethod
    def inv(z: complex) -> complex:
        return cmath.rect(1/AbstractComplexNumber.mod(z), -AbstractComplexNumber.arg(z))
    
    @staticmethod
    def multiply(z: complex, w: complex) -> complex:
        return cmath.rect(AbstractComplexNumber.mod(z)*AbstractComplexNumber.mod(w), AbstractComplexNumber.arg(z)+AbstractComplexNumber.arg(w))

    @staticmethod
    def pow(z: complex, n: float) -> complex:
        ''' raise z to the n-th power '''
        r,p = cmath.polar(z)
        return cmath.rect(r**n, p*n)

    def module(self) -> float:
        ''' Returns the module of the complex number '''
        return AbstractComplexNumber.mod(self.__z__)

    def setModule(self, a: float):
        ''' Leaves the argument of z unchanged and sets the module of z to a '''
        self.setZ(cmath.rect(a, self.argument()))
        return self

    def argument(self) -> float:
        ''' Returns the argument of the complex number '''
        return AbstractComplexNumber.arg(self.__z__)
    
    def setArgument(self, theta: float):
        ''' Leaves the module of z unchanged and and sets the argument of z to theta '''
        self.setZ(cmath.rect(self.module(), theta))
        return self

    def real(self) -> float:
        ''' Returns the real part of the complex number '''
        return self.__z__.real
    
    def setReal(self, real: float) -> 'AbstractComplexNumber':
        ''' Updates the real prt of the complex number'''
        self.setZ(complex(real, self.__z__.imag))
        return self

    def img(self) -> float:
        ''' Returns the img part of the complex number '''
        return self.__z__.imag
    
    def setImg(self, imag: float) -> 'AbstractComplexNumber':
        ''' Updates the imaginary part of the complex number '''
        self.setZ(complex(self.__z__.real, imag))
        return self

    def rect(self) -> complex:
        ''' Returns the rectangular form of the complex number '''
        return self.real() + self.img()*1j
    
    def polar(self) -> tuple[float, float]:
        ''' Returns the polar form of the complex number '''
        return cmath.polar(self.__z__)
    
    def setZ(self, z: Union[complex, 'AbstractComplexNumber']):
        ''' Updates the value of z '''
        if isinstance(z, complex):
            self.__z__ = z
        elif isinstance(z, AbstractComplexNumber):  # Assuming AbstractComplexNumber is a class
            self.__z__ = z.rect()

        if(self.__callback__):
            self.__callback__(self)
    
    def onChange(self, func: Callable[['AbstractComplexNumber'], Any]):
        ''' Retrieves and observer function that gets call every time z changes '''
        self.__callback__ = func

    @abstractmethod
    def power(self, n: float) -> 'AbstractComplexNumber':
        ''' Raises z to the power n '''
        pass

    @abstractmethod
    def getPower(self, n, float) -> 'AbstractComplexNumber':
        ''' 
            Returns the complex number obtained by raising it to the power n is equivalent to:
            z = re^(p i)
            z^n = (r^n)e^(n*p i)
        '''
        pass

    @abstractmethod
    def getTranslate(self, translate: 'AbstractComplexNumber') -> 'AbstractComplexNumber':
        ''' Returns the complex number obtain by translating the z by w'''
        pass

    @abstractmethod
    def translate(self, translate: 'AbstractComplexNumber') -> 'AbstractComplexNumber':
        ''' Translates the complex number z by w '''
        pass

    @abstractmethod
    def getRotation(self, alpha: float) -> 'AbstractComplexNumber':
        ''' Returns the complex number obtainer by rotating z by alpha'''
        pass

    @abstractmethod
    def rotate(self, alpha: float) -> 'AbstractComplexNumber':
        ''' Rotate the complex number by an angle alpha equivalent to multiply the number by another complex number w with unit module'''
        pass

    @abstractmethod
    def getReverse(self) -> 'AbstractComplexNumber':
        ''' Return the negative of z equivalent to returning -z'''
        pass

    @abstractmethod
    def reverse(self) -> 'AbstractComplexNumber':
        ''' Negates to z equivalent to doing -z'''
        pass

    @abstractmethod
    def getAmplification(self, a: float) -> 'AbstractComplexNumber':
        ''' Returns the number obtained by amplifying z by a equivalent to a*|z|e^(arg(z)i)'''
        pass

    @abstractmethod
    def amplify(self, a: float) -> 'AbstractComplexNumber':
        ''' Amplifies the z by a equivalent to a*|z|e^(arg(z)i) '''
        pass

    @abstractmethod
    def getConjugate(self) -> 'AbstractComplexNumber':
        ''' Returns the conjugating of z '''
        pass

    @abstractmethod
    def conjugate(self) -> 'AbstractComplexNumber':
        ''' Conjugates the complex number z '''
        pass
    
    @abstractmethod
    def getInverse(self) -> 'AbstractComplexNumber':
        ''' Returns the inverse of z namely: (1/|z|, -arg(z)) '''
        pass
    
    @abstractmethod
    def inverse(self) -> 'AbstractComplexNumber':
        ''' Invert the z equivalent to 1/|z|*e^(-arg(z)i)'''
        pass

    @abstractmethod
    def getAmplyTwist(self, w: 'AbstractComplexNumber') -> 'AbstractComplexNumber':
        ''' Returns the complex number obtained by amply twisting z by w, equivalent to z*w = |z||w|*e((arg(z)+arg(w))i)'''
        pass

    @abstractmethod
    def amplyTwist(self, w: 'AbstractComplexNumber') -> 'AbstractComplexNumber':
        ''' AmplyTwist z by w, equivalent to z*w = |z||w|*e((arg(z)+arg(w))i)'''
        pass

    @abstractmethod
    def show(self, **kArgs):
        ''' shoes the complex number in the given axes'''
        pass