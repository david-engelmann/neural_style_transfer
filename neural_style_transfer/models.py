import torch.nn as nn
import torchvision.models as models
from device import device

class VGG(nn.Module):
    def __init__(self, require_grad: bool = False, use_avg_pool: bool = False):
        super(VGG, self).__init__()
        print("after super") 
        self.chosen_features = ["0", "5", "10", "19", "28"]
        self.model = models.vgg19(pretrained=True)
        print("made it to model")
        if not require_grad:
            self.change_parameters_to_not_require_grad()
        self.model = self.model.features[:29]
        if use_avg_pool:
            self.convert_max_pool_to_avg_pool()
    
    def forward(self, inp):
        features = []
        
        for layer_mum, layer in enumerate(self.model):
            inp = layer(inp)
            if str(layer_mum) in self.chosen_features:
                features.append(inp)

        return features

    def change_parameters_to_not_require_grad(self):
        for param in self.model.parameters():
            param.requires_grad_(False)
        return self

    def convert_max_pool_to_avg_pool(self):
        for i, layer in enumerate(self.model):
            if isinstance(layer, nn.MaxPool2d):
                self.model[i] = nn.AvgPool2d(kernel_size=2, stride=2, padding=0)
        return self

model = VGG(require_grad=True, use_avg_pool=True)