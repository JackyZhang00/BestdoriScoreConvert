import re
from Score import *

with open('INCAR.txt','r') as file:
    string = file.read()
    # print(string)

# 预处理（使用中括号表示重复）
print("正在准备预处理中……")
pattern = r"\((.*?)\)" # 匹配被小括号括起来的部分

result = re.findall(pattern, string) # 查找所有匹配的结果
for match in result:
    string = string.replace(f"({match})", f"{match} {match}") # 将匹配到的部分重复两遍

with open('TEMPCAR','w') as file:
    file.write(string)

# # 处理附点音符

# lst = []
# lists = string.split()
# for i in lists:
#     if '.' in i:
#         note = i[:-1]
#         if i[0].isdigit: # 如果是普通音符
#             lst.append(i[:-1])
#             lst.append("r"+float(i[:-1])/2)

#         pattern = "([a-zA-Z]+)([*[0-9]+]*)"
#         result = re.match(pattern,i)
#         command = result.group(1)
#         beat = result.group(2)
#         lst.append(command)

print("预处理成功！")


# 是否继续生成
try:
    contcar = open('CONTCAR.txt','r')
    print("已有输出文件，谱面将在此基础上继续生成")
    compcar = open('COMPCAR','r')

except FileNotFoundError:
    pass


print("正在读取谱面文件")

with open('TEMPCAR','r') as file:
    string = file.read()
    string = string.split()

print(string)

pattern = "([a-zA-Z]+)([*[0-9]+]*)"

s = Score()
for i in string:
    if i.isdigit():
        s.addNote(Beat(float(i)))
    else:
        result = re.match(pattern, i)
        command = result.group(1)
        beat = result.group(2)
        print(beat)
        if command == 'b':
            s.addNote(BPM(float(beat)))
        elif command == 'D':
            s.addNote(DSingle(float(beat)))
        elif command == 'r':
            s.addNote(Rest(float(beat)))
        elif command == 'f':
            s.addNote(Flick(float(beat)))
        elif command == 'sf' or command == 'fs':
            s.addNote(SingleFlick(float(beat)))
        elif command == 'l':
            s.addNote(LineSlide(float(beat)))
        elif command == 's':
            beats = eval(i[1:])
            s.addNote(Slide(beats))
        elif command == 'S':
            beats = eval(i[1:])
            s.addNote(DoubleSlide(beats))
    # print(s.getScore())

# print(s.getScore)

with open('OUTCAR.txt','w') as file:
    print(s.output)
    file.write(s.getScore())

print("Bestdori谱面文件已生成为OUTCAR.txt文件！")
