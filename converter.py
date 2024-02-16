import os
import shutil
from tkinter import Tk, filedialog, Label, Button, StringVar

#this py file converts
#/dataset
#--/train
#----/images
#----/labels
#--/valid
#----/images
#----/labels

#into

#/dataset
#--/images
#----/train
#----/val
#--/labels
#----/train
#----/val

#this



def copy_images_and_labels(src_images, src_labels, dest_images, dest_labels):
    # Copy images and labels
    for filename in os.listdir(src_images):
        src_img_path = os.path.join(src_images, filename)
        dest_img_path = os.path.join(dest_images, filename)
        shutil.copy2(src_img_path, dest_img_path)

        # Copy label files
        label_filename = os.path.splitext(filename)[0] + ".txt"
        src_label_path = os.path.join(src_labels, label_filename)
        dest_label_path = os.path.join(dest_labels, label_filename)
        shutil.copy2(src_label_path, dest_label_path)

def copy_dataset(src_root, dest_root):
    # Folder structure to be created
    dest_train_images = os.path.join(dest_root, 'images', 'train')
    dest_val_images = os.path.join(dest_root, 'images', 'val')
    dest_train_labels = os.path.join(dest_root, 'labels', 'train')
    dest_val_labels = os.path.join(dest_root, 'labels', 'val')

    # Create folders
    os.makedirs(dest_train_images, exist_ok=True)
    os.makedirs(dest_val_images, exist_ok=True)
    os.makedirs(dest_train_labels, exist_ok=True)
    os.makedirs(dest_val_labels, exist_ok=True)

    # Copy train data
    train_images_src = os.path.join(src_root, 'train', 'images')
    train_labels_src = os.path.join(src_root, 'train', 'labels')
    copy_images_and_labels(train_images_src, train_labels_src, dest_train_images, dest_train_labels)

    # Copy val data
    val_images_src = os.path.join(src_root, 'valid', 'images')
    val_labels_src = os.path.join(src_root, 'valid', 'labels')
    copy_images_and_labels(val_images_src, val_labels_src, dest_val_images, dest_val_labels)

    # Delete train and valid folders in source folder
    shutil.rmtree(os.path.join(src_root, 'train'))
    shutil.rmtree(os.path.join(src_root, 'valid'))

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        destination_folder_var.set(folder_selected)
        source_folder_var.set(folder_selected)

def process_dataset():
    src_folder = source_folder_var.get()
    dest_folder = destination_folder_var.get()

    if src_folder and dest_folder:
        copy_dataset(src_folder, dest_folder)
        result_label.config(text="Copying Complete!")
    else:
        result_label.config(text="Please choose true and real folder, there is an error")

# Create GUI
root = Tk()
root.title("YoloV5 Dataset Converting")

# UI Elements
source_label = Label(root, text="Source Folder:")
source_label.pack()

destination_folder_var = StringVar()
destination_folder_var.set("Target Folder:")
destination_folder_label = Label(root, textvariable=destination_folder_var)
destination_folder_label.pack()

source_folder_var = StringVar()
source_folder_label = Label(root, textvariable=source_folder_var)
source_folder_label.pack()

result_label = Label(root, text="")
result_label.pack()

select_button = Button(root, text="Choose dataset folder", command=select_folder)
select_button.pack()

process_button = Button(root, text="Convert Dataset", command=process_dataset)
process_button.pack()

root.mainloop()
