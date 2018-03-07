import numpy as np


class Curve:
    def __init__(self):
        # was the line detected in the last iteration?
        self.detected = False
        # x values of the last n fits of the line
        self.recent_xfitted = []
        # average x values of the fitted line over the last n iterations
        self.bestx = None
        # polynomial coefficients averaged over the last n iterations
        self.best_fit = None
        # polynomial coefficients for the most recent fit
        self.current_fit = [np.array([False])]
        # radius of curvature of the line in some units
        self.radius_of_curvature = None
        # distance in meters of vehicle center from the curve
        self.curve_base_pos = None
        # difference in fit coefficients between last and new fits
        self.diffs = np.array([0, 0, 0], dtype='float')
        # x values for detected line pixels
        self.allx = None
        # y values for detected line pixels
        self.ally = None
        # meters per pixel in y dimension
        self.ym_per_pix = 30/720
        # meters per pixel in x dimension
        self.xm_per_pix = 3.7/700

    def get_fit(self, ploty):
        return self.current_fit[0]*ploty**2 + self.current_fit[1]*ploty + self.current_fit[2]

    def update_best_fit(self):
        #TODO calculate best fit and bestx
        pass

    def update_radius_of_curvature(self):
        #TODO update radius of curvature
        y_eval = np.max(self.ally)
        fit_cr = np.polyfit(self.ally * self.ym_per_pix,  self.allx * self.xm_per_pix, 2)
        self.radius_of_curvature = ((1 + (2 * fit_cr[0] * y_eval * self.ym_per_pix + fit_cr[1]) ** 2) ** 1.5) / np.absolute(2 * fit_cr[0])


    def update_curve_base_pos(self):
        #TODO update curve_base_pos
        pass

    def set_current_fit(self, current_fit, allx, ally):
        if self.detected:
            self.recent_xfitted.append(self.current_fit)
        self.update_best_fit()  # TODO Avg out the xfits

        self.current_fit = current_fit
        self.detected = (current_fit is not None)
        self.allx = allx
        self.ally = ally
        #TODO update the rest from the best fit
        if self.detected:
            self.update_radius_of_curvature()
            self.update_curve_base_pos()
