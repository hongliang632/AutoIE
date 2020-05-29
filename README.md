# 使用LTP进行命名实体识别

## 依赖说明
pyltp的安装
直接进行pip安装，人员报错，最好使用源码安装

### windows下安装

### lunix下安装
安装之前确定电脑安装gcc，g++，没有安装的话，sudo apt-get install gcc 或者g++
ubuntu
```
sudo apt-get install gcc
```
centos
```
sudo yum install gcc
```

下载pytlp源代码，下载地址pytlp源代码,解压后的文件目录结构如下,其中的ltp文件夹是空的。
https://github.com/HIT-SCIR/pyltp

去github下在ltp的源码，下载地址ltp源码，把此压缩文件解压后的所有文件放在上图中的ltp空文件夹。

进入pyltp目录下，运行setup.py文件进行安装，命令如下：
```
python setup.py install
```
##模块说明
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
├── readme.md                 # read me 文件
├── requirements.txt          # 依赖包
```

##快速开始

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


