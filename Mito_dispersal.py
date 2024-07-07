import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import subprocess
import os

class MitoDispersalAnalyzer:
    def __init__(self, master):
        self.master = master
        self.master.title("Mitochondrial Dispersal Analyzer")

        self.fixed_width = 600
        self.fixed_height = 600

        self.master.geometry(f"{self.fixed_width * 2 + 40}x{self.fixed_height + 250}")

        self.cell_img = None
        self.mito_img = None
        self.cell_mask = None
        self.mito_mask = None
        self.drawing = False
        self.roi_coords = []  # List of lists to store multiple ROIs

        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style(self.master)
        style.theme_use('clam')  # Use the 'clam' theme for a cleaner look

        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.placeholder_img = self.create_placeholder_image(self.fixed_width, self.fixed_height)

        img_frame = ttk.Frame(main_frame)
        img_frame.grid(row=0, column=0, columnspan=2, pady=10)

        self.cell_label = ttk.Label(img_frame)
        self.cell_label.grid(row=0, column=0, padx=10, pady=10)
        self.display_image(self.placeholder_img, self.cell_label, is_placeholder=True)

        self.mito_label = ttk.Label(img_frame)
        self.mito_label.grid(row=0, column=1, padx=10, pady=10)
        self.display_image(self.placeholder_img, self.mito_label, is_placeholder=True)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        self.upload_cell_btn = ttk.Button(button_frame, text="Upload Cell Image", command=self.upload_cell_image)
        self.upload_cell_btn.grid(row=0, column=0, padx=10, pady=5)

        self.upload_mito_btn = ttk.Button(button_frame, text="Upload Mitochondrial Image", command=self.upload_mito_image)
        self.upload_mito_btn.grid(row=0, column=1, padx=10, pady=5)

        self.mark_cell_btn = ttk.Button(button_frame, text="Mark Cell", command=self.mark_cell)
        self.mark_cell_btn.grid(row=1, column=0, padx=10, pady=5)

        self.delete_btn = ttk.Button(button_frame, text="Delete Mark", command=self.delete_mark)
        self.delete_btn.grid(row=1, column=1, padx=10, pady=5)

        self.calculate_btn = ttk.Button(button_frame, text="Calculate", command=self.calculate)
        self.calculate_btn.grid(row=2, column=0, columnspan=2, pady=5)

        self.result_label = ttk.Label(main_frame, text="Proportion of Mitochondria in Cell: ")
        self.result_label.grid(row=2, column=0, columnspan=2, pady=10)

        for widget in button_frame.winfo_children():
            widget.bind("<Enter>", self.on_enter)
            widget.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        event.widget['background'] = 'lightblue'

    def on_leave(self, event):
        event.widget['background'] = 'SystemButtonFace'

    def create_placeholder_image(self, width, height):
        img = np.zeros((height, width, 3), dtype=np.uint8)
        cv2.putText(img, 'No Image', (width // 4, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        return img

    def resize_image(self, img, width, height):
        scale = min(width / img.shape[1], height / img.shape[0])
        return cv2.resize(img, (int(img.shape[1] * scale), int(img.shape[0] * scale)), interpolation=cv2.INTER_AREA)

    def upload_cell_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.cell_img = self.resize_image(cv2.imread(file_path), self.fixed_width, self.fixed_height)
            self.display_image(self.cell_img, self.cell_label)
            self.cell_mask = np.zeros(self.cell_img.shape[:2], dtype=np.uint8)
            self.roi_coords = []

    def upload_mito_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.mito_img = self.resize_image(cv2.imread(file_path), self.fixed_width, self.fixed_height)
            self.display_image(self.mito_img, self.mito_label)
            self.mito_mask = np.zeros(self.mito_img.shape[:2], dtype=np.uint8)

    def display_image(self, img, label, is_placeholder=False):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)
        label.imgtk = img_tk
        label.configure(image=img_tk)
        if is_placeholder:
            label.image = img_tk  # Keep a reference to avoid garbage collection

    def mark_cell(self):
        if self.cell_img is None:
            messagebox.showerror("Error", "Please upload a cell image first.")
            return

        self.drawing = False
        self.cell_label.bind("<Button-1>", self.start_drawing)
        self.cell_label.bind("<B1-Motion>", self.draw)
        self.cell_label.bind("<ButtonRelease-1>", self.stop_drawing)
        self.cell_label.bind("<Double-Button-1>", self.finish_drawing)

    def start_drawing(self, event):
        self.drawing = True
        self.roi_coords.append([])  # Start a new ROI
        self.roi_coords[-1].append((event.x, event.y))
        self.update_drawing()

    def draw(self, event):
        if self.drawing:
            self.roi_coords[-1].append((event.x, event.y))
            self.update_drawing()

    def stop_drawing(self, event):
        self.drawing = False

    def finish_drawing(self, event):
        self.update_drawing(finalize=True)

    def update_drawing(self, finalize=False):
        if self.cell_img is not None:
            img = self.cell_img.copy()
            for i, roi in enumerate(self.roi_coords):
                if len(roi) > 1:
                    cv2.polylines(img, [np.array(roi)], isClosed=True, color=(0, 255, 0), thickness=2)
                    if finalize:
                        cv2.fillPoly(self.cell_mask, [np.array(roi)], color=255)
                    # Draw the label number in red
                    cv2.putText(img, f"{i+1}", roi[0], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            self.display_image(img, self.cell_label)

        if self.mito_img is not None:
            img = self.mito_img.copy()
            for i, roi in enumerate(self.roi_coords):
                if len(roi) > 1:
                    cv2.polylines(img, [np.array(roi)], isClosed=True, color=(0, 255, 0), thickness=2)
                    if finalize:
                        cv2.fillPoly(self.mito_mask, [np.array(roi)], color=255)
                    # Draw the label number in red
                    cv2.putText(img, f"{i+1}", roi[0], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            self.display_image(img, self.mito_label)

    def delete_mark(self):
        if self.cell_img is not None:
            self.cell_mask.fill(0)
            self.roi_coords = []
            self.display_image(self.cell_img, self.cell_label)
        if self.mito_img is not None:
            self.display_image(self.mito_img, self.mito_label)

    def calculate(self):
        if self.cell_img is None or self.mito_img is None:
            messagebox.showerror("Error", "Please upload both cell and mitochondrial images.")
            return

        if not self.roi_coords:
            messagebox.showerror("Error", "No ROI marked.")
            return

        data = {
            "ROI Number": [],
            "Marked Area Pixels": [],
            "Mitochondrial Green Area Pixels": [],
            "Mitochondrial Dispersal Ratio": []
        }

        roi_mito_list = []

        # Process each ROI independently
        for i, roi in enumerate(self.roi_coords):
            roi_mask = np.zeros(self.cell_img.shape[:2], dtype=np.uint8)
            cv2.fillPoly(roi_mask, [np.array(roi)], color=255)
            
            # Apply ROI mask to mitochondrial image
            green_channel = self.mito_img[:, :, 1]
            roi_mito = cv2.bitwise_and(green_channel, green_channel, mask=roi_mask)
            roi_mito_list.append(roi_mito)

            # Apply Otsu's thresholding within ROI
            _, mito_thresh = cv2.threshold(roi_mito, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Calculate the area with green signal within ROI
            mito_green_area = np.sum((mito_thresh > 0) & (roi_mask > 0))
            marked_area = np.sum(roi_mask > 0)
            dispersal_ratio = mito_green_area / marked_area if marked_area > 0 else 0

            data["ROI Number"].append(i + 1)
            data["Marked Area Pixels"].append(marked_area)
            data["Mitochondrial Green Area Pixels"].append(mito_green_area)
            data["Mitochondrial Dispersal Ratio"].append(dispersal_ratio)

        df = pd.DataFrame(data)

        # Save to Excel
        output_file = "MitoDispersalResults.xlsx"
        df.to_excel(output_file, index=False)

        # Open Excel file
        try:
            if os.name == 'nt':  # For Windows
                os.startfile(output_file)
            else:  # For macOS and Linux
                subprocess.call(['open', output_file] if os.name == 'darwin' else ['xdg-open', output_file])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open Excel file: {e}")

        result_text = df.to_string(index=False)
        self.result_label.config(text=result_text)

        # Display histogram figure of the Otsu thresholding
        self.show_histogram(roi_mito_list)

    def show_histogram(self, roi_mito_list):
        # Create a new window for the histogram
        hist_window = tk.Toplevel(self.master)
        hist_window.title("Histogram of Mitochondrial Image within ROIs")

        num_rois = len(roi_mito_list)
        cols = 2  # Number of columns (reduced to make the width of each subplot larger)
        rows = (num_rois + cols - 1) // cols  # Calculate the number of rows needed

        fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows))  # Increased width from 20 to 15 per row
        axes = axes.flatten()

        for i, (roi_mito, ax) in enumerate(zip(roi_mito_list, axes)):
            ax.hist(roi_mito.ravel(), bins=256, range=[0, 256], color='green', alpha=0.75)
            ax.set_yscale('log', base=2)  # Set y-axis to log2 scale
            ax.set_title(f'ROI {i+1}')
            ax.set_xlabel('Pixel Intensity')
            ax.set_ylabel('Frequency')
            
            # Calculate Otsu's threshold
            otsu_thresh, _ = cv2.threshold(roi_mito, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Plot the Otsu threshold
            ax.axvline(x=otsu_thresh, color='red', linestyle='dashed', linewidth=1, label=f'Otsu Threshold: {otsu_thresh:.2f}')
            ax.legend(loc='upper right')

        # Hide any unused subplots
        for ax in axes[num_rois:]:
            ax.axis('off')

        # Save the figure to a canvas
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=hist_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        plt.close(fig)  # Close the plot to avoid duplication in the next call


if __name__ == "__main__":
    root = tk.Tk()
    app = MitoDispersalAnalyzer(root)
    root.mainloop()
