""" module to make a rotating sphere animation """

import numpy as np
import config as cfg
import tensorflow as tf

import plotly.graph_objs as go 

class Sphere():
    """ class to define a sphere about origin """

    def __init__(self) -> None:

        self.theta = np.arange(start=0, stop=2*np.pi, step=cfg.ANGLE_STEP)
        self.phi = np.arange(start=0, stop=2*np.pi, step=cfg.ANGLE_STEP)

        self.x_values = []
        self.y_values = []
        self.z_values = []

    def get_sphere_points(self, theta: float, phi: float) -> list:
        """ function to calculate 3d coordinates of the sphere """

        return [
            np.square(cfg.RADIUS)*np.cos(theta)*np.cos(phi),
            np.square(cfg.RADIUS)*np.sin(theta)*np.cos(phi),
            cfg.RADIUS*np.sin(phi)
        ]

    def make_sphere(self) -> None:
        """ function to generate points on the required sphere """

        for theta in self.theta:
            for phi in self.phi:
                x_value, y_value, z_value = self.get_sphere_points(theta, phi)
                self.x_values.append(x_value)
                self.y_values.append(y_value)
                self.z_values.append(z_value)

    def get_sphere(self):
        """ function to return sphere data-points """

        return {
            "x_values": np.asarray(self.x_values),
            "y_values": np.asarray(self.y_values),
            "z_values": np.asarray(self.z_values) 
        }

    def get_next_angle(self, angle: float) -> float:
        """ function to get next angle """
        if angle + cfg.ANGLE_STEP < 2*np.pi:
            return angle + cfg.ANGLE_STEP
        return 0

    def get_previous_angle(self, angle: float) -> float:
        """ function to get previous angle """
        if angle - cfg.ANGLE_STEP >= 0:
            return angle - cfg.ANGLE_STEP
        return np.floor(2*np.pi)

    def find_adjacents(self) -> dict:
        """ function to find adjacent edges on the sphere """

        adjacents = {}
        for theta in self.theta:
            for phi in self.phi:
                adjacents[(theta, phi)] = np.asarray(
                    [
                        [self.get_next_angle(theta), phi],
                        [theta, self.get_next_angle(phi)]
                    ]
                )
        return adjacents

    def get_adjacent_points(self, x: float, y: float, z: float) -> list:
        """ function to get closest existing point """
        return np.asarray(
            [
                self.x_values[np.argmin(np.abs(self.x_values - x))],
                self.y_values[np.argmin(np.abs(self.y_values - y))],
                self.z_values[np.argmin(np.abs(self.z_values - z))]
            ]
        )

    def get_adjacents(self) -> list:
        """ function to find adjacent edges on the sphere """

        edges = []
        adjacents = self.find_adjacents()
        for edge_start, end_points in adjacents.items():
            current_x, current_y, current_z = self.get_sphere_points(
                theta=edge_start[0], phi=edge_start[1]
            )
            current_x_value, current_y_value, current_z_value = self.get_adjacent_points(
                current_x, current_y, current_z
            )
            for end_point in end_points:
                adjacent_x, adjacent_y, adjacent_z = self.get_sphere_points(
                    theta=end_point[0], phi=end_point[1]
                )
                adjacent_x_value, adjacent_y_value, adjacent_z_value = self.get_adjacent_points(
                    adjacent_x, adjacent_y, adjacent_z
                )
                edges.append(
                    [
                        [current_x_value, adjacent_x_value],
                        [current_y_value, adjacent_y_value],
                        [current_z_value, adjacent_z_value]
                    ]
                )
        return np.asarray(edges)

class Animate():
    pass

class Plot():
    """ class to plot the given sphere and its animations """

    def __init__(self, sphere_data: dict, adjacent_points: dict) -> None:
        self.sphere_data = sphere_data
        self.edges = adjacent_points
        self.figure = None

    def plot_edges(self) -> list:
        """ function to plot the edges in the plotly figure """

        edges_trace = []
        for edge_x, edge_y, edge_z in self.edges:
            edges_trace.append(
                go.Scatter3d(
                    x=edge_x, y=edge_y, z=edge_z, mode="lines",
                    marker={"color": cfg.EDGE_COLOR}, opacity=0.3
                )
            )
        return edges_trace

    def plot_sphere(self) -> go.Figure:
        """ function to plot the scatter 3d plotly figure """

        return go.Scatter3d(
            x=self.sphere_data["x_values"],
            y=self.sphere_data["y_values"],
            z=self.sphere_data["z_values"],
            mode="markers", name="3D Sphere", opacity=0.6,
            marker={"color": cfg.COLOR, "size": cfg.MARKER_SIZE}
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

        self.figure = go.Figure(
            [self.plot_sphere()] + self.plot_edges()
        )
        self.update_plot()
        self.figure.write_html("Animated Sphere.html")

if __name__ == "__main__":

    sphere_obj = Sphere()
    sphere_obj.make_sphere()
    plot_obj = Plot(sphere_obj.get_sphere(), sphere_obj.get_adjacents())
    plot_obj.run()
