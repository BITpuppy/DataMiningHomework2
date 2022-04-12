import pandas as pd
import numpy as np

# 计算五数数值
def process_data(num):
    MIN = min(num)
    Q1 = np.percentile(num, 25)
    Q2 = np.percentile(num, 50)
    Q3 = np.percentile(num, 75)
    MAX = max(num)
    return MIN, Q1, Q2, Q3, MAX

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

