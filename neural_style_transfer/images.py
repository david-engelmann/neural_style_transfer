from PIL import Image
from device import device
from loader import get_loader, unloader, normalization_mean, normalization_std, normalizer
import torch
import matplotlib.pyplot as plt
import numpy as np

image_size = 550 

def load_image(image_path, max_size: int = 1500, shape: tuple = None, normalize: bool = False):
    image = Image.open(image_path).convert("RGB")
    if max(image.size) > max_size:
        size = max_size
    else:
        size = max(image.size)

    if shape is not None:
        size = shape
    
    loader = get_loader(image_size=size, normalize=normalize)

    image = loader(image)[:3, :, :].unsqueeze(0)
    return image.to(device, torch.float)

def reverse_normalize_to_numpy_array(tensor) -> np.ndarray:
    image = tensor.to("cpu").clone().detach()
    image = image.numpy().squeeze()
    image = image.transpose(1, 2, 0)
    image = image * normalization_std.numpy() + normalization_mean.numpy()
    image = image.clip(0, 1)
    return image

def reverse_normalize_to_torch_tensor(tensor) -> torch.tensor:
    tensor = tensor.cpu().clone().squeeze(0)
    tensor = normalizer(tensor)
    return tensor


def display_image(tensor, title: str = None):
    plt.figure()
    image = tensor.clone()
    image = tensor.squeeze(0)
    image = unloader(image)
    plt.imshow(image)
    if title:
        plt.title(title)
    plt.savefig("tmp_training_image.png")


def save_image_from_numpy_array(array, file_name: str):
    image = Image.fromarray(np.uint8(255 * array))
    image.save(file_name)