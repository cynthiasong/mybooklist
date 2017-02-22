# 获取搜索书籍列表，以便选择正确的书籍id
import requests


def find_bookid(searchkey, count=20):
    search_url = 'https://api.douban.com/v2/book/search?{q}&{c}'.format(
        q='q=' + searchkey, c='count=%d' % count
    )
    books = requests.get(search_url).json()['books']
    for book in books:
        id = book['id']
        url = 'https://book.douban.com/subject/{id}'.format(id=id)
        print(id, book['title'], url)

if __name__ == '__main__':
    # 运行：find_book('搜索关键词')
    # 从输出结果中选择想要的书籍id，写入RAWLIST.md中
    find_bookid('经济学原理+第7版')