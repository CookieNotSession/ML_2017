# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#每一分鐘的 時間 收 開 高 低
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
df = pd.read_csv('TXF20112015.csv',sep=',',header=None)
TAIEX = df.values
tradeday = list(set(TAIEX[:,0]//10000)) #剩下年月日 
tradeday.sort()
profit = np.zeros((len(tradeday),1))
for i in range(len(tradeday)): #把分鐘資料找出來
    date = tradeday[i] #取最後一筆收盤價 與 第一筆開盤價 
    idx = np.nonzero(TAIEX[:,0]//10000==date)[0]
    idx.sort()
    p1 = TAIEX[idx[0],2] #開盤第一分鐘的開盤價 我買的價格
    idx2 = np.nonzero(TAIEX[idx,4]<=p1-30)[0] #符合停損情況
    idx3 = np.nonzero(TAIEX[idx,3]>=p1+30)[0] #符合停利情況
    if(len(idx2)==0 and len(idx3)==0): #那天太平順啦～都沒碰到停損與停利的情形！！
        p2 = TAIEX[idx[-1],1] #沒有找到30點的 回傳原本價格
    elif(len(idx3)==0):#碰到停損條件了 但停利條件為空集合
        p2 = TAIEX[idx[idx2[0]],1] #遇到停損那個低點30點 取第一個停損點收盤價 退場
    elif(len(idx2)==0):
        p2 = TAIEX[idx[idx3[0]],1]
    elif(idx2[0]<idx3[0]):
        p2 = TAIEX[idx[idx2[0]],1]
    else:
        p2 = TAIEX[idx[idx3[0]],1]
    profit[i] = p2-p1
profit2 = np.cumsum(profit)
plt.plot(profit2)
plt.show()
#不賠不賺都算虧錢 
ans1 = profit2[-1]
ans2 = np.sum(profit>0)/len(profit) #大於0的個數/總個數
ans3 = np.mean(profit[profit>0])
ans4 = np.mean(profit[profit<=0])
plt.hist(profit,bins=100) #切100等分 的直方圖

