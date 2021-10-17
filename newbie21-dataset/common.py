import json
import re
import numpy as np


def read_dataset_to_numpy(filename):
    with open(filename) as f:
        pointcloud = json.load(f)

    array = np.zeros((len(pointcloud), 4), dtype=np.float)

    for i, point in enumerate(pointcloud):
        array[i] = [point["x"], point["y"], point["z"], point["intensity"]]

    return array


def numpy_to_json(cloud):
    data = []

    for point in cloud:
        data.append({"x": point[0], "y": point[1], "z": point[2], "intensity": point[3]})

    return data


def get_number(name):
    name = name.split(".")[0]
    match = re.search(r'^.*?(\d+)$', name)
    return int(match.group(1))


def preprocess(cloud, min_radius, max_radius):
    cloud = cloud[cloud[:, 0] > 0]
    dist_squared = np.square(cloud[:, 0]) + np.square(cloud[:, 1])

    cloud = cloud[(dist_squared > min_radius**2) & (dist_squared < max_radius**2)]

    return cloud


def set_point_color(cloud, point):
    color = np.max(cloud[:, 3])
    dist = np.sqrt(np.square(cloud[:, 0] - point[0]) +
                   np.square(cloud[:, 1] - point[1]) + np.square(cloud[:, 2] - point[2]))
    cloud[dist < 0.001, 3] = color


def update_colors(cloud, cones):
    cloud = cloud.copy()

    for cone in cones:
        for point in cone:
            set_point_color(cloud, point)

    return cloud
