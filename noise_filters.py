from collections import Counter
from scipy import stats
import numpy as np

def round_to_quarters(number: list) -> list:
    '''
    Helper function to round a list of numbers to the nearest quarter.

    Args
    ----
        number: list of numbers to round
    Returns
    -------
        list of numbers rounded to the nearest quarter
    '''
    return [round(i * 4) / 4 for i in number]

def find_occ_noise_quarters(xyz_all: list, xyz_back: list, thresh: int=30):
    '''
    Find coordinates that show up a certain thresh amount of occurrences,
    considered as static/background noises.
    Uses background collected data and actual data.
    Rounds all the coordinates to the nearest quarter.

    Args
    ----
        xyz_all: raw xyz_all data for all the frames
        xyz_back: raw background xyz_all data for all the frames
        thresh - min amount of times the same point shows up that will be considered as noise
    Returns
    -------
        c - dictionary of noise coordinates, key: coordinates, value: # of occurrences
    '''
    c = Counter()
    for frame_idx in range(len(xyz_all)): 
        x_r = round_to_quarters(xyz_all[frame_idx][:, 0])
        y_r = round_to_quarters(xyz_all[frame_idx][:, 1])
        z_r = round_to_quarters(xyz_all[frame_idx][:, 2])
        temp = np.dstack((x_r, y_r, z_r))[0]
        xyzv_f = [tuple(i) for i in temp]
        c.update(xyzv_f)

    for frame_idx in range(len(xyz_back)): 
        x_r = round_to_quarters(xyz_all[frame_idx][:, 0])
        y_r = round_to_quarters(xyz_all[frame_idx][:, 1])
        z_r = round_to_quarters(xyz_all[frame_idx][:, 2])
        temp = np.dstack((x_r, y_r, z_r))[0]
        xyzv_f = [tuple(i) for i in temp]
        c.update(xyzv_f)

    noise_dict = {key:value for key, value in c.items() if value > thresh}

    return noise_dict

def find_occ_noise(xyz_all: list, xyz_back: list, thresh: int=30) -> dict:
    '''
    Find coordinates that show up a certain thresh amount of occurrences,
    considered as static/background noises. 
    Uses background collected data and actual data.
    Rounds all the coordinates to the nearest tenth place or 1st decimal place.

    Args
    ----
        xyz_all: raw xyz_all data for all the frames
        xyz_back: raw background xyz_all data for all the frames
        thresh: min amount of times the same point shows up that will be considered as noise
    Returns
    -------
        c: dictionary of noise coordinates, key: coordinates, value: # of occurrences
    '''
    c = Counter()
    for frame_idx in range(len(xyz_all)): 
        x_r = (np.around(xyz_all[frame_idx][:, 0], decimals=1))
        y_r = (np.around(xyz_all[frame_idx][:, 1], decimals=1))
        z_r = (np.around(xyz_all[frame_idx][:, 2], decimals=1))
        temp = np.dstack((x_r, y_r, z_r))[0]
        xyzv_f = [tuple(i) for i in temp]
        c.update(xyzv_f)

    for frame_idx in range(len(xyz_back)): 
        x_r = (np.around(xyz_back[frame_idx][:, 0], decimals=1))
        y_r = (np.around(xyz_back[frame_idx][:, 1], decimals=1))
        z_r = (np.around(xyz_back[frame_idx][:, 2], decimals=1))
        temp = np.dstack((x_r, y_r, z_r))[0]
        xyzv_f = [tuple(i) for i in temp]
        c.update(xyzv_f)

    # Add coordinates that show a min of thresh amount of times
    noise_dict = {key:value for key, value in c.items() if value > thresh}
    
    return noise_dict

def find_mode_vel(noise_dict: dict, xyz_all: list) -> list:
    '''
    Find the most occurring velocity in each frame. 
    Used to filter out background noise, since background noises are 
    approximately around the same velocity values.

    Args
    ----
        noise_dict: coordinates that are considered noise from using find_occ_noise
        xyz_all: raw xyz_all data for all the frames
    Returns
    -------
        list of all the velocity mode across all frames
    '''
    vel = []
    for frame_idx in range(len(xyz_all)):
        x_r = (np.around(xyz_all[frame_idx][:, 0], decimals=1))
        y_r = (np.around(xyz_all[frame_idx][:, 1], decimals=1))
        z_r = (np.around(xyz_all[frame_idx][:, 2], decimals=1))

        noise = [(x_r[i], y_r[i], z_r[i]) not in noise_dict.keys() for i in range(len(x_r))]
        vel.append(stats.mode(np.around(xyz_all[frame_idx][noise, 3], decimals=2), keepdims=False))
        
    return vel
