import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 计算五数数值
def process_data(num):
    MIN = min(num)
    Q1 = np.percentile(num, 25)
    Q2 = np.percentile(num, 50)
    Q3 = np.percentile(num, 75)
    MAX = max(num)
    return MIN, Q1, Q2, Q3, MAX

# 计算Lift系数
def calc_Lift(pyx, py):
    lift = pyx / py
    return lift

# 计算Kulf系数
def calc_Kulf(confidence1, confidence2):
    kulf = (confidence1 + confidence2) / 2
    return kulf

# 可视化数据分布
def visualize(data):
    x = [1, 2, 3, 4]
    x1 = [0 for i in range(4)]
    x2 = [0 for i in range(4)]
    x3 = [0 for i in range(4)]
    y1 = [0 for i in range(4)]
    y2 = [0 for i in range(4)]
    y3 = [0 for i in range(4)]
    for i in range(len(data)):
        for j in range(0, 4):
            if data.loc[i, 'views'] == j + 1:
                x1[j] += 1
            if data.loc[i, 'likes'] == j + 1:
                x2[j] += 1
            if data.loc[i, 'comment_count'] == j + 1:
                x3[j] += 1
    for i in range(0, 4):
        y1[i] = x1[i] / len(data)
        y2[i] = x2[i] / len(data)
        y3[i] = x3[i] / len(data)
    plt.axis([1, 4, 0.24, 0.26])
    plt.plot(x, y1, color = 'blue')
    plt.plot(x, y2, color = 'red')
    plt.plot(x, y3, color = 'green')
    plt.show()


if __name__ == '__main__':
    # 读入数据并消去残缺项
    df = pd.read_csv("USvideos.csv")
    for i in range(len(df)):
        if df.loc[i, 'likes'] == 0 or df.loc[i, 'comment_count'] == 0:
            df.loc[i, 'likes'] = np.nan
    df.dropna(inplace = True)
    df.reset_index(drop = True, inplace = True)

    # 根据五数属性处理数据，使其便于进行关联规则挖掘
    nominals = ['views', 'likes', 'comment_count']
    for i in nominals:
        MIN, Q1, Q2, Q3, MAX = process_data(df[i])
        for j in range(len(df)):
            num = df.loc[j, i]
            if num <= Q1:
                df.loc[j, i] = 1
            elif Q1 < num <= Q2:
                df.loc[j, i] = 2
            elif Q2 < num <= Q3:
                df.loc[j, i] = 3
            elif num > Q3:
                df.loc[j, i] = 4
    df = df[nominals]

    # 寻找频繁模式
    num = [0 for i in range(64)]
    support = [0 for i in range(64)]
    flag = 0
    for i in range(len(df)):
        for j in range(1, 5):
            for k in range(1, 5):
                for l in range(1, 5):
                    if df.loc[i, 'views'] == j and df.loc[i, 'likes'] == k and df.loc[i, 'comment_count'] == l:
                        index = 16 * (j - 1) + 4 * (k - 1) + l - 1
                        num[index] += 1
    print("频繁模式为:")
    for i in range(64):
        support[i] = num[i] / len(df)
        if support[i] > 0.1:
            i1 = i / 16 + 1
            i2 = (i % 16) / 4 + 1
            i3 = (i % 16) % 4 + 1
            flag += 1
            print("views = " + str(i1) + ", likes = " + str(i2) + ", comment_count = " + str(i3))
    
    # 计算关联规则的支持度和置信度
    px = [0 for i in range(flag)]
    py = [0 for i in range(flag)]
    for i in range(len(df)):
        if df.loc[i, 'views'] == 1:
            px[0] += 1
        elif df.loc[i, 'views'] == 4:
            px[1] += 1
    for i in range(len(df)):
        if df.loc[i, 'likes'] == 1 and df.loc[i, 'comment_count'] == 1:
            py[0] += 1
        elif df.loc[i, 'likes'] == 4 and df.loc[i, 'comment_count'] == 4:
            py[1] += 1
    support1 = support[0]
    support2 = support[63]
    confidence1 = num[0] / px[0]
    confidence2 = num[63] / px[1]
    print("关联规则1的支持度为:" + str(support1) + ", 置信度为:" + str(confidence1))
    print("关联规则1的支持度为:" + str(support2) + ", 置信度为:" + str(confidence2))

    # 采用Lift系数评价关联规则
    Lift1 = calc_Lift(confidence1, py[0] * len(df))
    Lift2 = calc_Lift(confidence2, py[1] * len(df))
    print("关联规则1的Lift系数为:" + str(Lift1))
    print("关联规则2的Lift系数为:" + str(Lift2))

    # 采用Kulf系数评价关联规则
    confidence11 = num[0] / px[0]
    confidence12 = num[0] / py[0]
    confidence21 = num[63] / px[1]
    confidence22 = num[63] / py[1]
    Kulf1 = calc_Kulf(confidence11, confidence12)
    Kulf2 = calc_Kulf(confidence21, confidence22)
    print("关联规则1的Kulf系数为:" + str(Kulf1))
    print("关联规则2的Kulf系数为:" + str(Kulf2))

    # 可视化数据
    visualize(df)