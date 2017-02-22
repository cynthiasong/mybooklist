# !Python 3

# 功能：
# 利用豆瓣搜索API获得RAWLIST.md中每本书籍的详细信息；
# 将转换完成的格式保存到README.md

# 使用：
# 使用前先安装requests（pip install requests）
# 安装后直接运行本脚本即可（python transform.py）

import requests
import re
import time


class Book(object):
    def __init__(self, searchkey='', bookid=None):
        # 如果有书籍id，根据id获取书籍信息
        if bookid:
            search_url = 'https://api.douban.com/v2/book/{bid}'.format(bid=bookid)
            bookinfo = requests.get(search_url).json()
            print('正在检索 -> {bid}'.format(bid=bookid))
        # 否则检索关键词，获取返回的第1本书
        else:
            search_url = 'https://api.douban.com/v2/book/search?{q}&{c}'.format(
                q='q='+searchkey, c='count=1'
            )
            print('正在检索 -> {sk}'.format(sk=searchkey))
            books = requests.get(search_url).json()['books']
            try:
                bookinfo = books[0]
            except IndexError:
                bookinfo = {}
        try:
            self.id = bookinfo['id']
        except KeyError:
            print('运行失败 -> 没有找到符合条件的书籍，请修改描述后重新运行'.format(
                sn=searchkey
            ))
            exit()
        self.url = 'https://book.douban.com/subject/{id}'.format(id=self.id)
        self.title = bookinfo['title']
        self.link_title = '[{title}]({url})'.format(
            title=self.title, url=self.url)
        self.rating = bookinfo['rating']['average']
        self.ratenum = bookinfo['rating']['numRaters']
        self.pubdate = bookinfo['pubdate']
        self.pagenum = bookinfo['pages']
        self.author = ','.join(bookinfo['author'])

    # 提取被标记频次最多的3个标签
    @property
    def tags(self):
        common_tag_info = requests.get('https://api.douban.com/v2/book/{id}/tags'.format(
            id=self.id)).json()['tags'][:3]
        return '; '.join([info['title'] for info in common_tag_info])

    @property
    def entry(self):
        book_entry = '|{bn}|{rt}|{rn}|{tags}|{pd}|{pn}|{au}|'.format(
            bn=self.link_title,
            au=self.author, pd=self.pubdate, pn=self.pagenum,
            rt=self.rating, rn=self.ratenum, tags=self.tags
        )
        return book_entry + '\n'

class Category(object):
    def __init__(self, catname):
        self.title = catname

    @property
    def entry(self):
        title = '##' + self.title
        header = '|书名|豆瓣评分|评分人数|常用标签|出版日期|页数|作者|'
        line = '|---|---|---|---|---|---|---|'
        cat_entry = '\n'.join((title, header, line))
        return '\n' + cat_entry + '\n'

def transform():
    output = ''
    with open('RAWLIST.md', 'r', encoding='utf-8') as raw:
        content = raw.read() + '\n'
        # 根据h2切分版块
        segments = ['##' + seg for seg in content.split('##')[1:]]
    for seg in segments:
        # 添加分类名称及表头
        catname = re.search('\#\#(.*?)\n', seg).group(1).strip()
        category = Category(catname)
        output += category.entry
        print('成功添加类别 -> {cat}'.format(cat=catname))
        lines = [line for line in seg.split('\n')[1:] if len(line)>0]
        # 遍历获取书籍信息，添加到表格
        for line in lines:
            # 搜索关键词
            search_keywords = [w.strip() for w in re.split(r'《|》|id\s*\d+', line) if len(w)>0]
            searchkey = '+'.join(search_keywords)
            # 书籍id
            id_info = re.search(r'id\s*(\d+)', line)
            bookid = int(id_info.group(1)) if id_info else None

            book = Book(searchkey, bookid)
            output += book.entry
            print('成功获取 -> 书名:《{bn}》; 作者: {au}\n'.format(
                bn=book.title, au=book.author
            ))

    # 添加介绍部分
    timeinfo = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    with open('INTRO.md', 'r', encoding='utf-8') as intro:
        output = re.sub('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', timeinfo,
                        intro.read()) + '\n' + output

    with open('README.md', 'w', encoding='utf-8') as final:
        final.write(output)
    print('结果成功保存在README.md')


if __name__ == '__main__':
    transform()