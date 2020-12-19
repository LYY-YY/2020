import sys
import xlrd as xd
import numpy as np
import pyecharts.options as opts    # for 散点图
import pylab as pl
import heapq    # for max值
# 导入txt的数据
d1 = []
with open(r"F:\大三上\机器学习\data1.txt", 'r') as f:
    for line in f:
        d1.append(list(line.strip('\n').split(',')))

# 导入xlsx的数据
data = xd.open_workbook ('F:/大三上/机器学习/data2.xlsx')  # 打开excel表所在路径
sheet = data.sheet_by_name('Sheet1')  # 读取数据，以excel表名来打开
d2 = []
for r in range(sheet.nrows):  # 将表中数据按行逐步添加到列表中，最后转换为list结构
    data1 = []
    for c in range(sheet.ncols):
        data1.append(sheet.cell_value(r, c))
    d2.append(list(data1))

# 将d2中的ID与d1一致化
for n in range(1, len(d2)):
    d2[n][0] = str(int(d2[n][0]) + 202000)

# 比对两个数据源的数据进行合并，当数据不一致时以txt数据源d1为准
d = d1

# 把d1,d2的ID存放在另外的列表中
d1_ID = []
d2_ID = []
for x in range(len(d1)):
    d1_ID.append(d1[x][0])
for y in range(len(d2)):
    d2_ID.append(d2[y][0])

# 去除重复的ID
Delete_Index = []
for p in range(1, len(d)):
    if d[p][0] == d[p - 1][0]:
         Delete_Index.append(p) # 保存重复的ID的下标

sign = 0    # 记下已删除的行的个数，当已删除d中的一行时，下标值会有变化，实际的下标值为原本的Delete_Index加上标志sign
for q in range(len(Delete_Index)):  # 删除重复的ID
    del d[Delete_Index[q] - sign]
    sign += 1

# 定义一个函数查判断某id是否在d1中
def FindID_d1(ID):
    if ID in d1_ID:
        return 1
    else:
        return 0


# 定义一个函数判断某ID是否在d2，有则返回下标
def FindID_d2(ID):
    if ID in d2_ID:
        for r in range(len(d2_ID)):
            if ID == d2_ID[r]:
                return r
    else:
        return -1


# 把d1数据为空的地方按照d2补充上
for i in range(1, len(d)):
    for j in range(1, len(d[0])):
        if d[i][j] == '':
            tmp_index =FindID_d2(d[i][0])
            if tmp_index >= 0:
                d[i][j] = d2[tmp_index][j]


# 把d2不在d1中的ID加入到d1中
for y in range(len(d2)):
    if FindID_d1(d2_ID[y]) == 0:
        d.append(list(d2[y]))

for n in range(1, len(d)):
    for m in range(1, len(d[0])):
        if d[n][3] == 'girl':  # 如果性别显示为girl则改为female
                d[n][3] = 'female'
        if d[n][3] == 'boy':
                d[n][3] = 'male'
        if float(d[n][4]) > 2:  # 如果身高为三位数则改为小数形式
            d[n][4] = float(d[n][4])/100

del d[0]    # 删除第一行，只剩下数据
d.sort(key = lambda x: x[0], reverse=False)  # 按照ID排序

for line in d:      # 输出最后结果
    print(line)


# 把最终结果写入到Final_Data.xlsx中
output = open('F:/大三上/机器学习/Final_Data.xlsx', 'w', encoding='gbk')
output.write('ID\tName\tCity\tGender\tHeight\tC1\tC2\tC3\tC4\tC5\tC6\tC7\tC8\tC9\tC10\tConstitution\n')
for i in range(len(d)):
    for j in range(len(d[0])):
        output.write(str(d[i][j]))  # write函数不能写int类型的参数，所以使用str()转化
        output.write('\t')  # 相当于Tab一下，换一个单元格
    output.write('\n')    # 写完一行立马换行
output.close()


# 两个数据源合并后读入内存，并统计：
# 1. 学生中家乡在Beijing的所有课程的平均成绩。
print("--------------------------------------------------------")
print("1. 学生中家乡在Beijing的所有课程的平均成绩。")
Score_tempC1 = []
Score_tempC2 = []
Score_tempC3 = []
Score_tempC4 = []
Score_tempC5 = []
Score_tempC6 = []
Score_tempC7 = []
Score_tempC8 = []
Score_tempC9 = []
for i in range(len(d)):
    for j in range(len(d[0])):
        if d[i][2] == 'Beijing':
            Score_tempC1.append(d[i][5])
            Score_tempC2.append(d[i][6])
            Score_tempC3.append(d[i][7])
            Score_tempC4.append(d[i][8])
            Score_tempC5.append(d[i][9])
            Score_tempC6.append(d[i][10])
            Score_tempC7.append(d[i][11])
            Score_tempC8.append(d[i][12])
            Score_tempC9.append(d[i][13])
