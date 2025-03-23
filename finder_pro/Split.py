import os
import shutil
import random

# Define paths
source_dir = os.path.join(os.getcwd(), "finder_pro","dataset")

#source_dir = "dataset"  # Folder containing images in subfolders (one per class)
train_dir = "dataset/train"
test_dir = "dataset/test"

# Train-test split ratio
split_ratio = 0.8  # 80% train, 20% test

# Create train & test directories
for folder in [train_dir, test_dir]:
    os.makedirs(folder, exist_ok=True)

# Iterate over each class folder in dataset
for class_name in os.listdir(source_dir):
    class_path = os.path.join(source_dir, class_name)
    
    if not os.path.isdir(class_path):  # Skip non-directory files
        continue
    
    # Create subdirectories in train & test folders
    train_class_path = os.path.join(train_dir, class_name)
    test_class_path = os.path.join(test_dir, class_name)
    
    os.makedirs(train_class_path, exist_ok=True)
    os.makedirs(test_class_path, exist_ok=True)
    
    # Get all images in class folder
    images = [img for img in os.listdir(class_path) if img.endswith((".jpg", ".png", ".jpeg"))]
    
    # Shuffle images
    random.shuffle(images)
    
    # Split into train & test
    split_index = int(len(images) * split_ratio)
    train_images = images[:split_index]
    test_images = images[split_index:]
    
    # Move images to respective folders
    for img in train_images:
        shutil.move(os.path.join(class_path, img), os.path.join(train_class_path, img))
    
    for img in test_images:
        shutil.move(os.path.join(class_path, img), os.path.join(test_class_path, img))

print("Dataset successfully split into train & test folders! ✅")
