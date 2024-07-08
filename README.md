# Interactive Analysis of Mitochondrial Dispersal in Cells

## Background

Mitochondria are essential organelles in eukaryotic cells, involved in energy production, signaling, and apoptosis. Understanding their localization within cells can provide insights into cellular function and health. This project aims to develop an interactive tool that allows researchers to analyze mitochondrial dispersal by uploading images of cells and mitochondria. The tool will enable users to manually mark regions of interest and calculate the proportion of mitochondria in these regions.

## Project Description

This project involves the creation of an interactive program that allows users to upload cell images along with corresponding mitochondrial channel images. The program will provide a drawing tool for users to mark regions of interest (ROI) within the cell images. The marked regions will then be analyzed to calculate the number of pixels in the ROI and the proportion of pixels in the mitochondrial images.

> This project was originally implemented as part of the [Python programming course](https://github.com/szabgab/wis-python-course-2024-04)
> at the [Weizmann Institute of Science](https://www.weizmann.ac.il/) taught by [Gabor Szabo](https://szabgab.com/)


## Technical Implementation

1. **Image Upload and Display**

   - Use Tkinter for the GUI to allow users to upload cell and mitochondrial images.
   - Display the images in the application window.

2. **Marking Regions of Interest**

   - Implement drawing tools using OpenCV to enable users to mark regions on the cell images.
   - Store the coordinates of the marked regions for further analysis.
   - ![Example Marked cells](https://github.com/DahaiSun/Mitochondrial_dispersal_statistics/blob/main/user_instruction/mark_cell.png)

3. **Pixel Calculation**

   - Calculate the total number of pixels within the marked regions.
   - Analyze the corresponding mitochondrial image to count the number of green pixels in the marked regions. Threshold was set up by OSTU method

4. **Proportion Calculation**

   - Compute the proportion of green pixels to the total pixels in the marked area.
   - Display the result to the user using pop up excel window.

5. **Figure Drawing**

   - Plot the intensity histogram for each mark regions, and indicate the OSTU threshold with a dashed line

## Software Dependencies

- Python 3
- Tkinter
- OpenCV
- NumPy
- Matplotlib
- Pillow
- Pandas

## User Guidance

### Installation

1. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2. **Running the Program:**

    ```bash
    python Mito_dispersal.py
    ```

3. **Run Tests:**

    ```bash
    python test_Mito_Dispersal.py
    ```

### Using the Software

1. **Launch the Application:**

    Run the program using the command provided above. The application window will open with options to upload images and mark regions of interest.

2. **Upload Images:**

    - Click the "Upload Cell Image" button to select and load a cell image.
    - Click the "Upload Mitochondrial Image" button to select and load a mitochondrial image.

3. **Mark Regions of Interest:**

    - Click the "Mark Cell" button to begin marking regions of interest on the cell image. Left click and hold to draw. Mutipule marks can be draw on the same image, each one label with a number
    - To delete marked regions, click the "Delete Mark" button.

4. **Calculate Mitochondrial Dispersal:**

    - After marking the regions, click the "Calculate" button to analyze the images. The results, including the proportion of mitochondria in each marked region, will be displayed in the GUI window.

    - The results will also be saved to an Excel file named `MitoDispersalResults.xlsx` and opened automatically.

5. **View Histograms:**

    - A histogram showing the distribution of mitochondrial pixels within each marked region will be displayed in a separate window.

## Note

Ensure that both the cell and mitochondrial images are properly loaded and regions of interest are marked before performing the calculation. If any issues arise, appropriate error messages will be displayed.