# 去掉列表为空的元素
Score_C1 = list(filter(None, Score_tempC1))
Score_C2 = list(filter(None, Score_tempC2))
Score_C3 = list(filter(None, Score_tempC3))
Score_C4 = list(filter(None, Score_tempC4))
Score_C5 = list(filter(None, Score_tempC5))
Score_C6 = list(filter(None, Score_tempC6))
Score_C7 = list(filter(None, Score_tempC7))
Score_C8 = list(filter(None, Score_tempC8))
Score_C9 = list(filter(None, Score_tempC9))
# 输出平均成绩
sum_C1 = 0.0
sum_C2 = 0.0
sum_C3 = 0.0
sum_C4 = 0.0
sum_C5 = 0.0
sum_C6 = 0.0
sum_C7 = 0.0
sum_C8 = 0.0
sum_C9 = 0.0
for m in range(len(Score_C1)):  # 计算C1的总成绩
    sum_C1 += float(Score_C1[m])
for m in range(len(Score_C2)):  # 计算C2的总成绩
    sum_C2 += float(Score_C2[m])
for m in range(len(Score_C3)):  # 计算C3的总成绩
    sum_C3 += float(Score_C3[m])
for m in range(len(Score_C4)):  # 计算C4的总成绩
    sum_C4 += float(Score_C4[m])
for m in range(len(Score_C5)):  # 计算C5的总成绩
    sum_C5 += float(Score_C5[m])
for m in range(len(Score_C6)):  # 计算C6的总成绩
    sum_C6 += float(Score_C6[m])
for m in range(len(Score_C7)):  # 计算C7的总成绩
    sum_C7 += float(Score_C7[m])
for m in range(len(Score_C8)):  # 计算C8的总成绩
    sum_C8 += float(Score_C8[m])
for m in range(len(Score_C9)):  # 计算C9的总成绩
    sum_C9 += float(Score_C9[m])
print("学生中家乡在Beijing的所有课程的平均成绩.")
print("课程C1的平均成绩为：", sum_C1/len(Score_C1))
print("课程C2的平均成绩为：", sum_C2/len(Score_C2))
print("课程C3的平均成绩为：", sum_C3/len(Score_C3))
print("课程C4的平均成绩为：", sum_C4/len(Score_C4))
print("课程C5的平均成绩为：", sum_C5/len(Score_C5))
print("课程C6的平均成绩为：", sum_C6/len(Score_C6))
print("课程C7的平均成绩为：", sum_C7/len(Score_C7))
print("课程C8的平均成绩为：", sum_C8/len(Score_C8))
print("课程C9的平均成绩为：", sum_C9/len(Score_C9))

# 2. 学生中家乡在广州，课程1在80分以上，且课程9在9分以上的男同学的数量
print("--------------------------------------------------------")
print("2. 学生中家乡在广州，课程1在80分以上，且课程9在9分以上的男同学的数量")
count = 0
for i in range(len(d)):
    for j in range(len(d[0])):
        if d[i][2] == 'Guangzhou' and d[i][3] == 'male' and float(d[i][5]) > 80 and float(d[i][13]) > 9:
            count += 1
print("学生中家乡在广州，课程1在80分以上，且课程9在9分以上的男同学的数量:", count)

# 3. 比较广州和上海两地女生的平均体能测试成绩，哪个地区的更强些？
# bad/general/good/excellent分别为1分/2分/3分/4分
print("--------------------------------------------------------")
print("3. 比较广州和上海两地女生的平均体能测试成绩，哪个地区的更强些？")
Constitution_SH = 0.0  # 上海女生体能成绩
Constitution_GZ = 0.0  # 广州女生体能成绩
count_SH = 0        # 上海女生人数
count_GZ = 0        # 广州女生人数
for i in range(len(d)):
    for j in range(len(d[0])):
        if d[i][2] == 'Shanghai' and d[i][3] == 'female':   # 按照条件筛选
            if d[i][15] != '':
                count_SH += 1
                if d[i][15] == 'bad':   # 不同的评价有不同的分数
                    Constitution_SH += 1
                if d[i][15] == 'general':
                    Constitution_SH += 2
                if d[i][15] == 'good':
                    Constitution_SH += 3
                if d[i][15] == 'excellent':
                    Constitution_SH += 4
        if d[i][2] == 'Guangzhou' and d[i][3] == 'female':
            if d[i][15] != '':
                count_GZ += 1
                if d[i][15] == 'bad':
                    Constitution_GZ += 1
                if d[i][15] == 'general':
                    Constitution_GZ += 2
                if d[i][15] == 'good':
                    Constitution_GZ += 3
                if d[i][15] == 'excellent':
                    Constitution_GZ += 4
print("上海女生体能平均成绩为：", Constitution_SH/count_SH)
print("广州女生体能平均成绩为：", Constitution_GZ/count_GZ)
if Constitution_SH/count_SH > Constitution_GZ/count_GZ:
    print("上海女生体能更强。")
elif Constitution_SH/count_SH < Constitution_GZ/count_GZ:
    print("广州女生体能更强。")
else:
    print("两个地区女生体能不分上下。")

# 4. 学习成绩和体能测试成绩，两者的相关性是多少？（九门课的成绩分别与体能成绩计算相关性）
print("--------------------------------------------------------")
print("4. 学习成绩和体能测试成绩，两者的相关性是多少？（九门课的成绩分别与体能成绩计算相关性）")
# 把体能测试成绩转化为数字表示的形式；bad/general/good/excellent分别为1分/2分/3分/4分
Constitution_Socre = []
for i in range(len(d)):
    if d[i][15] == 'bad':               
        Constitution_Socre.append(1)
    if d[i][15] == 'general':
        Constitution_Socre.append(2)
    if d[i][15] == 'good':
        Constitution_Socre.append(3)
    if d[i][15] == 'excellent':
        Constitution_Socre.append(4)
