import numpy as np
import cv2
from PIL import Image

import torch
import torch.nn.functional as F
from torch.autograd import Variable
from torchvision.transforms.functional import to_pil_image

from ai.models.shufflenetv2 import ShuffleNetV2
from ai.models.styletransfer import TransformerNet
from .util import denormalize, style_transform


def load_image(path):
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    original_size = img.shape
    img = cv2.resize(img, (256, 256))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = torch.Tensor(img / 255.).permute(2, 0, 1)
    return img.unsqueeze(dim=0), original_size


class Inference:

    def __init__(
            self,
            c_weight=None,
            s_weight=None,
            num_classes=28
    ):

        # Classification Phase
        if c_weight is not None:
            self.classification_model = ShuffleNetV2(num_classes=num_classes).cpu()
            self.classification_model.load_state_dict(torch.load(c_weight, map_location=torch.device('cpu')))
            self.classification_model.eval()

        # Style Transfer Phase
        if s_weight is not None:
            self.styletransfer_model = TransformerNet().cpu()
            self.styletransfer_model.load_state_dict(torch.load(s_weight, map_location=torch.device('cpu')))
            self.styletransfer_model.eval()
            self.transform = style_transform()

        self.classes = {
            0: '얼레지',
            1: '노루귀',
            2: '애기똥풀',
            3: '제비꽃',
            4: '민들레',
            5: '할미꽃',
            6: '은방울꽃',
            7: '비비추',
            8: '패랭이꽃',
            9: '수련',
            10: '맥문동',
            11: '엉겅퀴',
            12: '참나리',
            13: '초롱꽃',
            14: '상사화',
            15: '동백',
            16: '개망초',
            17: '장미',
            18: '해바라기',
            19: '무궁화',
            20: '진달래',
            21: '개나리',
            22: '수국',
            23: '연꽃',
            24: '나팔꽃',
            25: '목련',
            26: '벚꽃',
            27: '튤립',
        }

    @torch.no_grad()
    def classification(self, src):
        inputs, _ = load_image(src)
        output = self.classification_model(inputs)
        prob_with_idx = torch.sort(F.softmax(output))
        result = []
        total = prob_with_idx[0][0][-3:].sum().item()
        for i in range(1, 4):
            prob = prob_with_idx[0][0][-3:][-i].item()
            idx = prob_with_idx[1][0][-3:][-i].item()
            prob_100 = int((prob / total) * 100)
            output = {
                'probability': prob_100,
                'type': self.classes[idx]
            }
            result.append(output)
        return result

    @torch.no_grad()
    def transform(self, src):
        file_name = src.split('/')[-1]
        inputs = Variable(self.transform(Image.open(src)))
        inputs = inputs.unsqueeze(0)
        output = denormalize(self.styletransfer_model(inputs))
        output = to_pil_image(output[0])
        output.save(f'./picture/{file_name}')
        return output


c_weight_path = './ai/weight/shufflenetv2_weight.pt'
c_inference = Inference(c_weight=c_weight_path)


def classify(image_src):
    return c_inference.classification(image_src)


s_weight_path = './ai/weight/mosaic.pt'
s_inference = Inference(s_weight=s_weight_path)


async def drawing(image_src):
    return s_inference.transform(image_src)