# -*- coding: utf-8 -*-
# @Filename:HosVisual.py
# @Author:Ymh
# @Date:2026-2
# @IDE:PyCharm

import numpy as np
import matplotlib.pyplot as plt

#%%
filename = r"\\wsl.localhost\Ubuntu-22.04\home\yumh\HOS-Ocean\run\R3\Results\3d.dat"

# counting time steps
time_steps = 0
with open(filename, 'r') as f:
    for line in f:
        if line.startswith("ZONE SOLUTIONTIME"):
            time_steps += 1

print("Total time steps:", time_steps)

with open(filename, 'r') as f:

    t_index = -1
    data_counter = 0

    for line in f:

        line = line.strip()

        # find the 'ZONE SOLUTIONTIME'
        if line.startswith("ZONE SOLUTIONTIME"):

            t_index += 1
            data_counter = 0

            parts = line.replace(',', '').split()

            # the first 'ZONE SOLUTIONTIME'
            if t_index == 0:
                I = int(parts[parts.index('I=') + 1])
                J = int(parts[parts.index('J=') + 1])

                print("Grid:", I, J)

                # 预分配（float32 节省内存）
                eta = np.zeros((time_steps, I, J), dtype=np.float32)
                phis = np.zeros((time_steps, I, J), dtype=np.float32)
                time_list = np.zeros(time_steps)

                x = np.zeros((I, J), dtype=np.float32)
                y = np.zeros((I, J), dtype=np.float32)

            time_str = line.split('=')[1].split(',')[0]
            time_list[t_index] = float(time_str)

            continue

        if line.startswith("TITLE") or line.startswith("VARIABLES"):
            continue

        if t_index == -1:
            continue

        values = line.split()

        # 第一时间步
        if t_index == 0:

            if len(values) == 4:

                i = data_counter // J
                j = data_counter % J

                x[i, j] = float(values[0])
                y[i, j] = float(values[1])
                eta[t_index, i, j] = float(values[2])
                phis[t_index, i, j] = float(values[3])

                data_counter += 1

        # 后续时间步
        else:

            if len(values) == 2:

                i = data_counter // J
                j = data_counter % J

                eta[t_index, i, j] = float(values[0])
                phis[t_index, i, j] = float(values[1])

                data_counter += 1

print("Done.")
print("eta shape:", eta.shape)

#%% for 2D
t = 100

plt.figure()
plt.plot(eta[t,:,0]) # the y line
plt.show()

#%% for 3D

# Create a figure and a 3D axis
fig = plt.figure()
ax = plt.axes(projection='3d')

surf = ax.plot_surface(x,y,eta[t,:,:], cmap='viridis')

# color bar
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)

# labels and limits
ax.set_xlabel('X-axis')
ax.set_xlim(0, 2)
ax.set_ylabel('Y-axis')
ax.set_ylim(0, 2)
ax.set_zlabel('Z-axis')
ax.set_zlim(np.min(eta), np.max(eta))
ax.set_title('3D Surface with 2D Contour Projections')

plt.show()
