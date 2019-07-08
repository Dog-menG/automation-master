from skimage import data, transform
from skimage.color import rgb2gray
import os
import numpy as np
import matplotlib.pyplot as plt


def load_data(data_directory):
    directories = [d for d in os.listdir(data_directory)
                   if os.path.isdir(os.path.join(data_directory, d))]
    labels = []
    images = []
    for d in directories:
        label_directory = os.path.join(data_directory, d)
        file_names = [os.path.join(label_directory, f)
                      for f in os.listdir(label_directory)
                      if f.endswith(".ppm")]
        for f in file_names:
            images.append(data.imread(f))
            labels.append(int(d))
    return images, labels


ROOT_PATH = r'C:\Users\dogod\data'
train_data_directory = os.path.join(ROOT_PATH, r'Training')
test_data_directory = os.path.join(ROOT_PATH, r'Testing')

images, labels = load_data(train_data_directory)
images = np.array(images)

# Rescale the images in the `images` array
images28 = [transform.resize(image, (28, 28)) for image in images]

# Convert `images28` to an array
images28 = np.array(images28)

# Convert `images28` to grayscale
images28 = rgb2gray(images28)

traffic_signs = [300, 2250, 3650, 4000]

# Fill out the subplots with the random images that you defined
for i in range(len(traffic_signs)):
    plt.subplot(1, 4, i+1)
    plt.axis('off')
    plt.imshow(images28[traffic_signs[i]], cmap="gray")
    plt.subplots_adjust(wspace=0.5)

plt.show()
