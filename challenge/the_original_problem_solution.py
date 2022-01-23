Carnegie Mellon University
assessmentGradebook
clear_allJobs
Jaissruti Nanthakumararrow_drop_down
Jaissruti Nanthakumar
account_circleAccount
assignment_indCourse Profile
exit_to_appLog out
assessmentGradebook
clear_allJobs
home ITCS-5152-Fall-2021 (Fall 2021) The Original Problem Annotate Submission
Submission Version 5 for The Original Problem (jnanthak@uncc.edu)
Summary
Nothing to summarize yet.


jnanthak@uncc.edu_5_handin.py
COLLAPSE ALL EXPAND ALL
import numpy as np
from math import exp

def filter_2d(im, kernel):
    '''
    Filter an image by taking the dot product of each 
    image neighborhood with the kernel matrix.
    Args:
    im = (H x W) grayscale floating point image
    kernel = (M x N) matrix, smaller than im
    Returns: 
    (H-M+1 x W-N+1) filtered image.
    '''

    M = kernel.shape[0] 
    N = kernel.shape[1]
    H = im.shape[0]
    W = im.shape[1]
    
    filtered_image = np.zeros((H-M+1, W-N+1), dtype = 'float64')
    
    for i in range(filtered_image.shape[0]):
        for j in range(filtered_image.shape[1]):
            image_patch = im[i:i+M, j:j+N]
            filtered_image[i, j] = np.sum(np.multiply(image_patch, kernel))
            
    return filtered_image

def convert_to_grayscale(im):
    '''
    Convert color image to grayscale.
    Args: im = (nxmx3) floating point color image scaled between 0 and 1
    Returns: (nxm) floating point grayscale image scaled between 0 and 1
    '''
    return np.mean(im, axis = 2)



def classify(im):
    im = im[10:245,10:245]
    G = convert_to_grayscale(im/255)
    U = np.array([[1, 0, -1],
                [2, 0, -2],
                [1, 0, -1]])
    V = np.array([[1, 2, 1],
                [0, 0, 0],
                [-1, -2, -1]])
    Gx = filter_2d(G, U)
    Gy = filter_2d(G, V)
    Gmag = np.sqrt(Gx**2+Gy**2)
    Gdir = np.arctan2(Gy, Gx)

    edgeav = Gdir[Gmag > 0.95]
    
    z = np.histogram(edgeav, bins = 50)
    std_dev = np.std(z[0])
    if std_dev < 8.8:
        return 'ball'
    elif std_dev > 8.81 and std_dev < 16.75:
       return 'cylinder'
    else:
       return 'brick'
Autolab Project · Contact · GitHub · Facebook · Logoutv2.2.1