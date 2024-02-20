import glob
import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib

def list_nii_paths(directory):
    """Generator function to iterate over all nii files in a given directory.

    Args:
        directory: Directory path to search for nii files.

    Yields:
        Sorted array of file paths for each nii file found.
    """
    file_paths = glob.glob(f'{directory}/**/*.nii', recursive=True)
    return np.array(sorted(file_paths))

def list_prostate_paths(directory):
    """Generator function to iterate over all prostate and lesion mask files in a given directory.

    Args:
        directory: Directory path to search for mask files.

    Yields:
        Sorted array of file paths for lesion and prostate mask files found.
    """
    lesion_paths = glob.glob(f'{directory}/**/lesion_mask.npy', recursive=True)
    prostate_paths = glob.glob(f'{directory}/**/prostate_mask.npy', recursive=True)
    return np.array([sorted(lesion_paths), sorted(prostate_paths)])

def nib_to_numpy(directory):
    """Load an image using nibabel, and convert it to a numpy array.

    Args:
        directory: Directory path to convert nib file to numpy array.

    Yields:
        Numpy array of type uint8.
    """
    image = nib.load(directory).dataobj
    return np.array(image).astype(np.uint8)

def visualize_sample(img_tensor, label_tensor, img_size=(7, 3), pred_tensor=None):
    img = img_tensor.numpy().squeeze()
    label = label_tensor.numpy().squeeze()
    
    if pred_tensor is not None:
        pred = pred_tensor.numpy().squeeze()
        fig, axes = plt.subplots(1, 3, figsize=img_size)
        titles = ['Image', 'True Mask', 'Predicted Mask']
        images = [img, label, pred]
    else:
        fig, axes = plt.subplots(1, 2, figsize=img_size) 
        titles = ['Image', 'True Mask']
        images = [img, label]
    for ax, image, title in zip(axes, images, titles):
        ax.imshow(image, cmap='gray')
        ax.set_title(title)
        ax.axis('off') 

    plt.tight_layout()
    plt.show()