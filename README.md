# 使用LTP+自定义词表进行命名实体识别

项目的构想是实现一个知识图谱构建系统，包括三个部分，命名实体识别、关系抽取、属性抽取；

暂时的方案：

1. 命名实体识别：LTP（人名、地名、机构名）+自定义词表（领域词典）
2. 关系抽取：规则（rules）+深度学习方法
3. 属性抽取：pattern

**此处为第一部分**

# 依赖说明

pyltp的安装
直接进行pip安装，容易报错，最好使用源码安装

### windows下安装

参考文章[哈工大自然语言处理ltp在windows10下的安装使用](http://mlln.cn/2018/01/31/pyltp在windows下的编译安装/)

* 下载wheels，下面两个文件针对不同的python版本下载一个即可。

[pyltp-0.2.1-cp35-cp35m-win_amd64.whl](http://mlln.cn/2018/01/31/pyltp在windows下的编译安装/pyltp-0.2.1-cp35-cp35m-win_amd64.whl)

[pyltp-0.2.1-cp36-cp36m-win_amd64.whl](http://mlln.cn/2018/01/31/pyltp在windows下的编译安装/pyltp-0.2.1-cp36-cp36m-win_amd64.whl)

* 安装文件，下载好了以后, 在命令行下，win10下清除文件路径输入cmd，可以在目录下快速打开cmd， 然后使用命令pip install wheel文件名安装.



### lunix下安装
安装之前确定电脑安装gcc，g++，没有安装的话，sudo apt-get install gcc 或者g++

* 首先下载[pyltp](https://github.com/hit-scir/pyltp)

* 下载[ltp](https://github.com/hit-scir/ltp)，将解压后的ltp文件夹命名为ltp，复制到pyltp文件夹中并覆盖之前的ltp文件夹；

* 在pyltp文件夹中有一个名为setup.py的python程序，

* 执行命令：python setup.py install。

**最近访问[pyltp](https://github.com/hit-scir/pyltp)的时候发现里面的ltp目录已经不是空的，那么就不需要再下载ltp了**



# 模块说明

```
├── ltp_ner                   # 命名实体识别
│  ├── extraction.py          # 实体识别主程序
│  ├── force.py               # 自定义词表匹配
│  ├── hio.py                 # 训练
│  ├── hlog.py                # log 日志输出
├── ltp_data                  # LTP模型存放目录(也可以在main.py里指定ltp位置)
├── project                   # 项目目录
│  ├── articles.csv           # 输入数据集(文本)
│  ├── entity.csv             # 输出数据集(句子+实体)
│  ├── lexicon                # 词表
│  ├── run                    # 日志存放目录
├── README.md                 # read me 文件
├── requirements.txt          # 依赖包
```

# 快速开始

```
from ltp_ner.hio import *
from ltp_ner.extraction import *

if __name__ == "__main__":
    # TAG是要提取出的实体标注和类型对照表
    TAG = {'Nh': '人名', 'Ns': '地名', 'Ni': '机构名'}
    # LTP模型存放位置
    LTP = '/home/nuc/桌面/gBuilder3/ltp_data'
    articles = load_csv('articles.csv')
    sentences = sentence(articles=articles, ltp_dir=LTP)
    entity(sentences=sentences, tag=TAG)
    save_csv(filepath='entity.csv',data=sentences)

```
### articles.csv样例(需表头)
id|content
:---:|:---:
10000132|从相恋到结婚，辛柏青和朱媛媛的爱情生活也是鲜有人知。
10000133|秦叔宝转到齐郡通守张须陀帐下，以镇压农民起义起家。
10000134|董维贤-经历曾向徐斌寿、陆喜才、方颐珍、李洪春学艺。


### lexicon词表
分隔符为空格,词语 标注：
注意，不要出现英文括号
```
天宫一号 spaceship
天宫二号 spaceship
Terra对地观测卫星 spaceship
TerraSAR-X雷达卫星 spaceship
```


