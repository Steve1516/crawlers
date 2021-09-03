from urllib import request
movie_list_resp = request.urlopen('https://movie.douban.com/nowplaying/hangzhou/')
movie_list_html_data = movie_list_resp.read().decode('utf-8')

from bs4 import BeautifulSoup as bs
movie_list_soup = bs(movie_list_html_data, 'html.parser')

nowplaying_movie = movie_list_soup.find_all('div',id = 'nowplaying')
nowplaying_movie_list = nowplaying_movie[0].find_all('li', class_ = 'list-item')

import datetime

print('爬虫正在工作：')

nowplaying_list = []
for item in nowplaying_movie_list:
    nowplaying_dict = {}
    nowplaying_dict['id'] = item['data-subject']
    nowplaying_dict['name'] = item['data-title']
    nowplaying_dict['score'] = float(item['data-score'])

    each_movie_url = 'https://movie.douban.com/subject/' + nowplaying_dict['id'] + '/?from=playing_poster'
    each_movie_resp = request.urlopen(each_movie_url)
    each_movie_html_data = each_movie_resp.read().decode('utf-8')
    each_movie_soup = bs(each_movie_html_data, 'html.parser')

    nowplaying_dict['data'] = datetime.datetime.strptime(each_movie_soup.find_all('span', property = 'v:initialReleaseDate')[0].string[:10],'%Y-%m-%d')
    if (datetime.datetime.now() - nowplaying_dict['data']).days > 0 :
        nowplaying_dict['playing'] = '已经上映'
    else:
        nowplaying_dict['playing'] = '暂未上映'

    try:
        if nowplaying_dict['playing'] == '已经上映':
            nowplaying_dict['rating'] = int(each_movie_soup.find_all('span', property = 'v:votes')[0].string)
        else:
            nowplaying_dict['rating'] = '无评论'
    except:
        nowplaying_dict['rating'] = '无评论'

    print('Getting Data--> ' + nowplaying_dict['name'])

    nowplaying_list.append(nowplaying_dict)

playing_movie = []
pre_playing_movie = []

for element in nowplaying_list:
    if element['playing'] == '已经上映' and element['rating'] != '无评论':
        playing_movie.append(element)
    else:
        pre_playing_movie.append(element)

print('\n已上映电影（按评分和评论人数排名）：')
count = 0
playing_movie.sort(key=lambda x: (x.get('rating', 0), x.get('score', 0)), reverse=True)
for element in playing_movie:
    print('排名：%d ；电影名称：%s ；评分：%.1f ；评论人数：%d'%(count,element['name'],element['score'],element['rating']))
    count += 1

print('\n未上映电影：')
for element in pre_playing_movie:
    print('电影名称：%-s ；上映时间：%s'%(element['name'],str(element['data'])[:10]))
