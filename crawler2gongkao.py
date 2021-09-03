import requests

from bs4 import BeautifulSoup as bs


url = "http://www.bjrbj.gov.cn/gwyquery/publicQuery/gzwbkrsssquery"

payload_pro = "yhid=&pxdm=0&zwdm="

headers = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate",
    'accept-language': "zh-CN,zh;q=0.9",
    'cache-control': "no-cache",
    'connection': "keep-alive",
    'content-length': "27",
    'content-type': "application/x-www-form-urlencoded",
    'host': "www.bjrbj.gov.cn",
    'origin': "http://www.bjrbj.gov.cn",
    'referer': "http://www.bjrbj.gov.cn/gwyquery/publicQuery/gzwbkrsssquery",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    }


class ZwdmInfo:
    def __init__(self, zwdm, bkdw, bkzw, bkrs, msbl, scrs, scbl):
        self.zwdm = zwdm    #职位代码
        self.bkdw = bkdw    #报考单位
        self.bkzw = bkzw    #报考职位
        self.bkrs = bkrs    #报考人数
        self.msbl = msbl    #面试比例
        self.scrs = scrs    #审查通过人数
        self.scbl = scbl    #报考比例

    def file_data(self):    #标准化CSV文件写入格式
        return self.zwdm + "," + self.bkdw + "," + self.bkzw + "," + self.bkrs + "," + self.msbl + "," + self.scrs + "," + self.scbl + "\n"


try:
    zwdm_file = open('zwdm.txt')
    zwdm_data = open('爬取数据结果.csv','w')
    zwdm_data.write("职位代码,报考单位,报考职位,招考人数,面试比例（反比X:1）,报考该职位资格审查通过人数,报考比例（反比X:1）\n")      #写入标题

    for zwdm in zwdm_file:
        payload = payload_pro + zwdm[:-1]
        zwdm_soup = bs(requests.request("POST", url, data=payload, headers=headers).text, 'html.parser')
        zwdm = ZwdmInfo(zwdm[:-1],
                        str(zwdm_soup.find_all('table', class_='table1')).split('</tr>')[1].split('</td>')[1][5:],
                        str(zwdm_soup.find_all('table', class_='table1')).split('</tr>')[1].split('</td>')[2][5:],
                        str(zwdm_soup.find_all('table', class_='table1')).split('</tr>')[1].split('</td>')[3][5:],
                        str(zwdm_soup.find_all('table', class_='table1')).split('</tr>')[1].split('</td>')[4][7:],
                        str(zwdm_soup.find_all('table', class_='table1')).split('</tr>')[1].split('</td>')[5][5:],
                        str(zwdm_soup.find_all('table', class_='table1')).split('</tr>')[1].split('</td>')[6][7:])
            #print(zwdm.file_data())
        zwdm_data.write(zwdm.file_data())
        print('职位编号：'+ zwdm.zwdm + '\t已爬取完成\n')

    zwdm_file.close()
    zwdm_data.close()

    print("全部数据爬取完成，请打开文件查看!")

finally:
    pass



