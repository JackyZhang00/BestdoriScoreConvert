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

def getParameter():
    para = {"hand":hand,"isSlide":isSlide,"isSlides":isSlides,"density":density,"mindistence":mindistence,"slideMinDistence":slideMinDistence,
            "slideStep":slideStep,"lineStep":lineStep,"isSlideStatic":isSlideStatic}
    # tup = (hand,isSlide,isSlides,density,mindistence,slideMinDistence,slideStep,lineStep,isSlideStatic)
    return para

def set_hand(newHand):
    '''
    设置手位置，其中-1表示不指定，0表示左手，1表示右手
    '''
    global hand
    if newHand in [-1,0,1]:
        hand = newHand
    else:
        raise ValueError("非-1/0/1！")
    
def set_isSlide(new):
    global isSlide
    if isinstance(new,bool):
        isSlide = new
    else:
        raise ValueError("非布尔值！")
    
def set_isSlides(new):
    global isSlides
    if isinstance(new,bool):
        isSlides = new
    else:
        raise ValueError("非布尔值！")

class Score(object):
    def __init__(self):
        self.output = []
        self.lane = []
        
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
        add = note.add()
        if add != None:
            self.output.append(add)

    def setLane(self,lane):
        '''
        设置当前音符的位置
        '''
        self.lane = lane

    def getLane(self):
        '''
        获取当前谱面最后一个音符的轨道位置
        '''
        return self.lane

class Beat(Note):
    '''
    普通按键
    '''
    def __init__(self,beat,*lane):
        self.beat = beat
        self.hasLane = False
        if len(lane) != 0:
            self.lane = lane
            self.hasLane = True
    def add(self):
        global hand,density,isSlide,isSlides,beat
        visible=random.random()
        if not isSlides: #如果上一个不是双押长条
            if not self.hasLane:
                if isSlide: #如果上一个为长条
                    if hand==0: #长条为左手
                        lane=random.randint(min(slane+slideMinDistence,6),6) #键的位置在右侧
                    elif hand==1:#长条为右手
                        lane=random.randint(0,max(slane-slideMinDistence,0)) #键的位置在左侧
                    hand=-1 #恢复使用手的限制
                else: #如果上一个不是长条
                    lane=random.randint(0,6)
            else:
                lane = self.lane[0]
            if visible<=density:
                print("beat="+str(beat))
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
        ret = '{"beat":'+str(beat)+',"type":"BPM","bpm":'+str(self.bpm)+'}'
        return ret

class Rest(Note):
    '''
    休止符
    '''
    def __init__(self,beat):
        self.beat = beat
    def add(self):
        global beat
        beat=beat+4/(float(self.beat))

class Flick(Note):
    '''
    单划键
    '''
    def __init__(self,beat,*lane):
        self.beat = beat
        self.hasLane = False
        if len(lane) != 0:
            self.lane = lane
            self.hasLane = True
    def add(self):
        global beat,density
        if self.hasLane:
            lane = self.lane[0]
        else:
            lane=random.randint(0,6)
        visible=random.random()
        if visible<=density:
            ret = '{"type":"Single","lane":'+str(lane)+',"beat":'+str(beat)+',"flick":true}'
        beat=beat+4/(float(self.beat))
        return ret
    
