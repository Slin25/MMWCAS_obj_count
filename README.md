# MMWCAS_obj_count
Object counting algorithm using DBSCAN clustering for mmWave Cascade radar. The accuracy of the algorithm still needs to be tested on more data.

## Directory Overview
```
├── point_cloud_plot.py         # Raw point cloud plotting without filtering
├── obj_count.py                # Calculate object count
├── dbscan_cluster.py           # DBSCAN clustering helper functions
├── noise_filters.py            # Background noise filtering functions
├── plotting.py                 # Plotting point cloud with filtering
├── requirements.txt            # Required Python libraries to install
├── docs/                       # Images for documentation
├── LICENSE
└── README.md
```

## Hardware Setup
### Required Hardware:
- [MMWCAS-RF-EVM](https://www.ti.com/tool/MMWCAS-RF-EVM)
  - [User Guide and Technical Specs](https://www.ti.com/lit/pdf/swru553)
- [MMWCAS-DSP-EVM](https://www.ti.com/tool/MMWCAS-DSP-EVM)
  - [User Guide and Technical Specs](https://www.ti.com/lit/pdf/spruis6)
- Ethernet Cable
- USBA to miniB Cable
- 12V, 3A, DC barrel plug
## Software Setup
### External Software
- MMWAVE-STUDIO
  - [Setup Guide](https://software-dl.ti.com/ra-processors/esd/MMWAVE-STUDIO-2G/latest/index_FDS.html)
    - Please follow the instructions in the 3. Software Pre-requisites and 4. Setting Up TDA Capture Card section in the setup guide
    - Follow section 7. Device Configuration (mmWaveStudio) for capturing data using mmWaveStudio
    - Under section 7.2 Running LUA Script, use Case 2: MIMO Configurations
    - To use the default post processing that mmWave Studio provides, follow section 8.2 Post Processing the ADC Data
    - To use the example MATLAB plotting scripts as shown in section 8.3.2.3 Post-processing, follow section 8.3.1 Calibration up to 8.3.2.3
- MATLAB
  - Path to example MATLAB scripts `<PATH to ti>/mmwave_studio_<VERSION #>/mmWaveStudio/MatlabExamples/4chip_cascade_MIMO_example/main/cascade/`
  - Inside of `<PATH to ti>/mmwave_studio_<VERSION #>/mmWaveStudio/MatlabExamples/4chip_cascade_MIMO_example/main/cascade/cascade_MIMO_signalProcessing.m`Change `SAVEOUTPUT_ON` to `1` to save the output data to a `.mat` file, which will be used for object count or point cloud plotting in python

To install requirements
```
pip3 install -r ./requirements.txt
```

## Background Filtering Overview
First, collect some background noise data of the environment without any objects in front of the radar, then do the actual data collection with the object in front. By using both the background data and the actual data, we would first count the number of occurrences of each coordinate point, if the number of occurrences is above a certain threshold that we set, then we consider those coordinates as background coordinate points. The second layer of filtering is filtering out specific velocities, since background noise has around the same velocities. To calculate the noise’s velocities, we would go through each frame and find out the most occurred velocities from all the points and use that velocity to filter out all the coordinates that are below that threshold.
<img src="/docs/background_filter_flowchart.png" alt="Background Flowchart" width="75%"/>

## Clustering Overview
The clustering algorithm that showed the best results was using Density-Based Spatial Clustering of Applications with Noise (DBSCAN), since we still have noise in our data. The advantage of using DBSCAN is that it is also able to filter out outlier noises that do not have enough points clustered around to be considered a cluster. By using DBSCAN across all the frames in the data, we would find the number of clusters within each frame and at the end, do a mode operation, finding the most occurring number of clusters across all the frames, therefore we would be able to find the object count in the data.
<img src="/docs/clustering_flowchart.png" alt="Clustering Flowchart" width="75%"/>
## Run Project
To plot the point cloud of the raw data
```shell
python3 point_cloud_plot.py -p <PATH to .mat file>
```
Should see a popup window of the point cloud and a frame slider at the bottom:

<img src="/docs/point_cloud_example.png" alt="Point Cloud Example Popup" width="30%"/>

To calculate the object count
```shell
python3 obj_count.py -d <PATH to actual data .mat file> -b <PATH to background data .mat file>
```
Should see a popup window of the filtered point cloud a frame slider at the bottom and the object count result printed in your terminal:

<img src="/docs/obj_count_example.png" alt="Object Count Example Popup" width="30%"/>

To calculate the object count without plotting
```shell
python3 obj_count.py -d <PATH to actual data .mat file> -b <PATH to background data .mat file> -pl False
```

To calculate the object count and show the cluster colors
```shell
python3 obj_count.py -d <PATH to actual data .mat file> -b <PATH to background data .mat file> -c cluster
```
Should see a similar popup, but now the colors of the points are grouped by the clusters:

<img src="/docs/obj_count_clust_example.png" alt="Object Count Example Popup" width="30%"/>
