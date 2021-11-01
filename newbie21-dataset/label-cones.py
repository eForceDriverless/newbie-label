import os
import json
import sys
import platform
import pptk

from common import get_number, update_colors, read_dataset_to_numpy


def save_cones(path, cones):
    cones = [cone.tolist() for cone in cones]

    new_cones = []
    for cone in cones:
        new_cone = [{ "x": x, "y": y, "z": z, "intensity": i } for (x, y, z, i) in cone]
        new_cones.append(new_cone)

    cones = new_cones

    with open(path, "w") as f:
        json.dump(cones, f)


if __name__ == "__main__":
    is_windows = platform.system() == "Windows"

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    start = int(sys.argv[3])
    end = int(sys.argv[4])

    files = [f for f in os.scandir(input_path) if f.is_file()]
    files = [f for f in files if get_number(f.name) >= start and get_number(f.name) <= end]
    files.sort(key=lambda f: get_number(f.name))

    for entry in files:
        name = entry.name
        path = entry.path

        print(f"Reading pointcloud from {path}")

        cloud = read_dataset_to_numpy(path)

        v = pptk.viewer(cloud[:, :3], cloud[:, 3])
        v.color_map("jet")
        v.set(point_size=0.02)

        cones = []

        while True:
            v.wait()
            indices = v.get("selected")

            if len(indices) == 0:
                if len(cones) != 0:
                    filename = os.path.join(output_path, f"cones{get_number(name)}.json")
                    print(f"Saving cones to {filename}")
                    save_cones(filename, cones)

                v.clear()
                v.close()
                break

            cones.append(cloud[indices])

            if True:
                draw = update_colors(cloud, cones)

                print("Redrawing...")

                r = v.get("r")
                phi = v.get("phi")
                theta = v.get("theta")
                lookat = v.get("lookat")

                v.clear()
                v.load(draw[:, :3], draw[:, 3])
                v.set(r=r, phi=phi, theta=theta, lookat=lookat, selected=[])
