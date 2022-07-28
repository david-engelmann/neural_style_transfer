import torch
import torch.optim as optim
from torchvision.utils import save_image
from images import load_image, display_image, reverse_normalize_to_numpy_array, save_image_from_numpy_array, reverse_normalize_to_torch_tensor
from models import VGG
from device import device
from hyperparameters import Hyperparameters
from losses import calculate_total_loss, multi_step
import gc
import os
import shutil
import matplotlib.pyplot as plt
import numpy as np
from typing import Union


def apply_style_transfer(content_image_path: str, style_image_path, hyperparameters: Hyperparameters, output_image_path):
    model = VGG(require_grad=hyperparameters.require_grad, use_avg_pool=hyperparameters.use_avg_pool).to(device).eval()
    
    total_steps = hyperparameters.total_steps
    learning_rate = hyperparameters.learning_rate
    alpha = hyperparameters.alpha
    beta = hyperparameters.beta
    normalize = hyperparameters.normalize
    optimizer = hyperparameters.optimizer
 
    content_image = load_image(content_image_path, normalize=normalize)

    style_image = load_image(style_image_path, normalize=normalize)
 
    cloned_noise_image = content_image.clone().to(device, torch.float)
    cloned_noise_image.requires_grad_(True)

    for step in range(1, total_steps+1): 
        cloned_features = model(cloned_noise_image)
        content_features = model(content_image)
        style_features = model(style_image)
        
        total_loss = calculate_total_loss(cloned_features, content_features, style_features, alpha=alpha, beta=beta)

        optimizer.zero_grad()
        total_loss.backward()
        optimizer.step()

        if step == total_steps:
            if normalize:
                numpy_noise_image = reverse_normalize_to_numpy_array(cloned_noise_image)
                save_image_from_numpy_array(numpy_noise_image, output_image_path)
            else: 
                save_image(cloned_noise_image, output_image_path)

    return output_image_path

print("done importing")
model = VGG().to(device).eval()

print("make it past model")

david_headshot_path = "assets/david_headshot.jpeg"

self_portrait_main_path = "assets/self_portrait_main.jpeg"
another_self_portrait_path = "assets/another_self_portrait.jpg"
japan_self_portrait_path = "assets/japan_self_portrait.jpeg"
painting_self_portrait_path = "assets/painting_self_portrait.jpeg"
on_the_street_path = "assets/on_the_street.jpg"

self_portrait_style_image = load_image(self_portrait_main_path, 480)
#another_self_portrait_style_image = load_image(another_self_portrait_path)
#self_portrait_style_image = load_image(japan_self_portrait_path, 480)
#japan_self_portrait_style_image = load_image(japan_self_portrait_path)
#painting_self_portrait_style_image = load_image(painting_self_portrait_path)
print("content loaded")
david_headshot_image = load_image(on_the_street_path, 480)

#generated_noise_image = torch.randn(david_headshot_image.shape, device=device, requires_grad=True)

cloned_noise_image = david_headshot_image.clone().to(device, torch.float)
cloned_noise_image.requires_grad_(True)

total_steps = 2000
learning_rate = .001
alpha = 1
beta = .01
self_portrait_optimizer = optim.Adam([cloned_noise_image], lr=learning_rate)
#another_self_portrait_optimizer = optim.Adam([cloned_noise_image], lr=learning_rate)
#japan_self_portrait_optimizer = optim.Adam([cloned_noise_image], lr=learning_rate)
#painting_self_portrait_optimizer = optim.Adam([cloned_noise_image], lr=learning_rate)
#hyperparameters = Hyperparameters(total_steps=total_steps, learning_rate=learning_rate, alpha=alpha, beta=beta, optimizer=optimizer)
print("made it")
for step in range(1, total_steps+1): 
    cloned_features = model(cloned_noise_image)
    content_features = model(david_headshot_image)
    self_portrait_style_features = model(self_portrait_style_image)
#    another_self_portrait_style_features = model(another_self_portrait_style_image)
#    japan_self_portrait_style_features = model(japan_self_portrait_style_image)
#    painting_self_portrait_style_features = model(painting_self_portrait_style_image)
    self_portrait_total_loss = calculate_total_loss(cloned_features, content_features, self_portrait_style_features, alpha=alpha, beta=beta)
#    another_self_portrait_total_loss = calculate_total_loss(cloned_features, content_features, another_self_portrait_style_features)
#    japan_self_portrait_total_loss = calculate_total_loss(cloned_features, content_features, japan_self_portrait_style_features)
#    painting_self_portrait_total_loss = calculate_total_loss(cloned_features, content_features, painting_self_portrait_style_features)
#
#    del cloned_features
#    del content_features
#    del self_portrait_style_features
#    del another_self_portrait_style_features
#    del japan_self_portrait_style_features
#    del painting_self_portrait_style_features

    #multi_step([self_portrait_total_loss, another_self_portrait_total_loss, japan_self_portrait_total_loss, painting_self_portrait_total_loss], 
    #           [self_portrait_optimizer, another_self_portrait_optimizer, japan_self_portrait_optimizer, painting_self_portrait_optimizer])
    
    self_portrait_optimizer.zero_grad()
    self_portrait_total_loss.backward()
    self_portrait_optimizer.step()
    
#    if step % 100 == 0:
#        plt.figure()
#        display_image(cloned_noise_image, f"Step: {step}")
#        plt.show() 
    if step == total_steps:
#        print(f"self_portrait_total_loss: {self_portrait_total_loss}\nanother_self_portrait_total_loss: {another_self_portrait_total_loss}\njapan_self_portrait_total_loss: {japan_self_portrait_total_loss}\npainting_self_portrait_total_loss: {painting_self_portrait_total_loss}\n")
        
        #pytorch_noise_image = reverse_normalize_to_numpy_array(cloned_noise_image)
        save_image(cloned_noise_image, "self_generated_ktown_from_pytorch_no_norm_max_pool_2000.png")
        
        #numpy_noise_image = reverse_normalize_to_numpy_array(cloned_noise_image)
        #save_image_from_numpy_array(numpy_noise_image, "generated2.png")
        print("Image Saved")
#        cloned_noise_image = np.uint8(255 * cloned_noise_image)
#        cloned_noise_image = torch.from_numpy(cloned_noise_image).to(torch.int8)
#        
#        save_image(cloned_noise_image, "generated_from_pytorch.png")