# 求协方差
ss_Constitution = 0.0   # 记录体能成绩的协方差
from numpy import *
mean_Constitution = mean(Constitution_Socre)
for j in range(len(Constitution_Socre)):    # 协方差公式，先计算和
    ss_Constitution += (Constitution_Socre[j] - mean_Constitution) * (Constitution_Socre[j] - mean_Constitution)
ss_Constitution = ss_Constitution/(len(Constitution_Socre) - 1)
print("体能成绩的协方差是：", ss_Constitution)
std_Constitution = ss_Constitution ** 0.5
print("体能成绩的标准差是：", std_Constitution)
Constitution_Socre1 = []    # 体能成绩数组B`
for m in range(len(Constitution_Socre)):
    Constitution_Socre1.append((Constitution_Socre[m] - mean_Constitution)/std_Constitution)

# 计算C1
C1_Score = []
for i in range(len(d)):
    if d[i][5] != '' and d[i][15] != '':  # 体能成绩有两处为空，要舍去
        C1_Score.append(float(d[i][5]))
# 求协方差
ss_C1 = 0.0
mean_C1 = mean(C1_Score)    # C1成绩的平均值
for i in range(len(C1_Score)):  # 协方差公式，先计算和
    ss_C1 += (C1_Score[i] - mean_C1) * (C1_Score[i] - mean_C1)
ss_C1 = ss_C1/(len(C1_Score) - 1)
std_C1 = ss_C1 ** 0.5
print("C1成绩的平均值是：", mean_C1)
print("C1成绩的协方差是：", ss_C1)
print("C1成绩的标准差是：", std_C1)
C1_Score1 = []
for m in range(len(C1_Score)):  # C1成绩数组C1`
    C1_Score1.append((C1_Score[m] - mean_C1)/std_C1)

# 体能 成绩数组和C1成绩数组的相关性
correlation_Con_C1 = 0.0
for m in range(len(Constitution_Socre1)):
    correlation_Con_C1 += Constitution_Socre1[m] * C1_Score[m]
print("C1和体能测试成绩的相关性是（C1*B)：", correlation_Con_C1)
print("********************************************")

# 计算C2
C2_Score = []
for i in range(len(d)):
    if d[i][6] != '' and d[i][15] != '':  # 体能成绩有两处为空，要舍去
        C2_Score.append(float(d[i][6]))
# 求协方差
ss_C2 = 0.0
mean_C2 = mean(C2_Score)    # C2成绩的平均值
for i in range(len(C2_Score)):  # 协方差公式，先计算和
    ss_C2 += (C2_Score[i] - mean_C2) * (C2_Score[i] - mean_C2)
ss_C2 = ss_C2/(len(C2_Score) - 1)
std_C2 = ss_C2 ** 0.5
print("C2成绩的平均值是：", mean_C2)
print("C2成绩的协方差是：", ss_C2)
print("C2成绩的标准差是：", std_C2)
C2_Score1 = []
for m in range(len(C2_Score)):  # C2成绩数组C2`
    C2_Score1.append((C2_Score[m] - mean_C2)/std_C2)

# 体能 成绩数组和C2成绩数组的相关性
correlation_Con_C2 = 0.0
for m in range(len(Constitution_Socre1)):
    correlation_Con_C2 += Constitution_Socre1[m] * C2_Score[m]
print("C2和体能测试成绩的相关性是（C2*B)：", correlation_Con_C2)
print("********************************************")

# 计算C3
C3_Score = []
for i in range(len(d)):
    if d[i][7] != '' and d[i][15] != '':  # 体能成绩有两处为空，要舍去
        C3_Score.append(float(d[i][7]))
# 求协方差
ss_C3 = 0.0
mean_C3 = mean(C3_Score)    # C3成绩的平均值
for i in range(len(C3_Score)):  # 协方差公式，先计算和
    ss_C3 += (C3_Score[i] - mean_C3) * (C3_Score[i] - mean_C3)
ss_C3 = ss_C3/(len(C3_Score) - 1)
std_C3 = ss_C3 ** 0.5
print("C3成绩的平均值是：", mean_C3)
print("C3成绩的协方差是：", ss_C3)
print("C3成绩的标准差是：", std_C3)
C3_Score1 = []
for m in range(len(C3_Score)):  # C3成绩数组C3`
    C3_Score1.append((C3_Score[m] - mean_C3)/std_C3)

# 体能 成绩数组和C3成绩数组的相关性
correlation_Con_C3 = 0.0
for m in range(len(Constitution_Socre1)):
    correlation_Con_C3 += Constitution_Socre1[m] * C3_Score[m]
print("C3和体能测试成绩的相关性是（C3*B)：", correlation_Con_C3)
print("********************************************")

# 因为C4成绩有一个为空，所以需要按照C4重新计算体能测试数组B`
# 把体能测试转de成绩化为数字表示的形式
Constitution_SocreA = []
for i in range(len(d)):
    if d[i][8] != '':
        if d[i][15] == 'bad':
            Constitution_SocreA.append(1)
        if d[i][15] == 'general':
            Constitution_SocreA.append(2)
        if d[i][15] == 'good':
            Constitution_SocreA.append(3)
        if d[i][15] == 'excellent':
            Constitution_SocreA.append(4)
