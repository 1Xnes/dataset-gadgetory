import os
import shutil
import yaml
from tkinter import Tk, Button, filedialog, messagebox


#This code separates the photos of each class of the dataset into separate folders.

class ImageCopier:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Copier")
        self.dataset_folder = None
        self.yaml_file_path = None
        self.classes = None
        self.destination_folder = None

        self.btn_browse_dataset = Button(root, text="Browse Dataset", command=self.browse_dataset)
        self.btn_browse_dataset.pack()

        self.btn_browse_destination = Button(root, text="Browse Destination", command=self.browse_destination)
        self.btn_browse_destination.pack()

        self.btn_copy_images = Button(root, text="Copy Images", command=self.copy_images)
        self.btn_copy_images.pack()

    def browse_dataset(self):
        self.dataset_folder = filedialog.askdirectory(title="Select YOLOv5 Dataset Folder")
        self.yaml_file_path = os.path.join(self.dataset_folder, "data.yaml")

        if os.path.exists(self.yaml_file_path):
            with open(self.yaml_file_path, 'r') as yaml_file:
                yaml_data = yaml.safe_load(yaml_file)
                if isinstance(yaml_data['names'], dict):
                    self.classes = {int(key): value for key, value in yaml_data['names'].items()}
                elif isinstance(yaml_data['names'], list):
                    self.classes = {int(key): value for key, value in enumerate(yaml_data['names'])}

    def browse_destination(self):
        self.destination_folder = filedialog.askdirectory(title="Select Destination Folder")

    def copy_images(self):
        if self.dataset_folder is not None and os.path.exists(self.yaml_file_path) and self.destination_folder is not None:
            images_folder = os.path.join(self.dataset_folder, "images")
            labels_folder = os.path.join(self.dataset_folder, "labels")

            for label_set in ["train", "val"]:
                label_folder = os.path.join(labels_folder, label_set)
                image_folder = os.path.join(images_folder, label_set)

                for label_file in os.listdir(label_folder):
                    with open(os.path.join(label_folder, label_file), 'r') as label_file_content:
                        lines = label_file_content.readlines()
                        for line in lines:
                            class_index = int(line.split()[0])
                            class_name = self.classes.get(class_index)

                            if class_name is not None:
                                source_image_path = os.path.join(image_folder, f"{label_file.replace('.txt', '.jpg')}")
                                destination_folder = os.path.join(self.destination_folder, class_name)

                                if not os.path.exists(destination_folder):
                                    os.makedirs(destination_folder)

                                destination_image_path = os.path.join(destination_folder, f"{label_file.replace('.txt', '.jpg')}")

                                shutil.copy(source_image_path, destination_image_path)

            messagebox.showinfo("Success", "Images copied successfully.")
        else:
            messagebox.showerror("Error", "Dataset folder, YAML file, or destination folder not selected.")


if __name__ == "__main__":
    root = Tk()
    app = ImageCopier(root)
    root.geometry("400x250")  # You can change the GUI size
    root.mainloop()
