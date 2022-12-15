from noise_filters import *
from dbscan_cluster import *
from plotting import *
import scipy.io as sio
import argparse

PLOT = True
COLOR = True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data', action='store', dest='data',
                        help='Path to actual .mat data file', required=True)
    parser.add_argument('-b', '--back', action='store', dest='back',
                        default='',
                        help='Path to background .mat data file')
    parser.add_argument('-pl', '--plot', action='store', dest='plot',
                        default='True', choices=['True', 'False'],
                        help='Plot enabled/disabled')
    parser.add_argument('-a', '--axis', action='store', dest='axis',
                        default='xyz', choices=['xyz', 'xy', 'xz', 'yz'],
                        help='Which axes to use to plot')
    parser.add_argument('-c', '--color', action='store', dest='color',
                        default='velocity', choices=['velocity', 'cluster'],
                        help='Which color key to use for coordinate points')


    args = parser.parse_args()
    global PLOT, COLOR
    PLOT = args.plot == 'True'
    COLOR = args.color == 'velocity'

    # Load the .mat data files and get the xyz and velocity values
    xyz_all = sio.loadmat(args.data)['xyz_all'][0]
    if args.back != '':
        xyz_back = sio.loadmat(args.back)['xyz_all'][0]
    else:
        xyz_back = []

    # Calculate the obj count using DBSCAN clustering
    obj_count, avg_clust, labels = dbscan_mode_clust(xyz_all=xyz_all, 
                                                     xyz_back=xyz_back, 
                                                     min_samp=MIN_SAMP, 
                                                     eps=EPS, thresh=OCC_THRESH)
    print(f'MMWCAS OBJECT COUNT: {obj_count}')
    if PLOT:
        plot_data(xyz_data=xyz_all, xyz_back=xyz_back, axis=args.axis, 
                  color=COLOR, clusters=avg_clust, clust_label=labels)

if __name__ == '__main__':
    main()
