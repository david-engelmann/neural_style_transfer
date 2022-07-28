def test_loading_vgg19():
    import torchvision.models as models
    model = models.vgg19(pretrained=True).features
    assert model != None
    assert True == True
