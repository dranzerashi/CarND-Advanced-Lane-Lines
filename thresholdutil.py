import cv2
import numpy as np

def cvt_unint8(function):
    '''
    Decorator to convert result to np.uint8
    :param function:
    :return: wrapped function
    '''

    def wrapper(*args, **kwargs):
        res = function(*args, **kwargs)
        return np.uint8(res)

    return wrapper


@cvt_unint8
def scale_sobel(img):
    return (img*255)/np.max(img)


def binary_threshold(img, thresh=(0,255)):
    binary_output = np.zeros_like(img)
    binary_output[(img > thresh[0]) & (img <= thresh[1])] = 1
    return binary_output

def color_threshold(img, low=(0,0,0), high=(255,255,255)):
    c1_bin = binary_threshold(img[:, :, 0], thresh=(low[0], high[0]))
    c2_bin = binary_threshold(img[:, :, 1], thresh=(low[1], high[1]))
    c3_bin = binary_threshold(img[:, :, 2], thresh=(low[1], high[1]))
    binary_output = np.zeros_like(img[:,:,0])
    binary_output[(c1_bin==1) & (c2_bin==1) & (c3_bin==1)] = 1
    return binary_output

def abs_sobel_thresh(img, orient='x', sobel_kernel=3, thresh=(0, 255)):
    # Calculate directional gradient
    # Apply threshold
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    sx, sy = (1, 0) if orient == 'x' else (0, 1)
    sobel = cv2.Sobel(gray, cv2.CV_64F, sx, sy, ksize=sobel_kernel)
    abs_sobel = np.absolute(sobel)
    scaled_sobel = scale_sobel(abs_sobel)
    grad_binary = binary_threshold(scaled_sobel, thresh)
    return grad_binary


def mag_thresh(img, sobel_kernel=3, mag_thresh=(0, 255)):
    # Calculate gradient magnitude
    # Apply threshold
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    abs_sobel = np.sqrt(np.square(sobelx) + np.square(sobely))
    scaled_sobel = scale_sobel(abs_sobel)
    mag_binary = binary_threshold(scaled_sobel, mag_thresh)
    return mag_binary

@cvt_unint8
def dir_threshold(img, sobel_kernel=3, thresh=(0, np.pi/2)):
    # Calculate gradient direction
    # Apply threshold
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    abs_sobel_x = np.sqrt(np.square(sobelx))
    abs_sobel_y = np.sqrt(np.square(sobely))
    grad_dir = np.arctan2(abs_sobel_y, abs_sobel_x)
    dir_binary = binary_threshold(grad_dir, thresh)
    return dir_binary
