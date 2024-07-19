""" module to make a rotating sphere animation """

import numpy as np
import config as cfg
import tensorflow as tf

import plotly.graph_objs as go 

class Sphere():
    """ class to define a sphere about origin """

    def __init__(self) -> None:

        self.x = np.arange(start=cfg.X_MIN, stop=cfg.X_MAX+1, step=cfg.X_STEP)
        self.y = np.arange(start=cfg.Y_MIN, stop=cfg.Y_MAX+1, step=cfg.Y_STEP)

        x_grid = np.asarray([x for x in self.x for _ in self.y])
        self.x_values = np.concatenate([x_grid, x_grid])

        y_grid = np.asarray([y for _ in self.x for y in self.y])
        self.y_values = np.concatenate([y_grid, y_grid])

        z_grid = np.asarray(
            [
                np.sqrt(np.square(cfg.RADIUS) - (np.square(x) + np.square(y))) \
                    if np.square(x) + np.square(y) < np.square(cfg.RADIUS) else np.nan \
                        for x in self.x for y in self.y
            ]
        )
        self.z_values = np.concatenate([z_grid, -z_grid])

    def get_sphere(self):
        """ function to return sphere data-points """
        return {
            "x_values": self.x_values,
            "y_values": self.y_values,
            "z_values": self.z_values 
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
    plot_obj = Plot(sphere_obj.get_sphere())
    plot_obj.run()
