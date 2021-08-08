from method22 import *
import pandas as pd

han_font_set()
#데이터 로드
evening = pd.read_excel('./data/evening.xlsx')
noon = pd.read_excel('./data/noon.xlsx')
morning = pd.read_excel('./data/morning.xlsx')
ato = pd.read_excel('./data/atozzang.xlsx')
bbo = pd.read_excel('./data/bbo.xlsx')
haewon = pd.read_excel('./data/haewon.xlsx')
twomuk = pd.read_excel('./data/2muk.xlsx')
muksta = pd.read_excel('./data/muksta.xlsx')
dfs = [ato, bbo, haewon, twomuk, muksta]

#1
for i in dfs:
  prepro_content(i)
#2
sentences_pos = []
vocab = []
for i in dfs:
  tempS, tempV = make_vocab(i)
  sentences_pos.append(tempS)
  vocab.append(tempV)
#3
vocab_value_counts = []
for i in vocab:
  vocab_value_counts.append(value_counts_num(i, 15))

#태그분석

#태그 전처리
#1
for i in dfs:
    rename_Unnamed(i)

#태그수 보기
tag_value_counts = []
for i in dfs:
    tag_value_counts.append(value_counts_num(i['tags'], 15))


#워드크라우드 용 text파일
text_list = []
for i in dfs:
    text_list.append(make_all_text(i, 'tags'))


#content 시각화
#barplot

fig = plt.figure(figsize = (20,20))
fig.add_subplot(2, 3, 1)
barh(vocab_value_counts[0][0], vocab_value_counts[0][1])
fig.add_subplot(2, 3, 2)
barh(vocab_value_counts[1][0], vocab_value_counts[1][1])
fig.add_subplot(2,3,3)
barh(vocab_value_counts[2][0], vocab_value_counts[2][1])
fig.add_subplot(2,3,4)
barh(vocab_value_counts[3][0], vocab_value_counts[3][1])
fig.add_subplot(2,3,5)
barh(vocab_value_counts[4][0], vocab_value_counts[4][1])
plt.show()


#tag 시각화
#barplot

fig = plt.figure(figsize = (20,20))
fig.add_subplot(2, 3, 1)
barh(tag_value_counts[0][0], tag_value_counts[0][1])
fig.add_subplot(2, 3, 2)
barh(tag_value_counts[1][0], tag_value_counts[1][1])
fig.add_subplot(2,3,3)
barh(tag_value_counts[2][0], tag_value_counts[2][1])
fig.add_subplot(2,3,4)
barh(tag_value_counts[3][0], tag_value_counts[3][1])
fig.add_subplot(2,3,5)
barh(tag_value_counts[4][0], tag_value_counts[4][1])
plt.show()

#시각화
#word cloud

for i in range(len(vocab_value_counts)):
  temp = vocab_value_counts[i].set_index(0).to_dict()[1]
  make_wordcloud(temp)

#tag 시각화
#word cloud

for i in range(len(tag_value_counts)):
  temp = tag_value_counts[i].set_index(0).to_dict()[1]
  make_wordcloud(temp)
