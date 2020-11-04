import numpy as np

def correct_translation(cloud):
    centroid = np.mean(cloud, axis=0)
    return cloud - centroid


def correct_rotation(cloud):
    x, y = np.mean(cloud[:, :2], axis=0)
    theta = np.arctan2(y, x)

    return rotate_cloud(cloud, -theta)


def rotate_cloud(cloud, theta):
    s = np.sin(theta)
    c = np.cos(theta)

    rotated_cloud = cloud.copy()

    rotated_cloud[:, 0] = cloud[:, 0] * c - cloud[:, 1] * s
    rotated_cloud[:, 1] = cloud[:, 0] * s + cloud[:, 1] * c

    return rotated_cloud


def sort_by_distance(cloud):
    return np.array(
        sorted(cloud, key=lambda point: np.linalg.norm(point)),
        dtype=np.float32
    )


if __name__ == "__main__":
    cloud = np.array([
        [1, -1, 2],
        [10, 20, 30],
        [5, 5, 5]
    ], dtype=np.float32)

    # print(correct_translation(cloud))
    # print(correct_rotation(cloud))
    print(sort_by_distance(cloud))

