from database.models import Flower


def img_src(num):
    return f"./photo/{num}.jpg"

def img_src2(kor_name):
    return f"./photo/{kor_name}.jpg"

flower_list = [
    Flower(kor_name="얼레지", eng_name="Erythronium japonicum", flower_language="질투", img_src=img_src2(0)),
    Flower(kor_name="노루귀", eng_name="Hepatica", flower_language="인내", img_src=img_src(1)),
    Flower(kor_name="애기똥풀", eng_name="Greater celandine", flower_language="몰래주는 사랑", img_src=img_src(2)),
    Flower(kor_name="제비꽃", eng_name="Violet", flower_language="작은 사랑", img_src=img_src(3)),
    Flower(kor_name="민들레", eng_name="Dandelion", flower_language="행복과 감사", img_src=img_src(4)),
    Flower(kor_name="할미꽃", eng_name="Pasque flower", flower_language="슬픈 추억", img_src=img_src(5)),
    Flower(kor_name="은방울꽃", eng_name="Lily of the valley", flower_language="섬세함", img_src=img_src(6)),
    Flower(kor_name="비비추", eng_name="Hosta", flower_language="좋은 소식", img_src=img_src(7)),
    Flower(kor_name="패랭이꽃", eng_name="Gilly flower", flower_language="재능", img_src=img_src(8)),
    Flower(kor_name="수련", eng_name="Lotus", flower_language="깨끗한 마음", img_src=img_src(9)),
    
    Flower(kor_name="맥문동", eng_name="Lilyturf", flower_language="기쁨의 연속", img_src=img_src(10)),
    Flower(kor_name="엉겅퀴", eng_name="Thistle", flower_language="고독한 사랑", img_src=img_src(11)),
    Flower(kor_name="참나리", eng_name="Tiger lily", flower_language="깨꿋한 마음", img_src=img_src(12)),
    Flower(kor_name="초롱꽃", eng_name="Lantern flower", flower_language="감사", img_src=img_src(13)),
    Flower(kor_name="상사화", eng_name="Magic lily", flower_language="이루어질 수 없는 사랑", img_src=img_src(14)),
    Flower(kor_name="동백", eng_name="Camellia", flower_language="나는 당신만을 사랑합니다.", img_src=img_src(15)),
    Flower(kor_name="개망초", eng_name="Sagebrush", flower_language="화해", img_src=img_src(16)),
    Flower(kor_name="장미", eng_name="Rose", flower_language="사랑", img_src=img_src(17)),
    Flower(kor_name="해바라기", eng_name="Sun flower", flower_language="자부심", img_src=img_src(18)),
    Flower(kor_name="무궁화", eng_name="Rose of Sharon", flower_language="일편단심", img_src=img_src(19)),

    Flower(kor_name="진달래", eng_name="Azalea", flower_language="사랑의 기쁨", img_src=img_src(20)),
    Flower(kor_name="개나리", eng_name="Forsythia", flower_language="기대", img_src=img_src(21)),
    Flower(kor_name="수국", eng_name="Hydrangea", flower_language="진심", img_src=img_src(22)),
    Flower(kor_name="연꽃", eng_name="Lotus", flower_language="청결", img_src=img_src(23)),
    Flower(kor_name="나팔꽃", eng_name="Morning glory", flower_language="덧없는 사랑", img_src=img_src(24)),
    Flower(kor_name="목련", eng_name="Magnolia", flower_language="고귀함", img_src=img_src(25)),
    Flower(kor_name="벚꽃", eng_name="Cherry blossom", flower_language="당신에게 미소를", img_src=img_src(26)),
    Flower(kor_name="튤립", eng_name="Tulip", flower_language="새로운 시작", img_src=img_src(27)),
]
