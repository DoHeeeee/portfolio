import matplotlib
import pandas as pd
#from wordcloud import WordCloud
import matplotlib.pyplot as plt
#from konlpy.tag import Okt
import re
from collections import Counter
from matplotlib.pyplot import barh

#unnamed 컬럼이름 'num'으로 바꿔주기
#lunch.rename(columns = {'Unnamed: 0': 'num'}, inplace=True)
def rename_Unnamed(dataFrame):
    dataFrame.rename(columns = {'Unnamed: 0': 'num'}, inplace=True)

#필터링 하기
def filltering(dataFrame, column_name, string):
    mask = dataFrame[column_name].str.contains(string)
    result = dataFrame[mask]
    return result
#string 빼고 넣기
def filltering2(dataFrame, column_name, string):
    mask = dataFrame[column_name].str.contains(string)    
    mask = ~mask
    result = dataFrame[mask]
    return result

#text 합치기 
def make_all_text(dataFrame, columnName):
    dataFrame.reset_index(drop=True, inplace=True)
    result = ""

    if dataFrame[columnName][0][0] == '[':
        for i in dataFrame.index:
            text = " ".join(dataFrame[columnName][i][1:-1].replace(' ', '').replace('\'', '').split(','))
            result = result + " " + text

    else:
        for i in dataFrame.index:
            text = "".join(dataFrame[columnName][i])
            result = result + " " + text
    return result

#wordcloud 만들기
#딕셔너리 or 텍스트 넣기
def make_wordcloud(all_text):
    wordcloud = WordCloud(
        #font_path = 'C:\\Windows\\Fonts\\H2GTRE.TTF',
        font_path = 'C:/Windows/Fonts/malgun.ttf',
        width = 1600,
        height = 900
    )
    
    if type(all_text) == dict:
      result = wordcloud.generate_from_frequencies(all_text)
    else:
      result = wordcloud.generate(all_text)
    
    plt.imshow(
    result
    #interpolation='bilinear'
    )
    plt.axis("off")
    plt.show()

#원하는 그림모양으로 워드크라우드 만들기
#딕셔너리 or 텍스트 넣기
def make_wordcloud_background(all_text, background_img_path):
    from PIL import Image
    import numpy as np

    img = Image.open(background_img_path)
    img_matrix = np.array(img)

    wordcloud = WordCloud(
    #font_path = 'C:\\Windows\\Fonts\\H2GTRE.TTF',
    font_path = 'C:/Windows/Fonts/malgun.ttf',
    width = 1600,
    height = 900,
    mask = img_matrix,
    background_color='white'
    )
    
    if type(all_text) == dict:
      result = wordcloud.generate_from_frequencies(all_text)
    else:
      result = wordcloud.generate(all_text)

    plt.imshow(
    result
    #interpolation='bilinear'
    )
    plt.axis("off")
    plt.show()

#좋아요 콤마 지우고 int로 바꿔주기
#스트링으로 들어온 데이터를 int64로 바꿔준다.
def make_like(dataFrame, columnName):
    dataFrame[columnName] = dataFrame[columnName].str.replace(',', '')
    dataFrame[columnName] = dataFrame[columnName].fillna(0).astype('int64')

    return dataFrame

#여기서만 사용할 함수?
#태그를 한 리스트로 반환
def make_tags_list(tags_series):
    result = []
    for i in tags_series:
        temp_list = i[2: -2].split("', '")
        result = result + temp_list
    return result

#tag_value_counts 상위 n개 태그의 빈도수 df 반환
def value_counts_num(listOrSeries, num):
    if type(listOrSeries) == list:
      result = pd.DataFrame(Counter(listOrSeries).most_common(num))
    else:
      temp = make_tags_list(listOrSeries)
      result = pd.DataFrame(Counter(temp).most_common(num))
    return result
    
