from matplotlib import pyplot as plt
from matplotlib.axes import Axes
import numpy as np
from AbstractComplexPlane import AbstractComplexPlane
from ComplexNumber import ComplexNumber


class ExtendedComplexPlane(AbstractComplexPlane):

    def __init__(self, name: str, xDomain: np.ndarray, yDomain: np.ndarray, zDomain: np.ndarray) -> None:
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        super().__init__(fig,ax,name,np.array([xDomain, yDomain, zDomain]))
        self.__draw_axes__()

        ax.set_aspect('equal')

        ax.set_box_aspect([1,1,1]) # type: ignore # IMPORTANT - this is the new, key line
        ax.set_proj_type('ortho') # type: ignore # OPTIONAL - default is perspective (shown in image above)
        self.__set_axes_equal__(ax) # IMPORTANT - this is also required

        ax.set_xlim(xDomain[0],xDomain[-1])
        ax.set_ylim(yDomain[0],yDomain[-1])
        ax.set_zlim(zDomain[0],zDomain[-1]) # type: ignore

        # Show the plot grid
        plt.grid(color='#127ca3')

        self.__ax__.legend()

    def __draw_axes__(self):
        ''' Draws the x,y and z axes of the plane '''
        xDom = self.getxDom()
        yDom = self.getyDom()
        zDom = self.getzDom() # type: ignore
        ax = self.getAxes()
        # Define points for the lines along the x, y, and z axes
        x_line = [xDom[0],xDom[-1]]  # Along x-axis, from (-1, 0, 0) to (1, 0, 0)
        y_line = [yDom[0],yDom[-1]]  # Along y-axis, from (0, -1, 0) to (0, 1, 0)
        z_line = [zDom[0],zDom[-1]]  # Along z-axis, from (0, 0, -1) to (0, 0, 1)
        ax.plot([0, 0], [0, 0], z_line, color='blue')
        # Plot the lines passing through the origin
        ax.plot(x_line, [0, 0], [0, 0], color='red')
        ax.plot([0, 0], y_line, [0, 0], color='green')

    def __set_axes_equal__(self, ax: Axes):
        """Set 3D plot axes to equal scale.

        Make axes of 3D plot have equal scale so that spheres appear as
        spheres and cubes as cubes.  Required since `ax.axis('equal')`
        and `ax.set_aspect('equal')` don't work on 3D.
        """
        limits = np.array([
            ax.get_xlim3d(), # type: ignore
            ax.get_ylim3d(), # type: ignore
            ax.get_zlim3d(), # type: ignore
        ])
        origin = np.mean(limits, axis=1)
        radius = 0.5 * np.max(np.abs(limits[:, 1] - limits[:, 0]))
        self.__set_axes_radius__(ax, origin, radius)

    def __set_axes_radius__(self, ax, origin, radius):
        x, y, z = origin
        ax.set_xlim3d([x - radius, x + radius])
        ax.set_ylim3d([y - radius, y + radius])
        ax.set_zlim3d([z - radius, z + radius])

    def drawSphere(self, s: ComplexNumber, z:float, r: float, **kArgs):
        u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        x = np.cos(u)*np.sin(v)
        y = np.sin(u)*np.sin(v)
        zAx = np.cos(v)
        self.getAxes().plot_surface(x, y, zAx, **kArgs) # type: ignore

    def drawPseudoSphere(self, **kArgs):
        u = np.linspace(-10, 10, 100)  # Adjust range for u
        v = np.linspace(0, 2 * np.pi, 100)
        u, v = np.meshgrid(u, v)

        x = 1 / np.cosh(u) * np.cos(v)
        y = 1 / np.cosh(u) * np.sin(v)
        z = u - np.tanh(u)
        
        self.getAxes().plot_surface(x, y, z, **kArgs) # type: ignore