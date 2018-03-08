import cv2
import numpy as np

class Calibrate:
    def __init__(self, images, nx, ny):
        '''
        :param images: list of file paths to images
        :param nx: number of inside corners along x
        :param ny: number of inside corners along y
        '''
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((ny * nx, 3), np.float32)
        objp[:, :2] = np.mgrid[0:nx, 0:ny].T.reshape(-1, 2)

        # Arrays to store object points and image points from all the images.
        obj_points = []  # 3d points in real world space
        img_points = []  # 2d points in image plane.

        for fname in images:
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Find the chessboard corners
            ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)

            # If found, add object points, image points
            if ret:
                obj_points.append(objp)
                img_points.append(corners)

        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)
        self.ret = ret
        self.mtx = mtx
        self.dist = dist
        self.rvecs = rvecs
        self.tvecs = tvecs

    def undistort(self, img):
        '''
        Undistort the image
        :param img: image to undistort
        :return: undistorted image
        '''
        return cv2.undistort(img, self.mtx, self.dist, None, self.mtx)

