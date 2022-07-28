import torchvision.transforms as transforms
from device import device
import torch

image_size = 550
normalization_mean = torch.tensor([.485, .456, .406]).to(device)
normalization_std = torch.tensor([.229, .224, .225]).to(device)

def get_loader(image_size, normalize: bool = False):
    if normalize:
        loader = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=normalization_mean, std=normalization_std)
        ])
    else:
        loader = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor()
        ])
    return loader

loader = get_loader(image_size, normalize=False)

unloader = transforms.ToPILImage()

normalizer = transforms.Lambda(lambda img: img * normalization_std + normalization_mean)
