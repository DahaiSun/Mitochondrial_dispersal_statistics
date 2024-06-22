# Interactive Analysis of Mitochondrial Dispersal in Cells

## Background

Mitochondria are essential organelles in eukaryotic cells, involved in energy production, signaling, and apoptosis. Understanding their localization within cells can provide insights into cellular function and health. This project aims to develop an interactive tool that allows researchers to analyze mitochondrial dispersal by uploading images of cells and mitochondria. The tool will enable users to manually mark regions of interest and calculate the proportion of mitochondria in these regions.

## Project Description

This project involves the creation of an interactive program that allows users to upload cell images along with corresponding mitochondrial channel images. The program will provide a drawing tool for users to mark regions of interest (ROI) within the cell images. The marked regions will then be analyzed to calculate the number of pixels in the ROI and the proportion of pixels in the mitochondrial images.

> This project was originally implemented as part of the [Python programming course](https://github.com/szabgab/wis-python-course-2024-04)
> at the [Weizmann Institute of Science](https://www.weizmann.ac.il/) taught by [Gabor Szabo](https://szabgab.com/)


## Technical Implementation

1. Image Upload and Display

Use Tkinter for the GUI to allow users to upload cell and mitochondrial images.
Display the images in the application window.

2. Marking Regions of Interest

Implement drawing tools using OpenCV to enable users to mark regions on the cell images.
Store the coordinates of the marked regions for further analysis.

3. Pixel Calculation

Calculate the total number of pixels within the marked regions.
Analyze the corresponding mitochondrial image to count the number of green pixels in the marked regions.

4. Proportion Calculation

Compute the proportion of green pixels to the total pixels in the marked area.
Display the result to the user.

5. Figure drawing
Draw a figure that highlights the marked region on the cell image.
Overlay the mitochondrial image to show the green pixels within the marked region.
Use Matplotlib to generate and display the figure.

## Software Dependencies
Python 3
Tkinter
OpenCV
NumPy
Matplotlib

## User Guidance

Install Dependencies:
```bash
pip install -r requirements.txt

Running the program:
```bash
python3 Mito_dispersal.py

Run Test:
```bash
pytest


