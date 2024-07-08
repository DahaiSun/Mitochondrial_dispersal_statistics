# test_Mito_dispersal.py
import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
import cv2
import numpy as np
from Mito_dispersal import MitoDispersalAnalyzer

class TestMitoDispersalAnalyzer(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.app = MitoDispersalAnalyzer(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_ui_initialization(self):
        self.assertEqual(self.app.master.title(), "Mitochondrial Dispersal Analyzer")
        self.root.update_idletasks()
        expected_width = self.app.fixed_width * 2 + 40
        expected_height = self.app.fixed_height + 250
        actual_geometry = self.app.master.geometry().split('+')[0]
        actual_width, actual_height = map(int, actual_geometry.split('x'))
        self.assertEqual(actual_width, expected_width)
        self.assertTrue(abs(actual_height - expected_height) <= 10)
        print("test_ui_initialization passed")

    @patch('Mito_dispersal.filedialog.askopenfilename')
    @patch('Mito_dispersal.cv2.imread', return_value=np.zeros((800, 1200, 3), dtype=np.uint8))
    def test_upload_cell_image(self, mock_imread, mock_askopenfilename):
        mock_askopenfilename.return_value = "cell_image.png"
        self.app.upload_cell_image()
        self.assertIsNotNone(self.app.cell_img)
        self.assertIsNotNone(self.app.cell_mask)
        print("test_upload_cell_image passed")

    @patch('Mito_dispersal.filedialog.askopenfilename')
    @patch('Mito_dispersal.cv2.imread', return_value=np.zeros((800, 1200, 3), dtype=np.uint8))
    def test_upload_mito_image(self, mock_imread, mock_askopenfilename):
        mock_askopenfilename.return_value = "mito_image.png"
        self.app.upload_mito_image()
        self.assertIsNotNone(self.app.mito_img)
        self.assertIsNotNone(self.app.mito_mask)
        print("test_upload_mito_image passed")

    def test_create_placeholder_image(self):
        placeholder = self.app.create_placeholder_image(self.app.fixed_width, self.app.fixed_height)
        self.assertEqual(placeholder.shape, (self.app.fixed_height, self.app.fixed_width, 3))
        print("test_create_placeholder_image passed")

    def test_resize_image(self):
        img = np.zeros((800, 1200, 3), dtype=np.uint8)
        resized_img = self.app.resize_image(img, self.app.fixed_width, self.app.fixed_height)
        self.assertEqual(resized_img.shape[1], self.app.fixed_width)
        self.assertTrue(resized_img.shape[0] <= self.app.fixed_height)
        print("test_resize_image passed")


    def test_calculate_no_images(self):
        with patch('Mito_dispersal.messagebox.showerror') as mock_showerror:
            self.app.calculate()
            mock_showerror.assert_called_once_with("Error", "Please upload both cell and mitochondrial images.")
        print("test_calculate_no_images passed")

    def test_calculate_no_rois(self):
        self.app.cell_img = np.zeros((self.app.fixed_height, self.app.fixed_width, 3), dtype=np.uint8)
        self.app.mito_img = np.zeros((self.app.fixed_height, self.app.fixed_width, 3), dtype=np.uint8)
        with patch('Mito_dispersal.messagebox.showerror') as mock_showerror:
            self.app.calculate()
            mock_showerror.assert_called_once_with("Error", "No ROI marked.")
        print("test_calculate_no_rois passed")

    def test_mark_cell(self):
        self.app.cell_img = np.zeros((self.app.fixed_height, self.app.fixed_width, 3), dtype=np.uint8)
        self.app.mark_cell()
        self.assertIsNotNone(self.app.cell_label.bind("<Button-1>", self.app.start_drawing))
        print("test_mark_cell passed")

if __name__ == '__main__':
    unittest.main()
