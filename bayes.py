import sys # OS Commands
import random # generate pseudorandom numbers
import itertools # helps with looping
import numpy as np
import cv2 as cv

# these are constants, which is why they're in ALL CAPS

MAP_FILE = 'cape_python.png'

SA1_CORNERS = (130, 265, 180, 315) # (UL-X, UL-Y, LR-X, LR-Y)
SA2_CORNERS = (80, 255, 130, 305) # (UL-X, UL-Y, LR-X, LR-Y)
SA3_CORNERS = (105, 205, 155, 255) # (UL-X, UL-Y, LR-X, LR-Y)

# classes start with a Capital Letter
# defining the Seach class
class Search():
    """Bayesian Search & Rescue Game with 3 search areas."""

    def __init__(self, name):
        # initial values
        self.name = name
        self.img = cv.imread(MAP_FILE, cv.IMREAD_COLOR)
        if self.img is None:
            print('Could not load map file {}'.format(MAP_FILE), file= sys.stderr)
            sys.exit(1)

        # attributes for sailors actual location when found
        self.area_actual = 0
        self.sailor_actual = [0,0] # as "local" coords within search area; currently a placeholder

        # create a sub-array within the map array
        self.sa1 = self.img[SA1_CORNERS[1] : SA1_CORNERS[3], SA1_CORNERS[0] : SA1_CORNERS[2]]
        self.sa2 = self.img[SA2_CORNERS[1] : SA2_CORNERS[3], SA2_CORNERS[0] : SA2_CORNERS[2]]
        self.sa3 = self.img[SA3_CORNERS[1] : SA3_CORNERS[3], SA3_CORNERS[0] : SA3_CORNERS[2]]

        # pre-search probabilities and SEP (Search Effectiveness Probability)
        self.p1 = 0.2
        self.p2 = 0.5
        self.p3 = 0.3

        self.sep1 = 0
        self.sep2 = 0
        self.sep3 = 0

    # drawing the map
    def draw_map(self, last_known):
        """Display basemap with scale, last known xy location, search areas"""
        cv.line(self.img, (20,370), (70,370), (0,0,0), 2)
        cv.putText(self.img, '0', (8,370), cv.FONT_HERSHEY_PLAIN, 1, (0,0,0))
        cv.putText(self.img, '50 Nautical Miles', (71,370), cv.FONT_HERSHEY_PLAIN, 1, (0,0,0))

        # drawing the search areas
        # search area 1
        cv.rectangle(self.img, (SA1_CORNERS[0], SA1_CORNERS[1], SA1_CORNERS[3], SA1_CORNERS[4]), (0,0,0), 1)
        cv.putText(self.img, '1', (SA1_CORNERS[0]+3, SA1_CORNERS[1]+15), cv.FONT_HERSHEY_PLAIN, 1, 0)

        # search area 2
        cv.rectangle(self.img, (SA2_CORNERS[0], SA2_CORNERS[1], SA2_CORNERS[3], SA2_CORNERS[4]), (0,0,0), 1)
        cv.putText(self.img, '2', (SA2_CORNERS[0]+3, SA2_CORNERS[1]+15), cv.FONT_HERSHEY_PLAIN, 1, 0)

        # search area 3
        cv.rectangle(self.img, (SA3_CORNERS[0], SA3_CORNERS[1], SA3_CORNERS[3], SA3_CORNERS[4]), (0,0,0), 1)
        cv.putText(self.img, '3', (SA3_CORNERS[0]+3, SA3_CORNERS[1]+15), cv.FONT_HERSHEY_PLAIN, 1, 0)

        # sailor's last known position
        cv.putText(self.img, '+', (last_known), cv.FONT_HERSHEY_PLAIN, 1, (0,0,255))
        cv.putText(self.img, '+ = Last Known Position', (274, 355), cv.FONT_HERSHEY_PLAIN, 1, (0,0,255))
        cv.putText(self.img, '* = Actual Position', (275, 370), cv.FONT_HERSHEY_PLAIN, 1, (255,0,0))

        # showing the basemap in upper right of monitor
        cv.imshow('Search Area', self.img)
        cv.moveWindow('Search Area', 750, 10)
        cv.waitKey(500)

    def sailor_final_location(self, num_search_areas):
        """Return the actual x,y location of the missing sailor"""
        # Find sailor coordinates with respect to any Search Area subarray
        self.sailor_actual[0] = np.random.choice(self.sa1.shape[1], 1)
        self.sailor_actual[1] = np.random.choice(self.sa1.shape[0], 1)

        # pick a search area
        area = int(random.triangular(1, num_search_areas+1))

        if area == 1:
            x = self.sailor_actual[0] + SA1_CORNERS[0]
            y = self.sailor_actual[1] + SA1_CORNERS[1]
            self.area_actual = 1
        elif area == 2:
            x = self.sailor_actual[0] + SA2_CORNERS[0]
            y = self.sailor_actual[1] + SA2_CORNERS[1]
            self.area_actual = 2
        elif area == 3:
            x = self.sailor_actual[0] + SA3_CORNERS[0]
            y = self.sailor_actual[1] + SA3_CORNERS[1]
            self.area_actual = 3
        return x, y