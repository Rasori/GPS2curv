#!/usr/bin/python
# This project goal was to perform conversion from gps location data to curvature file needed in ChassisSim. The project
# was started when data logger on Tampere Formula Student -19 (TFS19) could not provide accurate acceleration data for
# ChassisSim software.
#
# Creator: Waltteri Koskinen
# v0.1 23.01.2020

import numpy as np
from matplotlib import pyplot as plt

INPUT = "Toijala.txt"
filename = 'Toijala_curv.TXT'

def gps2meter(long, lat):
    """
    Function takes long and lat coordinates and converts them to meters in cartesian coordinate system.
    First data point is threaded as an origo.

    :param long: Longitude coordinates
    :param lat: Latitude coordinates
    :return: x ,y coordinates in a lists as meters
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


def plot(x, y, k):
    plt.plot(x, y)
    plt.quiver(x, y, k[:, 0], k[:, 1], color='red')
    plt.grid('both')
    plt.show()

    return None


def main():
    long, lat = np.loadtxt(INPUT, delimiter='\t', unpack=True)
    x, y = gps2meter(long, lat)
    L, curvature, k = curvature_cal(x, y)

    data_to_save = np.array([curvature, L])
    data_to_save = data_to_save.T
    np.savetxt(filename, data_to_save, fmt='%.6f', delimiter=' ')
    plot(x, y, k)


main()