# 求协方差
ss_ConstitutionA = 0.0   # 记录体能成绩的协方差
from numpy import *
mean_ConstitutionA = mean(Constitution_SocreA)
for j in range(len(Constitution_SocreA)):    # 协方差公式，先计算和
    ss_ConstitutionA += (Constitution_SocreA[j] - mean_ConstitutionA) * (Constitution_SocreA[j] - mean_ConstitutionA)
ss_ConstitutionA = ss_ConstitutionA/(len(Constitution_SocreA) - 1)
print("体能成绩的协方差是(按照C4重新计算后)：", ss_ConstitutionA)
std_ConstitutionA = ss_ConstitutionA ** 0.5
print("体能成绩的标准差是(按照C4重新计算后)：", std_ConstitutionA)
Constitution_SocreA1 = []    # 体能成绩数组B`
for m in range(len(Constitution_SocreA)):
    Constitution_SocreA1.append((Constitution_SocreA[m] - mean_ConstitutionA)/std_ConstitutionA)

# 计算C4
C4_Score = []
for i in range(len(d)):
    if d[i][8] != '' and d[i][15] != '':  # 体能成绩有两处为空，要舍去
        C4_Score.append(float(d[i][8]))
# 求协方差
ss_C4 = 0.0
mean_C4 = mean(C4_Score)    # C4成绩的平均值
for i in range(len(C4_Score)):  # 协方差公式，先计算和
    ss_C4 += (C4_Score[i] - mean_C4) * (C4_Score[i] - mean_C4)
ss_C4 = ss_C4/(len(C4_Score) - 1)
std_C4 = ss_C4 ** 0.5
print("C4成绩的平均值是：", mean_C4)
print("C4成绩的协方差是：", ss_C4)
print("C4成绩的标准差是：", std_C4)
C4_Score1 = []
for m in range(len(C4_Score)):  # C4成绩数组C4`
    C4_Score1.append((C4_Score[m] - mean_C4)/std_C4)

# 体能 成绩数组和C4成绩数组的相关性
correlation_Con_C4 = 0.0
for m in range(len(Constitution_SocreA1)):
    correlation_Con_C4 += Constitution_SocreA1[m] * C4_Score[m]
print("C4和体能测试成绩的相关性是（C4*B)：", correlation_Con_C4)
print("********************************************")

# 因为C5成绩有一个为空，所以需要按照C5重新计算体能测试数组B`
# 把体能测试转de成绩化为数字表示的形式
Constitution_SocreB = []
for i in range(len(d)):
    if d[i][9] != '':
        if d[i][15] == 'bad':
            Constitution_SocreB.append(1)
        if d[i][15] == 'general':
            Constitution_SocreB.append(2)
        if d[i][15] == 'good':
            Constitution_SocreB.append(3)
        if d[i][15] == 'excellent':
            Constitution_SocreB.append(4)
# 求协方差
ss_ConstitutionB = 0.0   # 记录体能成绩的协方差
from numpy import *
mean_ConstitutionB = mean(Constitution_SocreB)
for j in range(len(Constitution_SocreB)):    # 协方差公式，先计算和
    ss_ConstitutionB += (Constitution_SocreB[j] - mean_ConstitutionB) * (Constitution_SocreB[j] - mean_ConstitutionB)
ss_ConstitutionB = ss_ConstitutionB/(len(Constitution_SocreB) - 1)
print("体能成绩的协方差是(按照C5重新计算后)：", ss_ConstitutionB)
std_ConstitutionB = ss_ConstitutionB ** 0.5
print("体能成绩的标准差是(按照C5重新计算后)：", std_ConstitutionB)
Constitution_SocreB1 = []    # 体能成绩数组B`
for m in range(len(Constitution_SocreB)):
    Constitution_SocreB1.append((Constitution_SocreB[m] - mean_ConstitutionB)/std_ConstitutionB)

# 计算C5
C5_Score = []
for i in range(len(d)):
    if d[i][9] != '' and d[i][15] != '':  # 体能成绩有两处为空，要舍去
        C5_Score.append(float(d[i][9]))
# 求协方差
ss_C5 = 0.0
mean_C5 = mean(C5_Score)    # C5成绩的平均值
for i in range(len(C5_Score)):  # 协方差公式，先计算和
    ss_C5 += (C5_Score[i] - mean_C5) * (C5_Score[i] - mean_C5)
ss_C5 = ss_C5/(len(C5_Score) - 1)
std_C5 = ss_C5 ** 0.5
print("C5成绩的平均值是：", mean_C5)
print("C5成绩的协方差是：", ss_C5)
print("C5成绩的标准差是：", std_C5)
C5_Score1 = []
for m in range(len(C5_Score)):  # C5成绩数组C5`
    C5_Score1.append((C5_Score[m] - mean_C5)/std_C5)

# 体能 成绩数组和C5成绩数组的相关性
correlation_Con_C5 = 0.0
for m in range(len(Constitution_SocreB1)):
    correlation_Con_C5 += Constitution_SocreB1[m] * C5_Score[m]
print("C5和体能测试成绩的相关性是（C5*B)：", correlation_Con_C5)
print("********************************************")

# 计算C6
C6_Score = []
for i in range(len(d)):
    if d[i][10] != '' and d[i][15] != '':  # 体能成绩有两处为空，要舍去
        C6_Score.append(float(d[i][10]))
