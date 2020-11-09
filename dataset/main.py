import os
import json
import numpy as np
import pptk


clouds = sorted(os.scandir("clouds"), key=lambda e: e.name)

for cloud in clouds:
    X = np.loadtxt(cloud)
    cones = []

    v = pptk.viewer(X[:, :3], X[:, 3])
    v.color_map("jet")
    while True:
        v.wait()
        indices = v.get("selected")
        
        if len(indices) == 0:
            v.close()

            if len(cones) != 0:
                filename = f"cones/{cloud.name[:-4]}_cones.json"
                print(f"Saving to {filename}")

                with open(filename, "w") as f:
                    json.dump(cones, f)

            break

        cones.append(X[indices].tolist())


