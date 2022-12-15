import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import argparse

VEL_THRESH = 0.0

xyz_lut = {
    'x': 0,
    'y': 1,
    'z': 2,
}

def plot_data(xyz_data: list, axis: str) -> None:
    """
    Plots the raw data and removes the absolute velocities less than VEL_THRESH.
    A frame slider bar to change which frame to plot and the color of the point
    corresponds to a velocity value with the color key on the right side.

    Args
    ---------
        xyz_data: raw xyz and velocity data for all the frames
        axis: which axes to plot from the options of ['xyz', 'xy', 'xz', 'yz']
    Returns
    -------
        NONE
    """

    # XYZ Limits
    X_PLIM, Y_PLIM, Z_PLIM = [np.max([np.max(xyz_data[i][:, j]) for i in range(len(xyz_data))]) for j in range(3)]
    X_NLIM, Y_NLIM, Z_NLIM = [np.min([np.min(xyz_data[i][:, j]) for i in range(len(xyz_data))]) for j in range(3)]

    xyz_lim = {
        'x': [X_NLIM, X_PLIM],
        'y': [Y_NLIM, Y_PLIM],
        'z': [Z_NLIM, Z_PLIM]
    }

    def set_lim(ax, frame_idx):
        ax.set_title(f'{len(axis)}D Point Cloud of Frame {frame_idx}')
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
    # Velocity filtering
    vel_all = abs(xyz_data[frame_idx][:, 3]) >= VEL_THRESH
    fig = plt.figure(figsize = (6, 6))
    plt.subplots_adjust(bottom=0.1)
    if len(axis) == 3:
        ax = fig.add_subplot(projection=f'3d')
    else:
        ax = fig.add_subplot()
    set_lim(ax, frame_idx)

    # Location of the frame sliding bar
    axfreq = plt.axes([0.25, 0.005, 0.65, 0.03])
    frame = Slider(axfreq, 'Frame', 0, len(xyz_data)-1, 0, valstep=1)

    def update(val):
        frame_idx = int(frame.val)
        # Velocity filtering
        vel_all = abs(xyz_data[frame_idx][:, 3]) >= VEL_THRESH
        
        ax.cla()
        set_lim(ax, frame_idx)
        ax.scatter(*[xyz_data[frame_idx][vel_all, xyz_lut[i]] for i in axis], c=xyz_data[frame_idx][vel_all, 3])

    # Updates the plot based on the new frame #
    frame.on_changed(update)

    p = ax.scatter(*[xyz_data[frame_idx][vel_all, xyz_lut[i]] for i in axis], c=xyz_data[frame_idx][vel_all, 3])

    fig.colorbar(p, ax=ax, pad=0.2, label="Velocity (m/s)", shrink=0.5)
    plt.show()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', action='store', dest='path',
                        help='Path to .mat data file', required=True)
    parser.add_argument('-a', '--axis', action='store', dest='axis',
                        default='xyz', choices=['xyz', 'xy', 'xz', 'yz'],
                        help='Which axes to use to plot')
    parser.add_argument('-v', '--velocity', action='store', dest='velocity',
                        default=0.0, 
                        help='Velocity threshold to parse out from data')
    args = parser.parse_args()
    global VEL_THRESH
    VEL_THRESH = float(args.velocity)

    # Load the .mat data file and get the xyz and velocity values
    xyz_all = sio.loadmat(args.path)['xyz_all'][0]
    plot_data(xyz_data=xyz_all, axis=args.axis)

if __name__ == '__main__':
    main()
