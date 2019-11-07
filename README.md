# 数据查询平台

从数据库内查询数据然后展示到平台

使用Tornado框架+bootstrap前端处理

运行环境：```Python3.0+```

平台完成截图如下：

![](https://github.com/chuxuan909/Tornado/blob/master/images/plat.png)

## DataStatistics

数据库查询核心模块，连接Redis、Mongodb、MySQL数据库来查询需要的数据，并为Tornado框架提供Api接口。也可以直接使用模块进行查询

模块入口文件为目录下```bin```目录内的```Coll.py```文件，命令：

```bash
python3 Coll.py
```

模块能实现的功能

```
coll.py
请输入功能参数

        dbtest                         测试数据库连接
        people                         查询注册总人数
        regpeople  <yyyy-mm-dd>        查询某日注册总的用户数，默认为当日
        pay        <yyyy-mm-dd>        查询某日支付用户数，默认为当日
        record     <yyyy-mm-dd>        查询某日游戏记录较多的用户数，默认为当日
        active     <yyyy-mm-dd>        查询某日活跃的用户数，默认为当日
        inputs     <yyyy-mm-dd>        查询某日投入前100的玩家数，默认为当日（即时查询）
        outputs    <yyyy-mm-dd>        查询某日产出前100的玩家数，默认为当日（即时查询）
        revenues   <yyyy-mm-dd>        查询某日游戏的营收（默认为昨日，超过昨天日期默认为昨日）
        win_rank   <yyyy-mm-dd>        查询某日赢前100的玩家，默认为当日
        lose_rank  <yyyy-mm-dd>        查询某日输前100的玩家，默认为当日
```

### 关于core目录下的模块功能

- **DataGo：** 入口文件调用的核心功能模块，接收数据查询功能并处理
- **DataManager：** 处理mongo查询到的复杂数据
- **DBfunction：** 处理MySQL查询
- **MongoFun：** 处理Mongodb查询
- **RedisFunction：** 处理Redis查询

## DataPlat 

Tornado框架的核心代码，利用数据库查询核心模块的API获取到数据库的数据，经过处理后展示到bootstrap前端

前端使用bootstrap的多标签分页处理来查询结果的循环展示

### ==注意==

在DataPlat下的```TornadoServer.py``` 文件中使用了绝对路径的方式来将数据库查询核心模块DataStatistics加入了环境变量，代码如下：

```python
#查询模块路径
DataGo_Path='F:/PythonBuild/DataStatistics'
# DataGo_Path='/home/Tornado/DataStatistics' #linux下路径

#环境变量
sys.path.append(DataGo_Path)
from core import DataGo
```

如果移植平台，需要指定新的绝对路径，或者直接使用相对路径等办法



