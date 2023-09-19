# 七酱使用相关说明
## 为什么要制作这样一个工具？
在制作BanG Dream自制谱（特别是FULL谱的时候），通常是拿到一个谱面（五线谱等音乐谱面），然后通过相关编辑器进行节奏的编辑。而我们制作这一工具（七酱），就是为了将这一转化过程实现**自动化**。

在使用该工具的时候，**不必考虑谱面按键的位置，只需考虑节奏即可**。因此，我们将制作自制谱的思路调整为如下方法：
- 根据已有音乐制作音乐谱面（五线谱等）
- 使用该工具生成BanG Dream自制谱面（bestdori格式）
- 对谱面人工进行进一步修改

## 设计计划
目前拟定的设计思路如下：
- [X] 完成基本框架
- [X] 实现滑条与双押滑条类的设计
- [X] 实现文本输入与文本输出
- [X] 实现延音的输入
- [ ] 实现双押粉键的设计
- [ ] 实现绿条+粉键的设计
- [ ] 实现三连音等输入
- [ ] 实现交互
- [ ] 实现特定节奏（双手交互快捷方式）
- [ ] ……
## 如何使用七酱？


### 关于`config.json`的参数说明
你可以通过相关参数的设定实现对全局参数的设定！包括如下参数：
- `"mindistence"` 双押最短距离，0表示双押可能重叠，1表示双押可能紧挨，一般建议设置为3，最大为6表示双押一定在两侧
- `"slideMinDistence"` 长条之间最短距离（包括长条尾部与普通键），距离为0表示两个相邻长条可能重叠，1表示两个长条紧挨，最大为6表示两侧。（若超过极限则以边界为准）
- `"slideStep"` 滑动长条中间音符最大步进
- `"lineStep"` 长直条两端跨度，0表示只有竖直，边界不考虑
- `"isSlideStatic"` 是否允许滑动长条的音符在同一位置，true表示允许，false表示不允许（边界不考虑）

### 如何使用NanaChan？

*由于受到我专业的影响*，基本使用方法如下：

- 将节奏信息以`INCAR.txt`文件保存，其中每一个音符之间以空格间隔，可以使用中括号表示将某一段在当前地方重复两遍。

一个音符的基本指令为`[音符类型][节奏]`，目前已经实现的类型有：
  - 普通音符，不需要输入类型，只需要有节奏即可。
  - 普通双押：音符类型指令为`D`（Double single）
  - 速度：音符类型指令为`b`(BPM)。注意，速度后面的数字表示bpm数值，不代表节奏信息
  - 休止符：音符类型指令为`r`(rest)
  - 单粉键：音符类型指令为`f`(flick)
  - 单键+粉键：音符类型为`sf` 或 `fs`(singleflick)
  - 长绿条：音符类型为`l`(line)
  - 划动绿条：音符类型为`s`(slide)
  - 双押划动绿条：音符类型为`S`(double Slide)

节奏为数字，目前已经实现的有：
  - 基本音符（如二分、四分、八分、十六分等），使用节奏指令分别为`2`,`4`,`8`,`16`等。
  - 附点音符（使用`.`表示）
  - 延音（使用`-`表示）

执行`main.py`程序，输出文件为`OUTCAT.txt`

### 如何自定义交互组合

*注：当前方式仅为临时方式，后续可能会进行重构*

使用基本元素（上述已经完成的元素），在`main.py`当中进行组合，必要时可调用函数`getParameter()`获得相关参数信息（通常情况可能需要用到的是`hand`,`isSlide`,`isSlides`等）

同时，在进行设计时，也可以根据需要使用函数`set_hand()`,`set_isSlide()`和`set_isSlides()`函数对相关参数进行修改。

在`main.py`当中，请在相关位置编写程序，基本框架为
```Python
elif command == [代码指令]:
  程序部分
```
