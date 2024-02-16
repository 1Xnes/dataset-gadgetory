import os
import yaml
from tkinter import Tk, Label, Button, filedialog, Toplevel, Frame
from tkinter.ttk import Notebook


#this code shows some dataset information like index numbers,count of label and photos


class YOLOv5DatasetAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("YOLOv5 Dataset Analyzer")
        self.dataset_folder = None
        self.yaml_file_path = None
        self.classes = None
        self.images_folder = None
        self.labels_folder = None
        self.class_counts_train = None
        self.class_counts_val = None
        self.class_occurrences = None

        self.label_info = Label(root, text="")
        self.label_info.pack()

        self.btn_browse = Button(root, text="Browse Dataset", command=self.browse_dataset)
        self.btn_browse.pack()

        self.btn_analyze = Button(root, text="Analyze Dataset", command=self.analyze_dataset)
        self.btn_analyze.pack()

    def browse_dataset(self):
        self.dataset_folder = filedialog.askdirectory(title="Select YOLOv5 Dataset Folder")
        self.yaml_file_path = os.path.join(self.dataset_folder, "data.yaml")

    def analyze_dataset(self):
        if self.dataset_folder is not None and os.path.exists(self.yaml_file_path):
            with open(self.yaml_file_path, 'r') as yaml_file:
                yaml_data = yaml.safe_load(yaml_file)
                self.classes = [yaml_data['names'][i] for i in range(len(yaml_data['names']))]
                self.images_folder = os.path.join(self.dataset_folder, "images")
                self.labels_folder = os.path.join(self.dataset_folder, "labels")

            self.class_counts_train = {cls: 0 for cls in self.classes}
            self.class_counts_val = {cls: 0 for cls in self.classes}
            self.class_occurrences = {cls: 0 for cls in self.classes}

            num_images_train = len(os.listdir(os.path.join(self.images_folder, "train")))
            num_labels_train = len(os.listdir(os.path.join(self.labels_folder, "train")))

            num_images_val = len(os.listdir(os.path.join(self.images_folder, "val")))
            num_labels_val = len(os.listdir(os.path.join(self.labels_folder, "val")))

            for label_file in os.listdir(os.path.join(self.labels_folder, "train")):
                with open(os.path.join(self.labels_folder, "train", label_file), 'r') as label_file_content:
                    lines = label_file_content.readlines()
                    for line in lines:
                        class_index = int(line.split()[0])
                        class_name = self.classes[class_index]
                        self.class_counts_train[class_name] += 1
                        self.class_occurrences[class_name] += 1

            for label_file in os.listdir(os.path.join(self.labels_folder, "val")):
                with open(os.path.join(self.labels_folder, "val", label_file), 'r') as label_file_content:
                    lines = label_file_content.readlines()
                    for line in lines:
                        class_index = int(line.split()[0])
                        class_name = self.classes[class_index]
                        self.class_counts_val[class_name] += 1
                        self.class_occurrences[class_name] += 1

            self.create_results_window(num_images_train, num_labels_train, num_images_val, num_labels_val)

        else:
            self.label_info.config(text="Dataset folder or YAML file not selected.")

    def generate_class_counts_text(self, class_counts):
        text = "\nClass Counts:\n"
        for cls, count in class_counts.items():
            text += f"{cls}: {count}\n"
        return text

    def generate_class_occurrences_text(self, class_occurrences):
        text = "\nClass Occurrences:\n"
        for cls, occurrences in class_occurrences.items():
            text += f"{cls}: {occurrences}\n"
        return text

    def create_results_window(self, num_images_train, num_labels_train, num_images_val, num_labels_val):
        results_window = Toplevel(self.root)
        results_window.title("Results")

        notebook = Notebook(results_window)

        # Index Page
        index_page = self.create_index_page(notebook, "Index Page")

        # Train Set Page
        train_page = self.create_page(notebook, "Train Set", num_images_train, num_labels_train, self.class_counts_train)

        # Val Set Page
        val_page = self.create_page(notebook, "Val Set", num_images_val, num_labels_val, self.class_counts_val)

        # Occurrences Page
        occurrences_page = self.create_occurrences_page(notebook, "Occurrences Page", self.class_occurrences)

        notebook.add(index_page, text="Index Page")
        notebook.add(train_page, text="Train Set")
        notebook.add(val_page, text="Val Set")
        notebook.add(occurrences_page, text="Occurrences Page")

        notebook.pack()

    def create_page(self, parent, set_name, num_images, num_labels, class_counts):
        page = Frame(parent)
        info_text = f"{set_name}:\nNumber of Images: {num_images}\nNumber of Labels: {num_labels}\n"
        info_text += self.generate_class_counts_text(class_counts)
        label_info = Label(page, text=info_text)
        label_info.pack()

        return page

    def create_index_page(self, parent, page_name):
        index_page = Frame(parent)
        index_label = Label(index_page, text="Class Index List:")
        index_label.pack()

        for i, cls in enumerate(self.classes):
            index_text = f"{i}: {cls}"
            index_label = Label(index_page, text=index_text)
            index_label.pack()

        return index_page

    def create_occurrences_page(self, parent, page_name, class_occurrences):
        occurrences_page = Frame(parent)
        occurrences_label = Label(occurrences_page, text=self.generate_class_occurrences_text(class_occurrences))
        occurrences_label.pack()

        return occurrences_page


if __name__ == "__main__":
    root = Tk()
    app = YOLOv5DatasetAnalyzer(root)
    root.geometry("900x700")  # GUI boyutunu değiştirebilirsin
    root.mainloop()
