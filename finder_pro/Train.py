import os
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import cv2
from torchvision import models, transforms
from torch.utils.data import Dataset, DataLoader

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Data Transformation
transform = transforms.Compose([
    transforms.ToPILImage(),   # Convert NumPy image to PIL Image
    transforms.Resize((224, 224)),
    transforms.ToTensor(),  # Convert PIL Image to Tensor
])

# Custom Dataset Class
class LocationDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        self.images = []
        self.labels = []
        self.label_mapping = {}

        # Load Data
        for idx, label in enumerate(os.listdir(data_dir)):
            self.label_mapping[label] = idx
            label_folder = os.path.join(data_dir, label)
            for filename in os.listdir(label_folder):
                img_path = os.path.join(label_folder, filename)
                img = cv2.imread(img_path)
                if img is not None:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
                    self.images.append(img)
                    self.labels.append(idx)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img = self.images[idx]
        label = self.labels[idx]

        if self.transform:
            img = self.transform(img)

        return img, label

# Load Data
train_path = os.path.join(os.getcwd(), "dataset", "train")
test_path = os.path.join(os.getcwd(),  "dataset", "test")

train_dataset = LocationDataset(train_path, transform=transform)
test_dataset = LocationDataset(test_path, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

# Load Pretrained MobileNetV2
model = models.mobilenet_v2(pretrained=True)
model.classifier[1] = nn.Linear(model.last_channel, len(train_dataset.label_mapping))  # Adjust classifier

# Move model to device
model = model.to(device)

# Loss & Optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Train Model
num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    correct, total = 0, 0

    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

    train_acc = 100 * correct / total
    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader):.4f}, Accuracy: {train_acc:.2f}%")

    # Evaluate on test set
    model.eval()
    with torch.no_grad():
        correct, total = 0, 0
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

        test_acc = 100 * correct / total
        print(f"Test Accuracy: {test_acc:.2f}%")

# Save Model
torch.save(model, "location_identifier_model.pth")  # Save the full model

#torch.save(model.state_dict(), "location_identifier_model.pth")
print("Model saved successfully!")