# 求协方差
ss_C6 = 0.0
mean_C6 = mean(C6_Score)    # C6成绩的平均值
for i in range(len(C6_Score)):  # 协方差公式，先计算和
    ss_C6 += (C6_Score[i] - mean_C6) * (C6_Score[i] - mean_C6)
ss_C6 = ss_C6/(len(C6_Score) - 1)
std_C6 = ss_C6 ** 0.5
print("C6成绩的平均值是：", mean_C6)
print("C6成绩的协方差是：", ss_C6)
print("C6成绩的标准差是：", std_C6)
C6_Score1 = []
for m in range(len(C6_Score)):  # C6成绩数组C6`
    C6_Score1.append((C6_Score[m] - mean_C6)/std_C6)

# 体能 成绩数组和C6成绩数组的相关性
correlation_Con_C6 = 0.0
for m in range(len(Constitution_Socre1)):
    correlation_Con_C6 += Constitution_Socre1[m] * C6_Score[m]
print("C6和体能测试成绩的相关性是（C6*B)：", correlation_Con_C6)
print("********************************************")

# 计算C7
C7_Score = []
for i in range(len(d)):
    if d[i][11] != '' and d[i][15] != '':  # 体能成绩有两处为空，要舍去
        C7_Score.append(float(d[i][11]))
# 求协方差
ss_C7 = 0.0
mean_C7 = mean(C7_Score)    # C7成绩的平均值
for i in range(len(C7_Score)):  # 协方差公式，先计算和
    ss_C7 += (C7_Score[i] - mean_C7) * (C7_Score[i] - mean_C7)
ss_C7 = ss_C7/(len(C7_Score) - 1)
std_C7 = ss_C7 ** 0.5
print("C7成绩的平均值是：", mean_C7)
print("C7成绩的协方差是：", ss_C7)
print("C7成绩的标准差是：", std_C7)
C7_Score1 = []
for m in range(len(C7_Score)):  # C7成绩数组C7`
    C7_Score1.append((C7_Score[m] - mean_C7)/std_C7)

# 体能 成绩数组和C7成绩数组的相关性
correlation_Con_C7 = 0.0
for m in range(len(Constitution_Socre1)):
    correlation_Con_C7 += Constitution_Socre1[m] * C7_Score[m]
print("C7和体能测试成绩的相关性是（C7*B)：", correlation_Con_C7)
print("********************************************")

# 计算C8
C8_Score = []
for i in range(len(d)):
    if d[i][12] != '' and d[i][15] != '':  # 体能成绩有两处为空，要舍去
        C8_Score.append(float(d[i][12]))
# 求协方差
ss_C8 = 0.0
mean_C8 = mean(C8_Score)    # C8成绩的平均值
for i in range(len(C8_Score)):  # 协方差公式，先计算和
    ss_C8 += (C8_Score[i] - mean_C8) * (C8_Score[i] - mean_C8)
ss_C8 = ss_C8/(len(C8_Score) - 1)
std_C8 = ss_C8 ** 0.5
print("C8成绩的平均值是：", mean_C8)
print("C8成绩的协方差是：", ss_C8)
print("C8成绩的标准差是：", std_C8)
C8_Score1 = []
for m in range(len(C8_Score)):  # C8成绩数组C8`
    C8_Score1.append((C8_Score[m] - mean_C8)/std_C8)

# 体能 成绩数组和C8成绩数组的相关性
correlation_Con_C8 = 0.0
for m in range(len(Constitution_Socre1)):
    correlation_Con_C8 += Constitution_Socre1[m] * C8_Score[m]
print("C8和体能测试成绩的相关性是（C8*B)：", correlation_Con_C8)
print("********************************************")

# 计算C9
C9_Score = []
for i in range(len(d)):
    if d[i][13] != '' and d[i][15] != '':  # 体能成绩有两处为空，要舍去
        C9_Score.append(float(d[i][13]))
# 求协方差
ss_C9 = 0.0
mean_C9 = mean(C9_Score)    # C9成绩的平均值
for i in range(len(C9_Score)):  # 协方差公式，先计算和
    ss_C9 += (C9_Score[i] - mean_C9) * (C9_Score[i] - mean_C9)
ss_C9 = ss_C9/(len(C9_Score) - 1)
std_C9 = ss_C9 ** 0.5
print("C9成绩的平均值是：", mean_C9)
print("C9成绩的协方差是：", ss_C9)
print("C9成绩的标准差是：", std_C9)
C9_Score1 = []
for m in range(len(C9_Score)):  # C9成绩数组C9`
    C9_Score1.append((C9_Score[m] - mean_C9)/std_C9)

# 体能 成绩数组和C9成绩数组的相关性
correlation_Con_C9 = 0.0
for m in range(len(Constitution_Socre1)):
    correlation_Con_C9 += Constitution_Socre1[m] * C9_Score[m]
print("C9和体能测试成绩的相关性是（C9*B)：", correlation_Con_C9)
print("********************************************")
print("********************************************")


