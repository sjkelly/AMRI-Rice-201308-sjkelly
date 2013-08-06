#!/usr/bin/python
"""
This program is a demonstration of ellipse fitting.

Trackbar controls threshold parameter.

Gray lines are contours.  Colored lines are fit ellipses.

Original C implementation by:  Denis Burenkov.
Python implementation by: Roman Stanchak, James Bowman

This originates from OpenCV examples and falls under the BSD license.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import os
import sys
import random
import cv
import json


def contour_iterator(contour):
    while contour:
        yield contour
        contour = contour.h_next()

class FitEllipse:

    def __init__(self, source_image, threshold_pos, path):
        self.source_image = source_image
        self.outPath = os.path.splitext(path)[0] + "_processed" + os.path.splitext(path)[1]
        self.outJSON = os.path.splitext(path)[0] + "_processed.json"
        cv.CreateTrackbar("Threshold", "Result", threshold_pos, 255, self.process_image)
        self.process_image(threshold_pos)

    def process_image(self, threshold_pos): 
        """
        This function finds contours, draws them and their approximation by ellipses.
        """
        stor = cv.CreateMemStorage()
        
        # Create the destination images
        image02 = cv.CloneImage(self.source_image)
        cv.Zero(image02)
        image04 = cv.CreateImage(cv.GetSize(self.source_image), cv.IPL_DEPTH_8U, 3)
        cv.Zero(image04)

        # Threshold the source image. This needful for cv.FindContours().
        cv.Threshold(self.source_image, image02, threshold_pos, 255, cv.CV_THRESH_BINARY)

        # Find all contours.
        cont = cv.FindContours(image02,
            stor,
            cv.CV_RETR_LIST,
            cv.CV_CHAIN_APPROX_NONE,
            (0, 0))

        ellipseList = []

        for idx, c in enumerate(contour_iterator(cont)):
            # Number of points must be more than or equal to 6 for cv.FitEllipse2
            if len(c) >= 6:
                # Copy the contour into an array of (x,y)s
                PointArray2D32f = cv.CreateMat(1, len(c), cv.CV_32FC2)
                for (i, (x, y)) in enumerate(c):
                    PointArray2D32f[0, i] = (x, y)
                
                # Draw the current contour in gray
                gray = cv.CV_RGB(100, 100, 100)
                cv.DrawContours(image04, c, gray, gray,0,1,8,(0,0))
                
                # Fits ellipse to current contour.
                (center, size, angle) = cv.FitEllipse2(PointArray2D32f)

                # Prevent OpenCV from making a big ellipse around everything
                if size[0] >= cv.GetSize(image04)[0] or size[1] >= cv.GetSize(image04)[1]:
                    continue

                ellipseData = {}
                ellipseData['number'] = str(idx)
                ellipseData['center'] = str(center)
                ellipseData['size'] = str(size)
                ellipseData['angle'] = str(angle)
                ellipseList.append(ellipseData)

                # Convert ellipse data from float to integer representation.
                center = (cv.Round(center[0]), cv.Round(center[1]))
                size = (cv.Round(size[0] * 0.5), cv.Round(size[1] * 0.5))
                angle = -angle

                color = cv.CV_RGB(255, 255, 255)
                cv.Ellipse(image04, center, size,
                          angle, 0, 360,
                          color, 1, cv.CV_AA, 0)
                font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, .4, .4, 0, 1, 8)
                cv.PutText(image04, str(idx), center, font, cv.RGB(250,0,0))

        # Show image. HighGUI use.
        cv.ShowImage( "Result", image04 )
        print(json.dumps(ellipseList, indent=2))
        f = open(self.outJSON, 'w')
        f.write(json.dumps(ellipseList, indent=2))
        f.close()
        cv.SaveImage(self.outPath, image04)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        path = os.path.abspath(sys.argv[1])
        source_image = cv.LoadImage(path, cv.CV_LOAD_IMAGE_GRAYSCALE)
    else:
        print("fitellipse.py [input image]")
        sys.exit(0)

    # Create windows.
    cv.NamedWindow("Source", cv.CV_WINDOW_NORMAL)
    cv.NamedWindow("Result", cv.CV_WINDOW_NORMAL)

    # Show the image.
    cv.ShowImage("Source", source_image)

    fe = FitEllipse(source_image, 70, path)

    print("Press any key to exit")
    cv.WaitKey(0)
    cv.DestroyWindow("Source")
    cv.DestroyWindow("Result")
