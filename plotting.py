from matplotlib.widgets import Slider
from noise_filters import *
from dbscan_cluster import *
import matplotlib.pyplot as plt

OCC_THRESH = 30     # Min # of occurrences to be considered as noise
MIN_SAMP = 4        # DBSCAN, min # of samples around a point
EPS = 3             # DBSCAN, max radius range around a point

xyz_lut = {
    'x': 0,
    'y': 1,
    'z': 2,
}

def plot_data(xyz_data: list, xyz_back: list, axis: str, color: bool, clusters: list, clust_label: list) -> None:
    '''
    Plots the data with background filtering applied.
    A frame slider bar to change which frame to plot and the color of the point
    corresponds to a velocity value with the color key on the right side if color is True,
    else the color is based on the cluter groupings.

    Args
    ----
        xyz_data: raw xyz and velocity data for all the frames
        xyz_back: background xyz and velocity data for all the frames
        axis: which axes to plot from the options of ['xyz', 'xy', 'xz', 'yz']
        color: chooses to use velocity (True) or cluster labels (False) as color key
        clusters: list of all the cluster number for all frames
        clust_labels: list of cluster grouping for all frames
    Returns
    -------
        NONE
    '''

    # XYZ Limits
    X_PLIM, Y_PLIM, Z_PLIM = [np.max([np.max(xyz_data[i][:, j]) for i in range(len(xyz_data))]) for j in range(3)]
    X_NLIM, Y_NLIM, Z_NLIM = [np.min([np.min(xyz_data[i][:, j]) for i in range(len(xyz_data))]) for j in range(3)]

    noise_dict = find_occ_noise(xyz_all=xyz_data, xyz_back=xyz_back, thresh=OCC_THRESH)
    noise_vel = find_mode_vel(noise_dict = noise_dict, xyz_all=xyz_data)

    xyz_lim = {
        'x': [X_NLIM, X_PLIM],
        'y': [Y_NLIM, Y_PLIM],
        'z': [Z_NLIM, Z_PLIM]
    }

    def set_lim(ax, frame_idx, num_clust):
        ax.set_title(f'{len(axis)}D Point Cloud of Frame {frame_idx}, # Clusters: {num_clust}')
        for idx, i in enumerate(axis):
            if idx == 0:
                ax.set_xlabel(f'{i} (m)')
                ax.axes.set_xlim(left=xyz_lim[i][0], right=xyz_lim[i][1])
            if idx == 1:
                ax.set_ylabel(f'{i} (m)')
                ax.axes.set_ylim(bottom=xyz_lim[i][0], top=xyz_lim[i][1])
            if idx == 2:
                ax.set_zlabel(f'{i} (m)')
                ax.axes.set_zlim3d(bottom=xyz_lim[i][0], top=xyz_lim[i][1])

    frame_idx = 0
    fig = plt.figure(figsize = (6, 6))
    plt.subplots_adjust(bottom=0.1)
    if len(axis) == 3:
        ax = fig.add_subplot(projection=f'3d')
    else:
        ax = fig.add_subplot()
    set_lim(ax, frame_idx, clusters[frame_idx])

    # Location of the frame sliding bar
    axfreq = plt.axes([0.25, 0.005, 0.65, 0.03])
    frame = Slider(axfreq, 'Frame', 0, len(xyz_data)-1, 0, valstep=1)

    def update(val):
        frame_idx = int(frame.val)
        # Filtering
        x_r = (np.around(xyz_data[frame_idx][:, 0], decimals=1))
        y_r = (np.around(xyz_data[frame_idx][:, 1], decimals=1))
        z_r = (np.around(xyz_data[frame_idx][:, 2], decimals=1))
        occ_noise = [(x_r[i], y_r[i], z_r[i]) not in noise_dict.keys() for i in range(len(x_r))]
        vel_filter = (np.around(xyz_data[frame_idx][occ_noise, 3], decimals=2)) >= (min(noise_vel[frame_idx]))
        
        ax.cla()
        set_lim(ax, frame_idx, clusters[frame_idx])
        ax.scatter(*[(xyz_data[frame_idx][occ_noise, xyz_lut[i]])[vel_filter] for i in axis], 
                   c=(xyz_data[frame_idx][occ_noise, 3])[vel_filter] if color else clust_label[frame_idx])

    # Updates the plot based on the new frame #
    frame.on_changed(update)

    # Filtering
    x_r = (np.around(xyz_data[frame_idx][:, 0], decimals=1))
    y_r = (np.around(xyz_data[frame_idx][:, 1], decimals=1))
    z_r = (np.around(xyz_data[frame_idx][:, 2], decimals=1))
    occ_noise = [(x_r[i], y_r[i], z_r[i]) not in noise_dict.keys() for i in range(len(x_r))]
    vel_filter = (np.around(xyz_data[frame_idx][occ_noise, 3], decimals=2)) >= (min(noise_vel[frame_idx]))
    
    p = ax.scatter(*[(xyz_data[frame_idx][occ_noise, xyz_lut[i]])[vel_filter] for i in axis], 
                   c=(xyz_data[frame_idx][occ_noise, 3])[vel_filter] if color else clust_label[frame_idx])

    if color:
        fig.colorbar(p, ax=ax, pad=0.2, label="Velocity (m/s)", shrink=0.5)
    plt.show()
