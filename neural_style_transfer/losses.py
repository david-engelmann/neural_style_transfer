import os 
import torch
import shutil
import gc

def calculate_content_loss(cloned_feature, content_feature):
    return torch.mean((cloned_feature - content_feature) ** 2)


def calculate_style_loss(cloned_feature, style_feature):
    batch_size, channel, height, width = cloned_feature.shape
    cloned_gram_matrix = torch.mm(cloned_feature.view(channel, height*width), cloned_feature.view(channel, height*width).t())
    style_gram_matrix = torch.mm(style_feature.view(channel, height*width), style_feature.view(channel, height*width).t())

    return torch.mean((cloned_gram_matrix-style_gram_matrix) **2 )


def calculate_total_loss(cloned_features, content_features, style_features, alpha = 1, beta = .01):
    content_loss = 0
    style_loss = 0
    for cloned_feature, content_feature, style_feature in zip(cloned_features, content_features, style_features):
        content_loss += calculate_content_loss(cloned_feature, content_feature)
        style_loss += calculate_style_loss(cloned_feature, style_feature)
    return alpha*content_loss + beta*style_loss


def multi_step(losses, optimizers):
    grads = [None]*len(losses)
    for i, (loss, optimizer) in enumerate(zip(losses, optimizers)):
        retain_graph = i != (len(losses)-1)
        optimizer.zero_grad()
        try:
            loss.backward(retain_graph=retain_graph)
        except Exception as er:
            try:
                gc.collect()
                loss.backward(retain_graph=retain_graph)
            except Exception as err:
                print(f"First Error:\n{er}\nSecond Error:\n{err}\n")
        grads[i] = [[p.grad+0 for p in group["params"]] for group in optimizer.param_groups]
    for optimizer, grad in zip(optimizers, grads):
        for p_group, g_group in zip(optimizer.param_groups, grad):
            for p, g in zip(p_group["params"], g_group):
                p.grad = g
        optimizer.step()