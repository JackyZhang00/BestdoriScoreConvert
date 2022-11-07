import random
import json
from Note import Note

isSlide=False
isSlides=False
hand=-1 #使用手无限制
beat=0
#output=[]
#fw=open("OUTCAR.txt",'w')
#fr=open("TEMP.txt",'r')
#test=fr.read()
#scores=test.split()
slane=random.randint(0,6)
#length=len(scores)
with open('config.json',encoding='utf-8') as a:
    result = json.load(a)
    mindistence = result.get("mindistence")
    slideMinDistence = result.get("slideMinDistence")
    slideStep = result.get("slideStep")
    lineStep = result.get("lineStep")
    isSlideStatic = result.get("isSlideStatic")

#以下内容已设置json文件------------
#mindistence=3 #【可修改】双押最短距离，0表示双押可能重叠，1表示双押可能紧挨，一般建议设置为3，最大为6表示双押一定在两侧
#slideMinDistence=2 #【可修改】长条之间最短距离（包括长条尾部与普通键），距离为0表示两个相邻长条可能重叠，
                    #1表示两个长条紧挨，最大为6表示两侧。（若超过
                    #极限则以边界为准）
#slideStep=1 #【可修改】滑动长条中间音符最大步进
#lineStep=2 #【可修改】长直条两端跨度，0表示只有竖直，边界不考虑
#isSlideStatic=False #【可修改】是否允许滑动长条的音符在同一位置，True表示允许，False表示不允许（边界不考虑）
#以上内容已设置json文件-----------
density=1 #【可修改】音符数量密度，0-1之间，数值越小则音符数量越少，难度越低

class Score(object):
    def __init__(self):
        self.output = []
        
    def getScore(self):
        #print('[',file=fw)
        #print('{"type":"BPM","bpm":'+str(bpm)+',"beat":0},',file=fw)
        #print(",".join(self.output),file=fw)
        #print(']',file=fw)
        ret = '[' + ",".join(self.output) + ']'
        #fr.close()
        #fw.close()
        return ret
        
    def addNote(self,note):
        self.output.append(note.add())

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


class BPM(Note):
    '''
    BPM标识
    '''
    def __init__(self,bpm):
        self.bpm = bpm
    def add(self):
        global beat
        ret = '{"type":"BPM","bpm":'+str(self.bpm)+',"beat":'+str(beat)+'}'
        return ret

class Rest(Note):
    '''
    休止符
    '''
    def __init__(self,beat):
        self.beat = beat
    def add(self):
        beat=beat+4/(float(self.beat))

class Flick(Note):
    '''
    单划键
    '''
    def __init__(self,beat):
        self.beat = beat
    def add(self):
        global beat,density
        lane=random.randint(0,6)
        visible=random.random()
        if visible<=density:
            ret = '{"type":"Single","lane":'+str(lane)+',"beat":'+str(beat)+',"flick":true}'
        beat=beat+4/(float(self.beat))
        return ret
    
class SingleFlick(Note):
    '''
    单键+划键
    '''
    def __init__(self,beat):
        self.beat = beat
    def add(self):
        global hand,beat,isSlides,isSlide,mindistence,density,slideMinDistence #声明全局变量hand
        lane1=random.randint(0,6) #第一个键
        lane2=random.randint(0,6) #第二个键
        visible=random.random()

        if not isSlides: #判断上一个是否为双押长条，如果是则跳过
            #判断上一个是否为长条形
            if not isSlide:
                while abs(lane2-lane1)<mindistence:
                    lane1=random.randint(0,6)
                    lane2=random.randint(0,6) #若两个键距离不够，重新生成
                if visible<=density:
                    ret = '{"type":"Single","lane":'+str(lane1)+',"beat":'+str(beat)+'}'
                    ret = ret + '{"type":"Single","lane":'+str(lane2)+',"beat":'+str(beat)+',"flick":true}'
            #如果上一个为长条形，则与普通划键一样
            if isSlide:
                if hand==0: #长条为左手
                    lane=random.randint(min(slane+slideMinDistence,6),6) #键的位置在右侧
                elif hand==1:#长条为右手
                    lane=random.randint(0,max(slane-slideMinDistence,0)) #键的位置在左侧
                hand=-1 #恢复使用手的限制
                if visible<=density:
                    ret = '{"type":"Single","lane":'+str(lane)+',"beat":'+str(beat)+',"flick":true}'
        isSlide=False
        isSlides=False
        beat=beat+4/(float(self.beat))            
        return ret
    
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
                    ret = ret + ',{"type":"Single","lane":'+str(lane2)+',"beat":'+str(beat)+'}'
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
    

class LineSlide(Note):
    '''
    长直条
    '''
    def __init__(self,beat):
        self.beat = beat
    def add(self):
        global hand,slane,slideMinDistence,density,beat,lineStep,isSlide
        visible=random.random()

        if hand==-1: #若没有限制使用手，则随意生成
            slane=random.randint(0,6)
            if slane>=0 and slane<3:
                hand=0 #若长条在左侧，则使用左手(0)
            elif slane>3 and slane<=6:
                hand=1 #右手(1)
            if slane==3:#若在中间，则随机选择左右
                hand=random.randint(0,1)
        elif hand==0: #若上一个长条为左手
            leftBond=min(slane+slideMinDistence,6)
            slane=random.randint(leftBond,6) #该长条位置在右侧（右手）
            hand=1
        elif hand==1: #若上一个长条为右手
            rightBond=max(slane-slideMinDistence,0)
            slane=random.randint(0,rightBond) #该长条位置在左侧
            hand=0
        #输出长条
        if visible<=density:  
            ret = '{"type":"Slide","connections":[{"beat":'+str(beat)+',"lane":'+str(slane)+'}'
        step=random.randint(-lineStep,lineStep)
        slane=slane+step
        while slane>5 or slane<1:
            slane=slane-step
            step=random.randint(-lineStep,lineStep)
            slane=slane+step
        if visible<=density:
            ret = ret + '{"beat":'+str(beat+4/(float(self.beat)))+',"lane":'+str(slane)+'}]}'
        beat=beat+4/(float(self.beat))
        isSlide=True #标记为长条
        return ret