class SingleFlick(Note):
    '''
    单键+划键, 若指定轨道参数，则第一个为蓝键轨道，第二个为粉键轨道
    '''
    def __init__(self,beat,*lane):
        self.beat = beat
        self.hasLane = False
        if len(lane) not in [0,1]:
            self.lane = lane
            self.hasLane = True
    def add(self):
        global hand,beat,isSlides,isSlide,mindistence,density,slideMinDistence #声明全局变量hand
        if self.hasLane:
            lane1 = self.lane[0]
            lane2 = self.lane[1]
        else:
            lane1=random.randint(0,6) #第一个键
            lane2=random.randint(0,6) #第二个键
        visible=random.random()

        if not isSlides: #判断上一个是否为双押长条，如果是则跳过
            #判断上一个是否为长条形
            if not isSlide:
                while abs(lane2-lane1)<mindistence and not self.hasLane:
                    lane1=random.randint(0,6)
                    lane2=random.randint(0,6) #若两个键距离不够，重新生成
                if visible<=density:
                    ret = '{"type":"Single","lane":'+str(lane1)+',"beat":'+str(beat)+'},'
                    ret = ret + '{"type":"Single","lane":'+str(lane2)+',"beat":'+str(beat)+',"flick":true}'
            #如果上一个为长条形，则与普通划键一样
            if isSlide:
                if self.hasLane:
                    lane = self.lane[0]
                else:
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
    def __init__(self,beat,*lane):
        self.beat = beat
        self.hasLane = False
        if len(lane) not in [0,1]:
            self.lane = lane
            self.hasLane = True
    def add(self):
        global hand,beat,isSlide,isSlides,density,slideMinDistence,mindistence #声明全局变量hand
        visible=random.random()
        if not isSlides: #判断上一个是否为双押长条

            #判断上一个是否为长条形
            if not isSlide:
                if self.hasLane:
                    lane1 = self.lane[0]
                    lane2 = self.lane[1]
                else:
                    lane1=random.randint(0,6) #第一个键
                    lane2=random.randint(0,6) #第二个键
                while abs(lane2-lane1)<mindistence and not self.hasLane:
                    lane1=random.randint(0,6)
                    lane2=random.randint(0,6) #若两个键相同，重新生成
                if visible<=density:
                    #输出结果
                    ret = '{"type":"Single","lane":'+str(lane1)+',"beat":'+str(beat)+'}'
                    ret = ret + ',{"type":"Single","lane":'+str(lane2)+',"beat":'+str(beat)+'}'
            #如果上一个为长条形，则于普通键一样
            if isSlide:
                if self.hasLane:
                    lane = self.lane[0]
                else:
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
        self.range = []
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
            self.range.append(slane)
        step=random.randint(-lineStep,lineStep)
        slane=slane+step
        while slane>5 or slane<1:
            slane=slane-step
            step=random.randint(-lineStep,lineStep)
            slane=slane+step
        if visible<=density:
            ret = ret + ',{"beat":'+str(beat+4/(float(self.beat)))+',"lane":'+str(slane)+'}]}'
            self.range.append(slane)
        beat=beat+4/(float(self.beat))
        isSlide=True #标记为长条
        self.range.sort()
        return ret
    def getLaneRange(self):
        '''
        返回绿条轨道范围，返回值为列表，第一项为左侧边界轨道，第二项为右侧边界轨道
        '''
        return self.range
class Slide(Note):
    '''
    单划动绿条
    '''
    def __init__(self,beats):
        self.beats = beats
        self.range = []
    def add(self):
        global beat,hand,slane
        visible=random.random()
        '''滑动长条，传入参数为音符列表'''
        if hand==-1: #若没有限制使用手，则随意生成
            slane=random.randint(0,6)
            if slane>=0 and slane<3:
                hand=0 #若长条在左侧（或中间），则使用左手(0)
            elif slane>3 and slane<=6:
                hand=1 #右手(1)
            elif slane==3:
                hand=random.randint(0,1)
        elif hand==0: #若上一个长条为左手
            slane=random.randint(min(slane+slideMinDistence,6),6) #该长条位置在右侧（右手）
            hand=1
        elif hand==1: #若上一个长条为右手
            slane=random.randint(0,max(slane-slideMinDistence,0)) #该长条位置在左侧
            hand=0
        #输出长条
        tempOut=[]
        ret = '{"type":"Slide","connections":['
        ret = ret + '{"beat":'+str(beat)+',"lane":'+str(slane)+'}'
        self.range.append(slane)
        for k in self.beats:
            beat=beat+4/(int(k))
            #判断是否在同一位置
            if isSlideStatic:
                step=random.randint(-slideStep,slideStep)
            else:
                step=random.randint(-slideStep,slideStep)
                while step==0:
                    step=random.randint(-slideStep,slideStep)
                
            slane=slane+step
            #调整位置，避免出界
            while slane>6 or slane<0:
                slane=slane-step
                if isSlideStatic:
                    step=random.randint(-slideStep,slideStep)
                else:
                    step=random.randint(-slideStep,slideStep)
                    while step==0:
                        step=random.randint(-slideStep,slideStep)
                slane=slane+step
                #slane=5
            #elif slane<0:
                #slane=1
                    
            #if slane>=0 and slane<=3:
                #hand=0
            #elif slane>3 and slane<=6:
                #hand=1
            ret = ret + ',{"beat":'+str(beat)+',"lane":'+str(slane)+'}'
            self.range.append(slane)
        ret = ret + ']}'
        if visible<=density:
            ret = ret
        else:
            ret = ""
        self.range.sort()
        return ret
    def getLaneRange(self):
        '''
        返回绿条轨道范围，返回值为列表，第一项为左侧边界轨道，第二项为右侧边界轨道
        '''
        ret = []
        ret.append(self.range[0])
        ret.append(self.range[-1])
        return ret
    
