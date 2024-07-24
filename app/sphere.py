""" module to make a rotating sphere animation """

import numpy as np
import config as cfg
import plotly.graph_objs as go

from plotly import subplots

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

    def get_sphere(self) -> dict:
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

    def get_adjacents(self) -> np.ndarray:
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

    def get_frame_points(self) -> list:
        """ function to rotate sphere along z-axis """

        aniamtion_frames = []
        phis = self.phi
        rotations = np.arange(start=0, stop=1, step=cfg.ANIMATION_STEP)
        for rotation in rotations:
            thetas = self.theta + rotation
            sphere_x = []
            sphere_y = []
            sphere_z = []
            for theta in thetas:
                for phi in phis:
                    x_value, y_value, z_value = self.get_sphere_points(theta, phi)
                    sphere_x.append(x_value)
                    sphere_y.append(y_value)
                    sphere_z.append(z_value)
            aniamtion_frames.append([sphere_x, sphere_y, sphere_z])
        return aniamtion_frames

class Plot():
    """ class to plot the given sphere and its animations """

    def __init__(self, sphere_data: dict, adjacent_points: dict, animation_frames: list) -> None:
        self.sphere_data = sphere_data
        self.edges = adjacent_points
        self.animation_frames = animation_frames
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

    def plot_sphere(self) -> list:
        """ function to plot the scatter 3d plotly figure """

        return [
            go.Scatter3d(
                x=self.sphere_data["x_values"],
                y=self.sphere_data["y_values"],
                z=self.sphere_data["z_values"],
                mode="markers", name="3D Sphere", opacity=0.6,
                marker={"color": cfg.COLOR, "size": cfg.MARKER_SIZE}
            )
        ]

    def update_plot(self) -> None:
        """ function to set 3D scene properties """

        self.figure.update_layout(
            title="Sphere Animation",
            scene={
                "xaxis": {"title": "X-axis"},
                "yaxis": {"title": "Y-axis"},
                "zaxis": {"title": "Z-axis"}
            },
            showlegend=False,
            updatemenus=[
                {
                    "type": "buttons", "buttons":[
                        {
                            "label": "Animate", "method":"animate",
                            "args":[
                                None,
                                {
                                    "frame": {"duration": 10},
                                    "transition": {"duration": 100}
                                }
                            ]
                        }
                    ]
                }
            ]
        )

    def animate(self) -> None:
        """ function to get animation frames """

        frames = []
        for frame in self.animation_frames:
            frames.append(
                go.Frame(
                    data=[
                        go.Scatter3d(
                            x=frame[0], y=frame[1], z=frame[2],
                            mode="markers", name="3D Sphere", opacity=0.6,
                            marker={"color": cfg.COLOR, "size": cfg.MARKER_SIZE}
                        )
                    ]
                )
            )
        return frames

    def run(self) -> None:
        """ class entry point """

        self.figure = go.Figure(
            data=self.plot_sphere(), frames=self.animate()
        )
        self.update_plot()
        self.figure.write_html("Animated Sphere.html")

if __name__ == "__main__":

    sphere_obj = Sphere()
    sphere_obj.make_sphere()
    plot_obj = Plot(
        sphere_obj.get_sphere(), sphere_obj.get_adjacents(), sphere_obj.get_frame_points()
    )
    plot_obj.run()
