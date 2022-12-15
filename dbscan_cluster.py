from sklearn.cluster import DBSCAN
from scipy import stats
from noise_filters import *
import numpy as np

def dbscan_frame(xyzv: list, min_samp: int, eps: int) -> tuple[list, int]:
    '''
    DBSCAN on a frame

    Args
    ----
        xyzv: list of coordinates and velocity, [[x0, y0, z0, v0], ..., [xn, yn, zn, vn]]
        min_s: min # of samples to be considered around a cluster core point
        eps: max distance away from a point, epsilon value
    Returns
    -------
        labels: list of cluster numbers corresponding to each point
        num_clusters: # of clusters grouped
    '''
    # fitting the model
    dbscan = DBSCAN(eps = eps, min_samples = min_samp).fit(xyzv)
    labels = dbscan.labels_
    num_clusters = set(labels)
    # Removes noise clusters, -1 = noise label
    num_clusters.discard(-1)

    return labels, len(num_clusters)

def dbscan_mode_clust(xyz_all: list, xyz_back: list, min_samp: int, eps: int, thresh: int) -> tuple[float, list, list]:
    '''
    Calculates the mode # of clusters across all frames using DBSCAN clustering

    Args
    ----
        xyz_all: raw xyz_all data for all the frames
        xyz_back: raw background xyz_all data for all the frames
        min_s: min # of samples to be considered around a cluster core point for DBSCAN clustering
        max_range: max distance away from a cluster core point to be considered within the cluster, 
                   eps value for DBSCAN
        thresh: min threshold for # of occurances of similar points to be considered as noise
    Returns
    -------
        mode # of clusters across all frames
        list of all the clusters for all frames
        list of all the dbscan labels for all frames
    '''
    noise_dict = find_occ_noise(xyz_all=xyz_all, xyz_back=xyz_back, thresh=thresh)
    noise_vel = find_mode_vel(noise_dict=noise_dict, xyz_all=xyz_all)
    avg_clust = []
    labels = []
    for frame_idx in range(len(xyz_all)):
        x_r = (np.around(xyz_all[frame_idx][:, 0], decimals=1))
        y_r = (np.around(xyz_all[frame_idx][:, 1], decimals=1))
        z_r = (np.around(xyz_all[frame_idx][:, 2], decimals=1))
        occ_noise = [(x_r[i], y_r[i], z_r[i]) not in noise_dict.keys() for i in range(len(x_r))]
        vel_filter = (np.around(xyz_all[frame_idx][occ_noise, 3], decimals=2)) >= (min(noise_vel[frame_idx]))

        temp = np.dstack((np.around(xyz_all[frame_idx][occ_noise, 0], decimals=1)[vel_filter], 
                          np.around(xyz_all[frame_idx][occ_noise, 1], decimals=1)[vel_filter],
                          np.around(xyz_all[frame_idx][occ_noise, 2], decimals=1)[vel_filter],
                          (xyz_all[frame_idx][occ_noise, 3])[vel_filter]))[0]
        xyzv_f = [list(i) for i in temp]
        dbscan_labels, num_clust = dbscan_frame(xyzv=xyzv_f, min_samp=min_samp, eps=eps)
        labels.append(dbscan_labels)
        avg_clust.append(num_clust)

    return np.floor(min(stats.mode(avg_clust, keepdims=False))), avg_clust, labels