class DoubleSlide(Note):
    def __init__(self,beats):
        self.beats = beats
    def add(self):
        global beat,hand
        visible=random.random()
        tempOutL=[] #左侧
        tempOutR=[] #右侧
        slaneL=random.randint(0,3)
        slaneR=random.randint(slaneL+slideMinDistence,6)
            

        tempOutL.append('{"type":"Slide","connections":[')
        tempOutL.append('{"beat":'+str(beat)+',"lane":'+str(slaneL)+'}')
        tempOutR.append(',{"type":"Slide","connections":[')
        tempOutR.append('{"beat":'+str(beat)+',"lane":'+str(slaneR)+'}')
        for k in self.beats:
            beat=beat+4/(int(k))
            #判断是否在同一位置
            if isSlideStatic:
                step=random.randint(-slideStep,slideStep)
            else:
                step=random.randint(-slideStep,slideStep)
                while step==0:
                    step=random.randint(-slideStep,slideStep)
            slaneL=slaneL+step
            while slaneL<0 or slaneL>=slaneR:
                slaneL=slaneL-step
                #判断是否在同一位置
                if isSlideStatic:
                    step=random.randint(-slideStep,slideStep)
                else:
                    step=random.randint(-slideStep,slideStep)
                    while step==0:
                        step=random.randint(-slideStep,slideStep)
                slaneL=slaneL+step

            #判断是否在同一位置
            if isSlideStatic:
                step=random.randint(-slideStep,slideStep)
            else:
                step=random.randint(-slideStep,slideStep)
                while step==0:
                    step=random.randint(-slideStep,slideStep)
                        
            slaneR=slaneR+step
            while slaneR>6:
                slaneR=slaneR-step
                #判断是否在同一位置
                if isSlideStatic:
                    step=random.randint(-slideStep,slideStep)
                else:
                    step=random.randint(-slideStep,slideStep)
                    while step==0:
                        step=random.randint(-slideStep,slideStep)
                slaneR=slaneR+step
            while slaneR-slaneL<slideMinDistence and slaneR<6: #当右侧滑条与左侧滑条距离很近，且右侧不在边缘时
                slaneR=slaneR-step
                #判断是否在同一位置
                if isSlideStatic:
                    step=random.randint(-slideStep,slideStep)
                else:
                    step=random.randint(-slideStep,slideStep)
                    while step==0:
                        step=random.randint(-slideStep,slideStep)
                slaneR=min(slaneR+step,6)
            tempOutL.append(',{"beat":'+str(beat)+',"lane":'+str(slaneL)+'}')
            tempOutR.append(',{"beat":'+str(beat)+',"lane":'+str(slaneR)+'}')

        tempOutL.append(']}')
        tempOutR.append(']}')
        if visible<=density:
            ret = "".join(tempOutL)
            ret = ret + "".join(tempOutR)
        return ret