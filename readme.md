# Mapreduce_Search_Engine_for_bilibili

> This is my final assignment of a course "Parallel and Distributed Computing".

This project contains: 
* Webcrawler
* Hadoop_mapreduce

Mapreduce program will find the html pages that have the most keywords.


# Getting Started

### Prerequisites
* Use [webCrawler.py](https://github.com/DizzyYunxuan/Mapreduce_Search_Program_for_bilibili/blob/master/webCrawler.py) to collect html pages
* You need to configure a hadoop cluster.You can find my configure guide in Hadoop_conf_guide.md [hadoop3.2.0]

### Usage

Start all node in cluster.

```sh
$ cd <your_hadoop_home>/sbin
$ ./start-all.sh
```

Upload data to hdfs file system. For example,

```sh
$ hdfs dfs -mkdir /user/hadoop/inputs
$ hdfs dfs -put <local data path> /user/hadoop/inputs
```
Use mapred program with mapper.py and reducer.py
Confirm output dir is not exist. Run following command.

```sh
mapred streaming \
-input /user/hadoop/inputs\
-output /user/hadoop/output \
-mapper mapper.py \
-reducer reducer.py \
-file <path of mapper.py> \
-file <path of reducer.py>
```
This command is equal to
```sh
$ python mapper.py | python reducer.py
```
So you can test your mapper and reducer on local machine.

The result is writed to file. It will looks like:
```
https://www.bilibili.com/video/av10000	<keyword>	46
https://www.bilibili.com/video/av10005	<keyword>	41
https://www.bilibili.com/video/av10001	<keyword>	41
https://www.bilibili.com/video/av100	<keyword>	47

......
```
![](https://i.loli.net/2019/07/09/5d24a712b323c45075.png)
![](https://i.loli.net/2019/07/09/5d24a7178024896115.png)
![](https://i.loli.net/2019/07/09/5d24a71f90f9082005.png)

## Authors

* **DizzyYunxuan** - *Initial work* - [DizzyYunxuan](https://github.com/DizzyYunxuan)
