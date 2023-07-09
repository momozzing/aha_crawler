import os
import json
import re
from bs4 import BeautifulSoup
from tqdm import tqdm
# filename = "gomc.html"

# file_path = 'test_page/'
file_path = 'pages/'
# domain_path = ["법률","세금세무","인사노무","의료","약료","반려동물","치과","한방","부동산","경제금융","보험","영양식단","교통사고","과학","육아아동","인문예술","생활꿀팁","청소","세탁","자동차","등산","캠핑","고민상담"]
domain_path = ["캠핑","고민상담"]

for main_file in tqdm(domain_path):     ### iterate file  
    json_list = []
    file_num = 0
    for file in tqdm(os.listdir(main_file+"/"+file_path)):     ### iterate file  
        with open (main_file+"/"+file_path + file , 'rt') as myfile:
            soup = BeautifulSoup(myfile, 'html.parser')
            #__layout > div > div.base > div.page-container.-pt.page > section > div > main > div > div.md\:tw-w-3\/4.md\:tw-pr-4 > div:nth-child(2) > div:nth-child(1) > div > article > div > header > a
            print("\n","domain:",main_file, "file_name:",file)

            my_titles = soup.select("head > script") #아이디로 태그 찾음

            # my_titles = soup.select('script', attrs={'type': 'application/ld+json'})
            # print(my_titles)
            aha_url_list = []
            question_list = []
            content_list = []
            for title in my_titles:
                aha_url_list.append(title.text)
                            
            json_data = json.loads(aha_url_list[2])
            
            question = json_data["mainEntity"]['name']
            content = json_data["mainEntity"]['text']

            # question_list.append(question)
            # content_list.append(content)

            # for q, c in zip(question_list, content_list):
                # print('question', q)
                # print('content', c)
                # print('index', file_num)
                
            json_shape = {
                "number":file_num,
                "question":question,
                "content":content
            }
            json_list.append(json_shape)
            # print(json_list)
                
        file_num += 1
        domain_name = main_file
        final_json_file = {
            "domain_name": domain_name,
            "Questions":json_list
        }

        with open(f"./{domain_name}.json", 'w', encoding='utf-8') as file:
            json.dump(final_json_file, file, indent=4, ensure_ascii=False)


# restaurant_list = []
# article_list = []
# review_list = []


# with open (file_path + "/23525.html", 'rt') as myfile:  # 파일 불러내기        ## title 
#     soup = BeautifulSoup(myfile, 'lxml')
#     # print(soup.h1.string)
#     title = soup.h1.string

#     abstract = str(soup.find_all(attrs={'class':'article-content-lead'}))
#     # print(abstract.replace('<p class="article-content-lead">', "").replace('</p>', "").replace('[', "").replace(']', ""))
#     abstract = abstract.replace('<p class="article-content-lead">', "").replace('</p>', "").replace('[', "").replace(']', "")
    
#     restaurant = soup.find_all(attrs={'class':'matome-show-article__heading2'})
#     for i in restaurant:
#         restaurant_clean_text = re.sub('<[^<]+?>', '', str(i))
#         restaurant_list.append(restaurant_clean_text)
        
#     # for i in restaurant_list:
#     #     print(i)
    
#     article = soup.find_all(attrs={'class':'ArticleImageComment'})
#     for i in article:
#         # print(str(i).replace('<p class="ArticleImageComment">', "").replace('</p>', "").replace("<br/><br/>", ""))
#         article_clean_text = str(i).replace('<p class="ArticleImageComment">', "").replace('</p>', "").replace("<br/><br/>", "")
#         article_list.append(article_clean_text)

        
#     review = soup.find_all(attrs={'class':'rvw-quote__quote'})
#     for i in review:
#         # print(str(i).replace('<q class="rvw-quote__quote">', "").replace('</q>', ""))
#         review_clean_text = str(i).replace('<q class="rvw-quote__quote">', "").replace('</q>', "")
#         review_list.append(review_clean_text)


