import numpy as np
from data_cleaning import rotate_cloud

def augment_cloud(cloud):
    augmented = []
    n_points = cloud.shape[0]

    # randomly rotate in both directions
    theta = np.random.uniform(0, 5 * (np.pi/180))
    augmented.append(rotate_cloud(cloud, theta))
    augmented.append(rotate_cloud(cloud, -theta))

    # randomly delete a subset of points
    sel = np.random.choice(n_points, n_points - n_points//20)
    augmented.append(cloud.copy()[sel])

    # apply a random global translation
    x_max, y_max, z_max = cloud.abs().max(axis=0)
    translation = [
        np.random.uniform(-x_max/10, x_max/10),
        np.random.uniform(-y_max/10, y_max/10),
        np.random.uniform(-z_max/10, z_max/10),
    ]
    augmented.append(cloud + translation)

    # randomly shift every point
    translation = np.zeros(n_points, 3, dtype=np.float32)
    translation[:, 0] = np.random.uniform(-x_max/20, x_max/20, size=n_points)
    translation[:, 1] = np.random.uniform(-y_max/20, y_max/20, size=n_points)
    translation[:, 2] = np.random.uniform(-z_max/20, z_max/20, size=n_points)
    augmented.append(cloud + translation)

    return augmented