# 实验二
"""
# 1.请以课程1成绩为x轴，体能成绩为y轴，画出散点图。
from matplotlib import pyplot as plt
# 加上横轴与纵轴标签
plt.xlabel("C1_Score")
plt.ylabel("Constitution_Socre")
# 绘制散点图，并且加上标签
plt.scatter(C1_Score, Constitution_Socre, label="C1")
plt.legend()
plt.show()

# 2.以5分为间隔，画出课程1的成绩直方图。
Score_OF_C1 = []
for m in range(len(d)):  # 计算C1的总成绩
    if d[m][5] != '':
        Score_OF_C1.append(int(d[m][5]))
Score_OF_C1.sort()
print(Score_OF_C1)
print(len(Score_OF_C1))
bins = [67, 72, 77, 82, 87, 92]     #设置间隔
pl.hist(Score_OF_C1, bins)
pl.xlabel('C1_Score')
pl.ylabel('Number of C1_Score')
pl.title('Histogram of C1_Score')
pl.show()
"""

# 3.对每门成绩进行z-score归一化，得到归一化的数据矩阵。

# 计算C1的z-score
C1_z_score = []
for i in range(len(d)):
    if d[i][5] != '':
        C1_z_score.append(float(d[i][5]))
# 求协方差
ss_z_C1 = 0.0
mean_z_C1 = mean(C1_z_score)    # 成绩的平均值
for i in range(len(C1_z_score)):  # 协方差公式，先计算和
    ss_z_C1 += (C1_z_score[i] - mean_z_C1) * (C1_z_score[i] - mean_z_C1)
ss_z_C1 = ss_z_C1/(len(C1_z_score) - 1)
std_z_C1 = ss_z_C1 ** 0.5
print("C1成绩的平均值是：", mean_z_C1)
print("C1成绩的协方差是：", ss_z_C1)
print("C1成绩的标准差是：", std_z_C1)
C1_z_scoreFinal = []
for m in range(len(C1_z_score)):  
    C1_z_scoreFinal.append((C1_z_score[m] - mean_z_C1)/std_z_C1)
print("课程1归一化的数据矩阵为：")
for x in range(len(C1_z_scoreFinal)):
    print(C1_z_scoreFinal[x])
print("********************************************")


# 计算C2的z-score
C2_z_score = []
for i in range(len(d)):
    if d[i][6] != '':
        C2_z_score.append(float(d[i][6]))
# 求协方差
ss_z_C2 = 0.0
mean_z_C2 = mean(C2_z_score)    # 成绩的平均值
for i in range(len(C2_z_score)):  # 协方差公式，先计算和
    ss_z_C2 += (C2_z_score[i] - mean_z_C2) * (C2_z_score[i] - mean_z_C2)
ss_z_C2 = ss_z_C2/(len(C2_z_score) - 1)
std_z_C2 = ss_z_C2 ** 0.5
print("C2成绩的平均值是：", mean_z_C2)
print("C2成绩的协方差是：", ss_z_C2)
print("C2成绩的标准差是：", std_z_C2)
C2_z_scoreFinal = []
for m in range(len(C2_z_score)):  
    C2_z_scoreFinal.append((C2_z_score[m] - mean_z_C2)/std_z_C2)
print("课程2归一化的数据矩阵为：")
for x in range(len(C2_z_scoreFinal)):
    print(C2_z_scoreFinal[x])
print("********************************************")


# 计算C3的z-score
C3_z_score = []
for i in range(len(d)):
    if d[i][7] != '':
        C3_z_score.append(float(d[i][7]))
# 求协方差
ss_z_C3 = 0.0
mean_z_C3 = mean(C3_z_score)    # 成绩的平均值
for i in range(len(C3_z_score)):  # 协方差公式，先计算和
    ss_z_C3 += (C3_z_score[i] - mean_z_C3) * (C3_z_score[i] - mean_z_C3)
ss_z_C3 = ss_z_C3/(len(C3_z_score) - 1)
std_z_C3 = ss_z_C3 ** 0.5
print("C3成绩的平均值是：", mean_z_C3)
print("C3成绩的协方差是：", ss_z_C3)
print("C3成绩的标准差是：", std_z_C3)
C3_z_scoreFinal = []
for m in range(len(C3_z_score)):
    C3_z_scoreFinal.append((C3_z_score[m] - mean_z_C3)/std_z_C3)
print("课程3归一化的数据矩阵为：")
for x in range(len(C3_z_scoreFinal)):
    print(C3_z_scoreFinal[x])
print("********************************************")


# 计算C4的z-score
C4_z_score = []
for i in range(len(d)):
    if d[i][8] != '':
        C4_z_score.append(float(d[i][8]))
# 求协方差
ss_z_C4 = 0.0
mean_z_C4 = mean(C4_z_score)    # 成绩的平均值
for i in range(len(C4_z_score)):  # 协方差公式，先计算和
    ss_z_C4 += (C4_z_score[i] - mean_z_C4) * (C4_z_score[i] - mean_z_C4)
ss_z_C4 = ss_z_C4/(len(C4_z_score) - 1)
std_z_C4 = ss_z_C4 ** 0.5
print("C4成绩的平均值是：", mean_z_C4)
print("C4成绩的协方差是：", ss_z_C4)
print("C4成绩的标准差是：", std_z_C4)
C4_z_scoreFinal = []
for m in range(len(C4_z_score)):
    C4_z_scoreFinal.append((C4_z_score[m] - mean_z_C4)/std_z_C4)
print("课程4归一化的数据矩阵为：")
for x in range(len(C4_z_scoreFinal)):
    print(C4_z_scoreFinal[x])
print("********************************************")


