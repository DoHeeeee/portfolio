import pandas as pd
from method22 import *
import numpy as np
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules



ato_df = pd.read_excel('./data/atozzang.xlsx')
ato_df

rename_Unnamed(ato_df)

#데이터 전처리 -- 각 게시글 단위로 태그들을 묶어주는 2차원 list
def Make_tag(num_tag_df):
    result = []

    for i in range(len(num_tag_df.index)):
        #tags = num_tag_df['tags'][i][1:-1].replace(' ', '').replace('\'', '').split(',')
        tags = num_tag_df['tags'][i][2:-2].split("', '")
        result.append(tags)
        
        if(i % 100 == 0):
            print(i)
        
    return result

df_tmp_arr = Make_tag(ato_df)

#중복값 제거
df_tmp_arr.pop(0)
num=0
for i in df_tmp_arr :
    df_tmp_arr[num] = list(set(df_tmp_arr[num]))
    num+=1
df_tmp_arr


te = TransactionEncoder()
te_ary = te.fit(df_tmp_arr).transform(df_tmp_arr)
df = pd.DataFrame(te_ary, columns=te.columns_)

frequent_itemsets = apriori(df, min_support=0.05, use_colnames=True)
frequent_itemsets

