#!/usr/bin/python3
# This project goal was to perform conversion from gps location data to curvature file needed in ChassisSim. The project
# was started when data logger on Tampere Formula Student -19 (TFS19) could not provide accurate acceleration data for
# ChassisSim software.
#
# Creator: Waltteri Koskinen
# v1.3 26.01.2020

import numpy as np
from matplotlib import pyplot as plt
import argparse


def gps2meter(long, lat):
    """
    Function takes long and lat coordinates and converts them to meters in cartesian coordinate system.
    First data point is threaded as an origo.

    :param long: Longitude coordinates list
    :param lat: Latitude coordinates list
    :return: x ,y coordinates in lists as meters
    """
    R_E = 6.3781 * 10 ** 6
    lat2meter = 111.3199 * 10 ** 3
    equator_circ = 2*R_E*np.pi

    x = [0]
    y = [0]
    for i in range(len(long)-1):
        long_m = (long[i+1]-long[i])*equator_circ*np.cos(np.deg2rad(lat[i+1]))/360+x[i]
        x.append(long_m)
        y.append((lat[i+1]-lat[i])*lat2meter+y[i])

    return x, y


def curvature_cal(x, y):
    """
    Calculates cumulative travel, curvature of each segment and components of curvature vectors.

    :param x: x coordinates list
    :param y: y coordinates list
    :return: Cumulative travel, curvatures with sign and k_urvature vectors
    """
    z = np.zeros(len(x))

    track = np.transpose(np.array([x, y, z]))
    L = [0]
    curvature = [0]
    k = np.array([[0, 0, 0]])
    for i in range(len(x)-2):
        R, k_i = circumcenter(track[i,:], track[i+1,:], track[i+2,:])
        k = np.append(k, [np.transpose(k_i)], axis=0)
        L.append(L[i]+np.linalg.norm(track[i, :]-track[i-1, :]))
        sign = np.sign(np.cross(track[i+1, :]-track[i, :], k_i)[2])
        curvature.append(R**(-1)*sign)

    return L, curvature, k


def circumcenter (B, A, C):
    """
    Calculates curvature vectors and radius of route from three points in xy plane

    :param B: coordinates (x,y) of current point
    :param A: coordinates (x,y) of point before
    :param C: coordinates (x,y) of point after
    :return: R_adius of each section and components of k_urvature vector
    """

    D = np.cross(B-A, C-A)
    b = np.linalg.norm(A-C)
    c = np.linalg.norm(A-B)
    E = np.cross(D, B-A)
    F = np.cross(D, C-A)
    G = (b**2*E-c**2*F)/np.linalg.norm(D)**2/2
    R = np.linalg.norm(G)

    if R == 0:
        k = G
    else:
        k = np.transpose(G)/R**2

    return R, k


def filter(x, y, min_dist):
    """
    Filters data points based on distance between them. Uses filter argument to determinate minimum distance parameter.
    :param x: in meters
    :param y: in meters
    :return: Returns filtered x, y coordinates
    """

    x_filt = [x[0]]
    y_filt = [y[0]]
    for i in range(len(x)-1):
        if np.sqrt((x[i+1]-x_filt[-1])**2+(y[i+1]-y_filt[-1])**2) > float(min_dist):
            x_filt.append(x[i+1])
            y_filt.append(y[i+1])

    return x_filt, y_filt


def plot(x, y, k):
    plt.plot(x, y)
    plt.quiver(x, y, k[:, 0], k[:, 1], color='red')
    plt.grid('both')
    plt.show()

    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='state input file')
    parser.add_argument('-m', '--meters', action='store_true',
                        help='use if the input file is already in meters')
    parser.add_argument('-d', '--delimiter', action='store', default='\t',
                        help='specify the delimiter used in the input file')
    parser.add_argument('-f', '--filter', action='store',
                        help='specify minimum distance between two points in meters')
    parser.add_argument('-o', '--output', action='store',
                        help='state output filename')
    parser.add_argument('-p', '--plot', action='store_true',
                        help='plots the track and curvature vectors in it')

    args = parser.parse_args()

    try:
        long, lat = np.loadtxt(args.input, delimiter=args.delimiter, unpack=True)
    except OSError as e:
        print('Error occurred while opening the file.')
        print(e)
        return False
    except ValueError as e:
        print('Error occurred while reading the file. Check the delimiter in input file. Default is set to "Tab"')
        print(e)
        return False

    if not args.meters:
        x, y = gps2meter(long, lat)
    else:
        x = long
        y = lat

    if args.filter:
        x, y = filter(x, y, args.filter)


    L, curvature, k = curvature_cal(x, y)

    data_to_save = np.array([curvature, L])
    data_to_save = data_to_save.T

    if not args.output:  # Output filename
        filename = args.input.split('.')[0] + '_curv.txt'
    else:
        filename = args.output

    try:  # Data save
        np.savetxt(filename, data_to_save, fmt='%.6f', delimiter=' ')
    except OSError as e:
        print('Error while saving the data check the output filename if you have specified one.')
        print(e)
        return False

    if args.plot:  # Vector plot
        plot(x, y, k)


if __name__ == "__main__":
    main()