# 计算C5的z-score
C5_z_score = []
for i in range(len(d)):
    if d[i][9] != '':
        C5_z_score.append(float(d[i][9]))
# 求协方差
ss_z_C5 = 0.0
mean_z_C5 = mean(C5_z_score)    # 成绩的平均值
for i in range(len(C5_z_score)):  # 协方差公式，先计算和
    ss_z_C5 += (C5_z_score[i] - mean_z_C5) * (C5_z_score[i] - mean_z_C5)
ss_z_C5 = ss_z_C5/(len(C5_z_score) - 1)
std_z_C5 = ss_z_C5 ** 0.5
print("C5成绩的平均值是：", mean_z_C5)
print("C5成绩的协方差是：", ss_z_C5)
print("C5成绩的标准差是：", std_z_C5)
C5_z_scoreFinal = []
for m in range(len(C5_z_score)):
    C5_z_scoreFinal.append((C5_z_score[m] - mean_z_C5)/std_z_C5)
print("课程5归一化的数据矩阵为：")
for x in range(len(C5_z_scoreFinal)):
    print(C5_z_scoreFinal[x])
print("********************************************")


# 计算C6的z-score
C6_z_score = []
for i in range(len(d)):
    if d[i][10] != '':
        C6_z_score.append(float(d[i][10]))
# 求协方差
ss_z_C6 = 0.0
mean_z_C6 = mean(C6_z_score)    # 成绩的平均值
for i in range(len(C6_z_score)):  # 协方差公式，先计算和
    ss_z_C6 += (C6_z_score[i] - mean_z_C6) * (C6_z_score[i] - mean_z_C6)
ss_z_C6 = ss_z_C6/(len(C6_z_score) - 1)
std_z_C6 = ss_z_C6 ** 0.5
print("C6成绩的平均值是：", mean_z_C6)
print("C6成绩的协方差是：", ss_z_C6)
print("C6成绩的标准差是：", std_z_C6)
C6_z_scoreFinal = []
for m in range(len(C6_z_score)):
    C6_z_scoreFinal.append((C6_z_score[m] - mean_z_C6)/std_z_C6)
print("课程6归一化的数据矩阵为：")
for x in range(len(C6_z_scoreFinal)):
    print(C6_z_scoreFinal[x])
print("********************************************")


# 计算C7的z-score
C7_z_score = []
for i in range(len(d)):
    if d[i][11] != '':
        C7_z_score.append(float(d[i][11]))
# 求协方差
ss_z_C7 = 0.0
mean_z_C7 = mean(C7_z_score)    # 成绩的平均值
for i in range(len(C7_z_score)):  # 协方差公式，先计算和
    ss_z_C7 += (C7_z_score[i] - mean_z_C7) * (C7_z_score[i] - mean_z_C7)
ss_z_C7 = ss_z_C7/(len(C7_z_score) - 1)
std_z_C7 = ss_z_C7 ** 0.5
print("C7成绩的平均值是：", mean_z_C7)
print("C7成绩的协方差是：", ss_z_C7)
print("C7成绩的标准差是：", std_z_C7)
C7_z_scoreFinal = []
for m in range(len(C7_z_score)):
    C7_z_scoreFinal.append((C7_z_score[m] - mean_z_C7)/std_z_C7)
print("课程7归一化的数据矩阵为：")
for x in range(len(C7_z_scoreFinal)):
    print(C7_z_scoreFinal[x])
print("********************************************")


# 计算C8的z-score
C8_z_score = []
for i in range(len(d)):
    if d[i][12] != '':
        C8_z_score.append(float(d[i][12]))
# 求协方差
ss_z_C8 = 0.0
mean_z_C8 = mean(C8_z_score)    # 成绩的平均值
for i in range(len(C8_z_score)):  # 协方差公式，先计算和
    ss_z_C8 += (C8_z_score[i] - mean_z_C8) * (C8_z_score[i] - mean_z_C8)
ss_z_C8 = ss_z_C8/(len(C8_z_score) - 1)
std_z_C8 = ss_z_C8 ** 0.5
print("C8成绩的平均值是：", mean_z_C8)
print("C8成绩的协方差是：", ss_z_C8)
print("C8成绩的标准差是：", std_z_C8)
C8_z_scoreFinal = []
for m in range(len(C8_z_score)):
    C8_z_scoreFinal.append((C8_z_score[m] - mean_z_C8)/std_z_C8)
print("课程8归一化的数据矩阵为：")
for x in range(len(C8_z_scoreFinal)):
    print(C8_z_scoreFinal[x])
print("********************************************")


# 计算C9的z-score
C9_z_score = []
for i in range(len(d)):
    if d[i][13] != '':
        C9_z_score.append(float(d[i][13]))
# 求协方差
ss_z_C9 = 0.0
mean_z_C9 = mean(C9_z_score)    # 成绩的平均值
for i in range(len(C9_z_score)):  # 协方差公式，先计算和
    ss_z_C9 += (C9_z_score[i] - mean_z_C9) * (C9_z_score[i] - mean_z_C9)
ss_z_C9 = ss_z_C9/(len(C9_z_score) - 1)
std_z_C9 = ss_z_C9 ** 0.5
print("C9成绩的平均值是：", mean_z_C9)
print("C9成绩的协方差是：", ss_z_C9)
print("C9成绩的标准差是：", std_z_C9)
C9_z_scoreFinal = []
for m in range(len(C9_z_score)):
    C9_z_scoreFinal.append((C9_z_score[m] - mean_z_C9)/std_z_C9)
