import torch.nn as nn
import math
from collections import OrderedDict
import torch.nn.functional as F

from models.resnet.layers import MaskedConv2d
from models.resnet.layers import MaskedLinear

__all__ = ['ResNet', 'resnet18', 'resnet34', 'resnet50', 'resnet101',
           'resnet152']


model_urls = {
    'resnet18': 'https://download.pytorch.org/models/resnet18-5c106cde.pth',
    'resnet34': 'https://download.pytorch.org/models/resnet34-333f7ec4.pth',
    'resnet50': 'https://download.pytorch.org/models/resnet50-19c8e357.pth',
    'resnet101': 'https://download.pytorch.org/models/resnet101-5d3b4d8f.pth',
    'resnet152': 'https://download.pytorch.org/models/resnet152-b121ed2d.pth',
}


def conv3x3(in_planes, out_planes, stride=1):
    # "3x3 convolution with padding"
    #return nn.Conv2d(in_planes, out_planes, kernel_size=3, stride=stride, padding=1, bias=False)
    return MaskedConv2d(in_planes, out_planes, kernel_size=3, stride=stride, padding=1, bias=False)


class BasicBlock(nn.Module):
    expansion = 1
    def __init__(self, inplanes, planes, stride=1, downsample=None):
        super(BasicBlock, self).__init__()
        '''m = OrderedDict()
        m['conv1'] = conv3x3(inplanes, planes, stride)
        m['bn1'] = nn.BatchNorm2d(planes)
        m['relu1'] = nn.ReLU(inplace=True)
        m['conv2'] = conv3x3(planes, planes)
        m['bn2'] = nn.BatchNorm2d(planes)
        self.group1 = nn.Sequential(m)'''

        '''self.conv1 = conv3x3(inplanes, planes, stride)
        self.bn1 = nn.BatchNorm2d(planes)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = conv3x3(planes, planes)
        self.bn2 = nn.BatchNorm2d(planes)'''

        self.conv1 = MaskedConv2d(inplanes, planes, stride)
        self.bn1 = nn.BatchNorm2d(planes)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = MaskedConv2d(planes, planes)
        self.bn2 = nn.BatchNorm2d(planes)

        #self.relu = nn.Sequential(nn.ReLU(inplace=True))
        self.relu = nn.ReLU(inplace=True)

        self.downsample = downsample

    def forward(self, x):
        if self.downsample is not None:
            residual = self.downsample(x)
        else:
            residual = x

        #out = self.group1(x) + residual
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        out = self.conv2(out)
        out = self.bn2(out)
        
        out = out + residual

        #out = self.relu(out)
        out = F.relu(out)

        return out


