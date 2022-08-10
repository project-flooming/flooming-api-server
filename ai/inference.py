import time

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


def load_image_cv2(path):
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (256, 256))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = torch.Tensor(img / 255.).permute(2, 0, 1)
    return img.unsqueeze(dim=0)


def load_image_pillow(path):
    img = Image.open(path).convert('RGB')
    img = img.resize((256,256))
    img = torch.from_numpy(np.array(img))
    return img.unsqueeze(dim=0)


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
        inputs = load_image_cv2(src)  # cv2로 한거
        # inputs = load_image_pillow(src) # pillow로 한거
        # 위에 cv2랑 pillow 중에 뭐가 더 빠른지 함 테스트해보셈
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

    # @torch.no_grad()
    # def style_convert(self, src):
    #     start1 = time.time()
    #     file_name = src.split('/')[-1]
    #     inputs = Variable(self.transform(Image.open(src).convert('RGB')))
    #     print(f"style_convert : Variable Image.open 시간 = {time.time() - start1}")

    #     start = time.time()
    #     inputs = inputs.unsqueeze(0)
    #     print(f"unsqueeze 시간 = {time.time() - start}")

    #     start = time.time()
    #     output = denormalize(self.styletransfer_model(inputs))
    #     print(f"denormalize 시간 = {time.time() - start}")

    #     start = time.time()
    #     output = to_pil_image(output[0])
    #     print(f"pillow to_pil_image 시간 = {time.time() - start}")

    #     start2 = time.time()
    #     output.save(f'./picture/{file_name}')
    #     print(f"style_convert :output.save 시간 = {time.time() - start2}")
    #     return output
    

    @torch.no_grad()
    def style_convert(self, src):
        file_name = src.split('/')[-1]
        original_img = Image.open(src).convert('RGB')
        original_size = original_img.size
        inputs = original_img.resize((256,256)) # 여기 사이즈 줄여주는 코드 넣음
        inputs = Variable(self.transform(inputs))
        inputs = inputs.unsqueeze(0)
        output = denormalize(self.styletransfer_model(inputs))
        output = to_pil_image(output[0])
        output = output.resize(original_size) # 여기가 upsampling하는 부분
        output.save(f'./picture/{file_name}')
        return output


c_weight_path = './ai/weight/shufflenetv2_weight.pt'
c_inference = Inference(c_weight=c_weight_path)


def classify(image_src):
    return c_inference.classification(image_src)


HAPPY_TEARS = './ai/weight/happy_tears.pt'
MOSAIC = './ai/weight/mosaic.pt'


s_weight_path = MOSAIC
s_inference = Inference(s_weight=s_weight_path)


async def drawing(image_src):
    start = time.time()
    result = s_inference.style_convert(image_src)
    print(f"async def drawing 최종 처리시간 = {time.time() - start}")
    return result