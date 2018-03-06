import cv2
import numpy as np
class PerspectiveTransform:
    def __init__(self, src, dst):
        '''
        :param src: Source Coordinates for perspective transform
        :param dst: Destination Coordinates for perspective transform
        '''
        src = np.float32(src)
        dst = np.float32(dst)
        self.M = cv2.getPerspectiveTransform(src, dst)
        self.Minv = cv2.getPerspectiveTransform(dst, src)

    def transform(self, img):
        '''
        Function to transform the perspective
        :param img:
        :return:
        '''
        return cv2.warpPerspective(img, self.M, (img.shape[1], img.shape[0]), flags=cv2.INTER_LINEAR)

    def inverse_transform(self, img):
        '''
        Function to return the inverse of the perspective transformation
        :param img:
        :return:
        '''
        return cv2.warpPerspective(img, self.Minv, (img.shape[1],img.shape[0]),flags=cv2.INTER_LINEAR)