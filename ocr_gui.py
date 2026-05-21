import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import pytesseract
from PIL import Image, ImageTk
import os

class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart OCR System")
        self.root.geometry("800x600")

        self.image_path = None
        self.extracted_text = ""

        # Title
        tk.Label(root, text="OCR Image to Text System", font=("Arial", 18, "bold")).pack(pady=10)

        # Buttons
        tk.Button(root, text="Upload Image", command=self.upload_image, width=20).pack(pady=5)
        tk.Button(root, text="Extract Text", command=self.extract_text, width=20).pack(pady=5)
        tk.Button(root, text="Save as TXT", command=self.save_text, width=20).pack(pady=5)

        # Image display
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        # Text box
        self.text_box = tk.Text(root, height=15, width=90)
        self.text_box.pack(pady=10)

    # Upload image
    def upload_image(self):
        self.image_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )

        if self.image_path:
            img = Image.open(self.image_path)
            img = img.resize((300, 300))
            img = ImageTk.PhotoImage(img)

            self.image_label.configure(image=img)
            self.image_label.image = img

            messagebox.showinfo("Success", "Image Loaded Successfully")

    # OCR processing
    def extract_text(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please upload an image first")
            return

        img = cv2.imread(self.image_path)

        # Preprocessing
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # OCR
        self.extracted_text = pytesseract.image_to_string(gray)

        # Show in textbox
        self.text_box.delete("1.0", tk.END)
        self.text_box.insert(tk.END, self.extracted_text)

        messagebox.showinfo("Done", "Text Extracted Successfully")

    # Save output
    def save_text(self):
        if not self.extracted_text:
            messagebox.showerror("Error", "No text to save")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text File", "*.txt")]
        )

        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.extracted_text)

            messagebox.showinfo("Saved", "File Saved Successfully")


# Run app
root = tk.Tk()
app = OCRApp(root)
root.mainloop()
