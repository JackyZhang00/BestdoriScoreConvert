import random
from Note import Note
from Score import hand
from Score import beat
from Score import isSlide
from Score import isSlides
from Score import density
from Score import slideMinDistence
from Score import mindistence
class DSingle(Note):
    '''
    双押普通
    '''
    def __init__(self,beat):
        self.beat = beat
    def add(self):
        global hand,beat,isSlide,isSlides,density,slideMinDistence,mindistence #声明全局变量hand
        visible=random.random()
        if not isSlides: #判断上一个是否为双押长条

            #判断上一个是否为长条形
            if not isSlide:
                lane1=random.randint(0,6) #第一个键
                lane2=random.randint(0,6) #第二个键
                while abs(lane2-lane1)<mindistence:
                    lane1=random.randint(0,6)
                    lane2=random.randint(0,6) #若两个键相同，重新生成
                if visible<=density:
                    #输出结果
                    ret = '{"type":"Single","lane":'+str(lane1)+',"beat":'+str(beat)+'}'
                    ret = ret + '{"type":"Single","lane":'+str(lane2)+',"beat":'+str(beat)+'}'
            #如果上一个为长条形，则于普通键一样
            if isSlide:
                if hand==0: #长条为左手
                    lane=random.randint(min(slane+slideMinDistence,6),6) #键的位置在右侧
                elif hand==1:#长条为右手
                    lane=random.randint(0,max(slane-slideMinDistence,0)) #键的位置在左侧
                hand=-1 #恢复使用手的限制
                if visible<=density:
                    #输出结果
                    ret = '{"type":"Single","lane":'+str(lane)+',"beat":'+str(beat)+'}'
        isSlide=False
        isSlides=False
        beat=beat+4/(float(self.beat))
        return ret