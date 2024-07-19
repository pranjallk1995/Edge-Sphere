""" module to make a rotating sphere animation """

import numpy as np
import config as cfg
import tensorflow as tf

import plotly.graph_objs as go 

class Sphere():
    """ class to define a sphere about origin """

    def __init__(self) -> None:
        self.theta = np.arange(start=0, stop=2*np.pi, step=0.3)
        self.phi = np.arange(start=0, stop=2*np.pi, step=0.3)

        self.x_values = []
        self.y_values = []
        self.z_values = []

    def make_sphere(self) -> None:
        """ function to generate points on the required sphere """
        for theta in self.theta:
            for phi in self.phi:
                self.x_values.append(np.square(cfg.RADIUS)*np.cos(theta)*np.cos(phi))
                self.y_values.append(np.square(cfg.RADIUS)*np.sin(theta)*np.cos(phi))
                self.z_values.append(cfg.RADIUS*np.sin(phi))

    def get_sphere(self):
        """ function to return sphere data-points """
        return {
            "x_values": np.asarray(self.x_values),
            "y_values": np.asarray(self.y_values),
            "z_values": np.asarray(self.z_values) 
        }

class Animate():
    pass

class Plot():
    """ class to plot the given sphere and its animations """

    def __init__(self, sphere_data: dict) -> None:
        self.sphere_data = sphere_data
        self.figure = None

    def plot_sphere(self) -> go.Figure:
        """ function to return the scatter 3d plotly figure """

        return go.Figure(
            [
                go.Scatter3d(
                    x=self.sphere_data["x_values"],
                    y=self.sphere_data["y_values"],
                    z=self.sphere_data["z_values"],
                    mode="markers", name="3D Sphere",
                    marker={"color": cfg.COLOR, "size": cfg.MARKER_SIZE}
                )
            ]
        )

    def update_plot(self) -> None:
        """ function to set 3D scene properties """

        self.figure.update_layout(
            template="plotly_dark", title="Sphere Animation",
            scene={
                "xaxis": {"title": "X-axis"},
                "yaxis": {"title": "Y-axis"},
                "zaxis": {"title": "Z-axis"}
            },
            showlegend=False
        )

    def run(self) -> None:
        """ class entry point """

        self.figure = self.plot_sphere()
        self.update_plot()
        self.figure.write_html("Animated Sphere.html")

if __name__ == "__main__":

    sphere_obj = Sphere()
    sphere_obj.make_sphere()
    plot_obj = Plot(sphere_obj.get_sphere())
    plot_obj.run()
