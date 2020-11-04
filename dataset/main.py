import os
import json
import numpy as np
import pptk


for cloud in os.scandir("clouds"):
    X = np.loadtxt(cloud)
    cones = []

    v = pptk.viewer(X)
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


