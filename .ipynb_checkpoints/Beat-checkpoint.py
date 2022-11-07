import random
from Note import Note
from Score import hand
from Score import density
from Score import isSlide
from Score import isSlides
from Score import beat
class Beat(Note):
    '''
    普通按键
    '''
    def __init__(self,beat):
        self.beat = beat
    def add(self):
        global hand,density,isSlide,isSlides,beat
        visible=random.random()
        if not isSlides: #如果上一个不是双押长条
            if isSlide: #如果上一个为长条
                if hand==0: #长条为左手
                    lane=random.randint(min(slane+slideMinDistence,6),6) #键的位置在右侧
                elif hand==1:#长条为右手
                    lane=random.randint(0,max(slane-slideMinDistence,0)) #键的位置在左侧
                hand=-1 #恢复使用手的限制
            else: #如果上一个不是长条
                lane=random.randint(0,6)
            if visible<=density:
                ret = '{"type":"Single","lane":'+str(lane)+',"beat":'+str(beat)+'}'
        beat=beat+4/(float(self.beat))
        isSlide=False
        isSlides=False
        return ret