#plot 한글 설정
def han_font_set():
    from matplotlib import font_manager, rc
    font_name = font_manager.FontProperties(fname='C:/Windows/Fonts/malgun.ttf').get_name()
    matplotlib.rc('font', family = font_name)
    matplotlib.font_manager._rebuild()
'''
import matplotlib.font_manager as fm
fontpath = '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf'
font = fm.FontProperties(fname=fontpath)
plt.rc('font', family='NanumBarunGothic') 
matplotlib.font_manager._rebuild()
'''
#content 전처리
def prepro_content(dataFrame):
    dataFrame = dataFrame.fillna("nan")
    dataFrame.isnull().sum() # null 사라짐

    def text_cleaner(text):
        clean = text
        publisher = "\((.*?)\)"
        braces = "\[(.*?)\]"
        braces2 = "\{(.*?)\}"
        braces3 = "\【(.*?)\】"
        weird = "[=_\.,;:~…\"\"\'\'◇%\<\>/·○★☆ㅡ]"
        tab = '\\t'
        newline = '\\n'

        clean = re.sub(publisher,'', clean)
        clean = re.sub(braces,'', clean)
        clean = re.sub(braces2,'', clean)
        clean = re.sub(braces3,'', clean)
        clean = re.sub('[YTN,OSEN]','', clean)
        clean = re.sub(weird,'', clean)
        clean = re.sub(tab,'', clean)
        clean = re.sub(newline,'',clean)
        
        return clean

    for idx, text in enumerate(dataFrame['content']):
        dataFrame['content'][idx] = text_cleaner(text)

#나중에 학습시킬때 사용 
def make_vocab(dataframe):
    okt = Okt()

    sentences_pos = []
    for line in dataframe['content']:
        sentences_pos.append(okt.nouns(line))

    max_len = max([len(i) for i in sentences_pos])

    vocab = []
    for line in sentences_pos:
        for word in line:
            vocab.append(word)

    vocab_size = len(vocab) +1
    vocab = sorted(list(vocab))

   
    vocab = [item for item in vocab if len(item) != 1]

    return sentences_pos, vocab

#----------------------------------------------------
#워드클라우드 딕셔너리 들어왔을때 만들어지게 하기 폰트 주소 바꾸기


#------------------------만들엇지만 필요없는 함수

#컬럼이 한 사람으로 태그 뽑기
#num_tag_df = df[['num', 'tags]]
def Make_tag_df(num_tag_df):
    result = pd.DataFrame(index = range(0, 50))

    for i in range(len(num_tag_df.index)):
        #tags = num_tag_df['tags'][i][1:-1].replace(' ', '').replace('\'', '').split(',')
        tags = num_tag_df['tags'][i][2:-2].split("', '")
        num_column = num_tag_df['num'][i]

        tags = pd.DataFrame(tags)
        tags.rename(columns = {0 : num_column}, inplace = True)

        result = pd.concat([result, tags], join = 'outer', axis = 1)
        
        if(i % 100 == 0):
            print(i)
        
    return result

#한 사람이 한 row 태그 추출
def Make_tag_df2(num_tag_df):

    result = pd.DataFrame(columns = range(0, 50))

    for i in range(len(num_tag_df.index)):
        #tags = num_tag_df['tags'][i][1:-1].replace(' ', '').replace('\'', '').split(',')
        tags = num_tag_df['tags'][i][2:-2].split("', '")
        num_column = num_tag_df['num'][i]

        tags = pd.DataFrame(tags)
        tags = tags.transpose()
        tags.rename(index = {0 : num_column}, inplace = True)

        result = pd.concat([result, tags], join = 'outer')

        if(i % 100 == 0):
            print(i)
        
    return result

#태그 프래임을 집어넣으면 각 각의 갯수 반환
#make_tag_df2 리턴 값 사용
def make_value_counts(dataFrame):
    result = pd.Series()
    for i in dataFrame.columns:
        result = pd.concat([result, dataFrame[i]])

    return result.value_counts()


