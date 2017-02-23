# BookList：利用GiHub搭建个人/团队书单系统

信息最后更新时间：1970-00-00 00:00:00

**运行环境：**
Python 3 + requests

[安装Python 3](https://www.python.org/download/releases/3.0/)

[安装requests](http://docs.python-requests.org/en/master/user/install)

**使用方法：**

1. 将本版本库Fork到自己的GitHub账号上
2. 将建立的新版本库Clone到本地
3. 在本地修改`INTRO.md`（生成在顶部的固定信息）
4. 修改`RAWLIST.md`（转换前的书单）
5. 运行`main.py`，自动从豆瓣API获取书籍信息，格式化保存到`README.md`
6. 完成后提交到自己的远程库

**`RAWLIST.md`填写说明：**

1. 每一行代表一本书，基本格式：`《书名》补充信息 id00000000`
2. 建议使用`《书名》`格式添加大多数书籍
3. 如果书名搜索结果不唯一，可选择添加补充信息或者指定书籍id
4. 书籍id为豆瓣网址最后的一串数字，如书籍网址为`https://book.douban.com/subject/5421787/`，则id为`5421787`
5. 可以使用`find_book.py`从控制台搜索书籍id
6. Markdown二级标题代表分类

可接受的格式示例如下：
```
《重新定义公司》
《人类简史》从动物到上帝
《经济学原理》第7版 id26435630
id11445548
```

以下为`RAWLIST.md`转换后的示例书单：