# json_file = {
#     "title": title,
#     "abstract": abstract,
#     "restaurant": {
#         "酒と女と鶏と麺": {
#             "article": "大阪梅田駅から徒歩4分の場所にあるお店「酒と女と鶏と麺」は、和・中・韓の味が融合したタッカンマリの専門店。個室が完備されているため、様々なシーンで利用しやすいと人気です。 「タッカンマリ・白鍋」は、白湯スープを使用したタッカンマリを楽しめるスタンダードなコース。薬味は、自家製の味付け味噌のタテギ、黒胡椒塩漬けなどがついてくるそう。 「タッカンマリ・フカヒレ」は、鶏白湯タッカンマリと約300gのフカヒレが食べられるコースです。鶏白湯で煮込まれたフカヒレは、ツルツルとしたのど越しで絶品だそう。とても贅沢な韓国鍋ですね。",
#             "review1": "今回は個室にてスタンダードなタッカンマリのコースをいただきました。看板メニューのタッカンマリには伊達鶏が使用され、しっかりした食べ応えがあります。またこれで〆てほしいくらい美味しいスープです",
#             "review2": "・麻辣タッカンマリ・朱鍋私は少し辛いのが苦手ですが、コレはお代わりがいくらでも欲しいくらい美味しかった！勿論鍋以外のお料理も一つ一つ美味しい。それにお店の方が丁寧に説明してくださるし、お鍋も良いタイミングで食べられますよ。"
#         },
#         "つぼキムチ 北新地店": {
#             "article": "「つぼキムチ 北新地店」は、梅田駅から徒歩10分の距離にあるお店です。素材だけでなく、調理法や盛り付けにまでこだわった韓国料理が楽しめます。 店内には、テーブル席・座敷・半個室など様々な席があります。写真は9名で利用できる個室。「ヘムルチゲ」は、深い出汁の味わいを楽しめる韓国鍋。渡り蟹、海老、あさりなどの魚介類が入っているそうです。追加で豚バラ肉やホルモンを入れると、美味しさが増すのだとか。「プルダックのカルグクス」は、激辛のランチメニューです。玉ねぎがたくさん入っているため、辛さの後に甘みが追いかけてくるのだとか。韓国うどんの「カルグクス」は、平打ちでコシがあるそう。",
#             "review1": "前とメニュー変わってて、焼肉とちりとり鍋のお店に。ちりとり鍋自体美味しいのはもちろん、お肉めっちゃ美味しい❗️次は焼肉食べに行きます",
#             "review2": "もちもちしたチヂミに甘酸っぱいチキン。お鍋のお出汁の辛さもちょうどよい。どのお料理をみんな美味しかったです。"
#         }
#     }
# }



    # print(test.replace('<p class="ArticleImageComment">', "").replace('</p>', ""))            
    # tmp = test.replace('<p class="ArticleImageComment">', "").replace('</p>', "")
    # print(tmp)
    # for i in tmp:
    #     print(i)


    # for myline in myfile:                 # 모든 파일 1줄씩 읽기
    #     if myline.find("<title>")!=-1: # <title> 와 같은 string 이 있다면
    #         print(myline.replace("<title>", "").replace("</title>", "").replace("[食べログまとめ]", ""))                     # 그 1줄씩 출력하기
        
    #     if myline.find("article-content-lead")!=-1:                    ### abstract
    #         print(myline.replace('<p class="article-content-lead">', "").replace('</p>', ""))
            
    #     if myline.find('class="matome-show-article__heading2"')!=-1:                    ### abstract
    #         clean_text = re.sub('<[^<]+?>', '', myline)
    #         # string_list = [s.strip() for s in clean_text.split('\n') if s.strip()]
    #         # restaurant_list.append(string_list)
            
    #         # merged_list = [elem for sublist in restaurant_list for elem in sublist][-1]
    #         print(clean_text)
            
    #     if myline.find("ArticleImageComment")!=-1:                    ### abstract
    #         # print(myline.replace('<p class="article-content-lead">', "").replace('</p>', ""))            
    #         print(myline)            
            
    #     if myline.find('ArticleDesc')!=-1:
    #         print(myline)            

            
# for i in restaurant_list:
#     print("test", i)
    
        # if myline.find('class="matome-show-article__heading2"')!=-1:                    ### abstract
        # clean_text = re.sub('<[^<]+?>', '', myline)
        # string_list = [s.strip() for s in clean_text.split('\n') if s.strip()]
        # restaurant_list.append(string_list)
        
        # # merged_list = [elem for sublist in restaurant_list for elem in sublist][-1]
        # print(restaurant_list)
        