print("课程9归一化的数据矩阵为：")
for x in range(len(C9_z_scoreFinal)):
    print(C9_z_scoreFinal[x])
print("********************************************")


# 体能成绩的协方差，标准差已在实验一计算过，不再重复计算
# 体能成绩的归一化矩阵
print("体能成绩的协方差是：", ss_Constitution)
print("体能成绩的标准差是：", std_Constitution)
Constitution_z_scoreFinal = []  # 保存归一化矩阵
# Constitution_Socre保存着体能成绩（以1分，2分，3分，4分表示）
for m in range(len(Constitution_Socre)):
    Constitution_z_scoreFinal.append((Constitution_Socre[m] - mean_Constitution)/std_Constitution)
print("体能成绩归一化的数据矩阵为：")
for x in range(len(Constitution_z_scoreFinal)):
    print(Constitution_z_scoreFinal[x])
print("********************************************")


# 4.计算出100x100的相关矩阵，并可视化出混淆矩阵。（为避免歧义，这里“协相关矩阵”进一步细化更正为100x100的相关矩阵，100为学生样本数目，视实际情况而定）
# 把学生课程1成绩至课程5成绩保存在一个新的列表,因为课程1-5是百分制的，6-9是十分制的
row = []
column = []
data = []
row_mean = []        # 存放行的平均值
s_ID = []       # 存放data中学生的ID
# 每一行的平均值
for x in range(len(d)):
    temp_sum = 0.0
    flag = 0    # 标志某一行是否有空值，1则有；0则没有
    for y in range(5, 10):      # 某一行有空值，则不加入列表data；相当于舍去有某一项成绩为空的学生
        if d[x][y] != '':
            row.append(int(d[x][y]))
            temp_sum += int(d[x][y])  # 存放第x行的和
        if d[x][y] == '':
            flag = 1
    if flag == 0:
        row_mean.append(temp_sum/5.0)
        data.append(row)
        s_ID.append(d[x][0])
    row = []

# 计算每一行的方差
row_s = []      # 存放每一行的方差
for x in range(len(data)):
    temp_sum = 0.0
    for y in range(5):
        temp_sum += (data[x][y] - row_mean[x]) ** 2   # 先求差的平方
    row_s.append(temp_sum/5)    # 第x行的方差

print("二维列表的维数为(人数*5)：", len(data), "*", len(data[0]))
for line in data:      # 输出最后结果
    print(line)
print("每一行的平均值", row_mean)
print("每一行的方差", row_s)

# 求协方差
p_x_y = []    # 相关系数矩阵
row_p = []      # 行的相关系数
for x in range(len(data)):      # data第x行和第y行的相关系数
    for y in range(len(data)):
        temp_sum = 0.0
        for m in range(5):
            temp_sum += (data[x][m] - row_mean[x]) * (data[y][m] - row_mean[y])
        row_p.append(temp_sum/(5*((row_s[x] * row_s[y]) ** 0.5)))   # 相关系数公式
    p_x_y.append(row_p)
    row_p = []
print(len(data), "个学生样本5个课程的相关系数矩阵为：")
for line in p_x_y:
    print(line)
"""
# 可视化混淆矩阵我不是很不理解
# 混淆矩阵
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix


def plot_confusion_matrix(confusion_mat):
    plt.imshow(confusion_mat)
    plt.title('Confusion Matrix')
    plt.colorbar()

    labels = ['a', 'b', 'c', 'd']
    tick_marks = np.arange(len(labels))
    plt.xticks(tick_marks, labels)
    plt.yticks(tick_marks, labels)
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.show()


if __name__ == '__main__':
    y_true = [1, 0, 0, 2, 1, 0, 3, 3, 3]
    y_pred = [1, 1, 0, 2, 1, 0, 1, 3, 3]
    confusion_mat = confusion_matrix(y_true, y_pred)
    plot_confusion_matrix(confusion_mat)
"""

# 5. 根据相关矩阵，找到距离每个样本最近的三个样本，得到100x3的矩阵（每一行为对应三个样本的ID）输出到txt文件中，以\t,\n间隔。
min_distance = []   # 保存100x3的矩阵（每一行为对应三个样本的ID）

for i in range(len(data)):
    nums = p_x_y[i][:]
    max_num_index_list = list(map(nums.index, heapq.nlargest(4, nums)))     # 找到每一行的4个最大值的下标,因为每一行最大值为1，也计算进去了
    # 所以找到最大的4个值，舍去为1的值的下标
    temp_id = []
    temp_id.append(s_ID[max_num_index_list[1]])     # 把对应下标的ID放进min_distance矩阵，但并未排序
    temp_id.append(s_ID[max_num_index_list[2]])
    temp_id.append(s_ID[max_num_index_list[3]])
    min_distance.append(temp_id)
print("5. 根据相关矩阵，找到距离每个样本最近的三个样本，得到100x3的矩阵（每一行为对应三个样本的ID）")
for line in min_distance:
    print(line)
# 输出到txt文件中，以\t,\n间隔。
with open(r'F:\大三上\机器学习\100-3.txt', 'w') as f:
    for i in min_distance:
        for j in i:
            f.write(j)
            f.write('\t')
        f.write('\n')
    f.close()
