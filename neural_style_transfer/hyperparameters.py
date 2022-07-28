import torch.optim as optim
from typing import Union

class Hyperparameters:
    def __init__(self, total_steps: int = 6000, learning_rate: float = .001, alpha: Union[int, float] = 1, beta: float = .01, optimizer = None, noise_image = None, require_grad: bool = False, use_avg_pool: bool = False, normalize: bool = False):
        if optimizer is not None and noise_image is not None:
            raise "Can't have both an optimizer set and a noise_image, noise_image is just for when no optimizer is provided (Defaults to Adam)"
        self.total_steps = total_steps
        self.learning_rate = learning_rate
        self.alpha = alpha
        self.beta = beta
        if optimizer is not None:
            self.optimizer = optimizer
        else:
            self.optimizer = optim.Adam([noise_image], lr=self.learning_rate)

        self.require_grad = require_grad
        self.use_avg_pool = use_avg_pool
        self.normalize = normalize

    
    def __str__(self) -> str:
        return f"total_steps: {self.total_steps}\nlearning_rate: {self.learning_rate}\nalpha: {self.alpha}\nbeta: {self.beta}\noptimizer: {self.optimizer}"


def get_hyperparameters(content_image_path: str, total_steps: int = 6000, learning_rate: float = .001, alpha: Union[int, float] = 1, beta: float = .01, require_grad: bool = False, use_avg_pool: bool = False, normalize: bool = False):
    return Hyperparameters(total_steps=total_steps, learning_rate=learning_rate, alpha=alpha, beta=beta, noise_image=content_image_path, require_grad=require_grad, use_avg_pool=use_avg_pool, normalize=normalize)