class Bottleneck(nn.Module):
    expansion = 4
    def __init__(self, inplanes, planes, stride=1, downsample=None):
        super(Bottleneck, self).__init__()
        '''m  = OrderedDict()
        m['conv1'] = nn.Conv2d(inplanes, planes, kernel_size=1, bias=False)
        m['bn1'] = nn.BatchNorm2d(planes)
        m['relu1'] = nn.ReLU(inplace=True)
        m['conv2'] = nn.Conv2d(planes, planes, kernel_size=3, stride=stride, padding=1, bias=False)
        m['bn2'] = nn.BatchNorm2d(planes)
        m['relu2'] = nn.ReLU(inplace=True)
        m['conv3'] = nn.Conv2d(planes, planes * 4, kernel_size=1, bias=False)
        m['bn3'] = nn.BatchNorm2d(planes * 4)
        self.group1 = nn.Sequential(m)'''

        '''self.conv1 = nn.Conv2d(inplanes, planes, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.conv3 = nn.Conv2d(planes, planes * 4, kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm2d(planes * 4)'''

        self.conv1 = MaskedConv2d(inplanes, planes, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = MaskedConv2d(planes, planes, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.conv3 = MaskedConv2d(planes, planes * 4, kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm2d(planes * 4)

        #self.relu = nn.Sequential(nn.ReLU(inplace=True))
        self.relu = nn.ReLU(inplace=True)

        self.downsample = downsample

    def forward(self, x):
        if self.downsample is not None:
            residual = self.downsample(x)
        else:
            residual = x

        #out = self.group1(x) + residual
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)
        out = self.conv3(out)
        out = self.bn3(out)
        
        out = out + residual

        #out = self.relu(out)
        out = F.relu(out)

        return out


class ResNet(nn.Module):

    def __init__(self, block, layers, num_classes=1000):
        self.inplanes = 64
        super(ResNet, self).__init__()

        '''m = OrderedDict()
        m['conv1'] = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
        m['bn1'] = nn.BatchNorm2d(64)
        m['relu1'] = nn.ReLU(inplace=True)
        m['maxpool'] = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        self.group1= nn.Sequential(m)'''

        #self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.conv1 = MaskedConv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        self.layer1 = self._make_layer(block, 64, layers[0])
        self.layer2 = self._make_layer(block, 128, layers[1], stride=2)
        self.layer3 = self._make_layer(block, 256, layers[2], stride=2)
        self.layer4 = self._make_layer(block, 512, layers[3], stride=2)

        #self.avgpool = nn.Sequential(nn.AvgPool2d(7))
        self.avgpool = nn.AvgPool2d(kernel_size=7, stride=1, padding=0)

        '''self.group2 = nn.Sequential(
            OrderedDict([
                ('fc', nn.Linear(512 * block.expansion, num_classes))
            ])
        )'''
        #self.fc = nn.Linear(512 * block.expansion, num_classes)
        self.fc = MaskedLinear(512 * block.expansion, num_classes)

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                m.weight.data.normal_(0, math.sqrt(2. / n))
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()

    def _make_layer(self, block, planes, blocks, stride=1):
        downsample = None
        if stride != 1 or self.inplanes != planes * block.expansion:
            downsample = nn.Sequential(
                nn.Conv2d(self.inplanes, planes * block.expansion, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(planes * block.expansion),
            )

        layers = []
        layers.append(block(self.inplanes, planes, stride, downsample))
        self.inplanes = planes * block.expansion
        for i in range(1, blocks):
            layers.append(block(self.inplanes, planes))

        return nn.Sequential(*layers)

    def forward(self, x):
        #x = self.group1(x)
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        #x = self.group2(x)
        x = self.fc(x)

        return x

    def set_conv_mask(self, layer_index, layer_item):
        convlayers = 0
        for module in self.modules():
            if module.__str__().startswith('MaskedConv2d'):  #[cout, cin, k, k]
                if convlayers == layer_index:
                    for i in layer_item:
                        #print(module._mask[i,j,:,:])
                        module._mask[i,:,:,:] = 0
                        #print(module._mask[i,j,:,:])
                if convlayers == layer_index + 1:
                    for j in layer_item:
                        #print(module._mask[i,j,:,:])
                        module._mask[:,j,:,:] = 0
                        #print(module._mask[i,j,:,:])
                convlayers = convlayers + 1

    def set_linear_mask(self, layer_index, layer_item):
        linearlayers = 0
        for module in self.modules():
            if module.__str__().startswith('MaskedLinear'):  #[cout, cin]
                if linearlayers == layer_index:
                    for i in layer_item:
                        #print(module._mask[i,j])
                        module._mask[i,:] = 0
                        #print(module._mask[i,j])
                if linearlayers == layer_index + 1:
                    for j in layer_item:
                        #print(module._mask[i,j])
                        module._mask[:,j] = 0
                        #print(module._mask[i,j])
                linearlayers = linearlayers + 1

    def set_conv_linear_mask(self, conv_layer_index, linear_layer_index, conv_layer_item, fc_layer_item):
        convlayers = 0
        for module in self.modules():
            if module.__str__().startswith('MaskedConv2d'):  #[cout, cin, k, k]
                if convlayers == conv_layer_index:
                    for i in conv_layer_item:
                        #print(module._mask[i,j,:,:])
                        module._mask[i,:,:,:] = 0
                        #print(module._mask[i,j,:,:])
                convlayers = convlayers + 1

        linearlayers = 0
        for module in self.modules():
            if module.__str__().startswith('MaskedLinear'):  #[cout, cin]
                if linearlayers ==  linear_layer_index:
                    for j in fc_layer_item:
                        #print(module._mask[i,j])
                        module._mask[:,j] = 0
                        #print(module._mask[i,j])
                linearlayers = linearlayers + 1


def resnet18(pretrained=False, model_root=None, **kwargs):
    model = ResNet(BasicBlock, [2, 2, 2, 2], **kwargs).cuda()
    if pretrained:
        misc.load_state_dict(model, model_urls['resnet18'], model_root)
    return model


def resnet34(pretrained=False, model_root=None, **kwargs):
    model = ResNet(BasicBlock, [3, 4, 6, 3], **kwargs).cuda()
    if pretrained:
        misc.load_state_dict(model, model_urls['resnet34'], model_root)
    return model


def resnet50(pretrained=False, model_root=None, **kwargs):
    model = ResNet(Bottleneck, [3, 4, 6, 3], **kwargs).cuda()
    if pretrained:
        misc.load_state_dict(model, model_urls['resnet50'], model_root)
    return model


def resnet101(pretrained=False, model_root=None, **kwargs):
    model = ResNet(Bottleneck, [3, 4, 23, 3], **kwargs).cuda()
    if pretrained:
        misc.load_state_dict(model, model_urls['resnet101'], model_root)
    return model


def resnet152(pretrained=False, model_root=None, **kwargs):
    model = ResNet(Bottleneck, [3, 8, 36, 3], **kwargs).cuda()
    if pretrained:
        misc.load_state_dict(model, model_urls['resnet152'], model_root)
    return model
