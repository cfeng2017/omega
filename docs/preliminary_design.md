Omega Preliminary Design
===

引言
---

### 目的

统一DBA目前系统，为DBAs提供一个方便的平台，减少DBAs一些重复繁琐的工作。

### 背景

目前老系统对Mysql监控图表的显示异常，对Nosql监控缺乏，对slow，dbrt等系统有需求，急需一套管理系统，所以本系统提上日程。目前系统名叫Omega，对于以后分布在各监控对象上的Agent，可命名为 Alpha。

总体设计
---

第一期完成最基本的监控和报警功能，第二期完成slow，dbrt等功能，后续还会增加job调度管理等功能。期间会不定时的对系统进行完善和优化。

### 需求分析

#### 监控

对于监控模块，需要满足如下条件：

- 提供 RESTful API
- 3种级别的展示，每种级别的展示包括相应级别需要监控的具体项，每个具体项为一张图表，每个具体项中可包括一级子项——即每张图中可包括多种子监控项。3种级别如下：
 - 组/集群
 - Host
 - Instance
- 每种级别都可以被订阅及接警
- 能满足自定义监控

#### 报警

报警模块需要尽量提供可定制化。其内容主要如下：

- 接警人   
- 报警频率  
  每隔多长时间接收报警
- 延迟报警  
  连续N分钟异常则报警
- 报警方式  
 可使用消息通知中的方法
- 报警阈值
 - 差值
     - 具体值
     - 百分比
 - 极值
 - 斜率

#### CMC

整个系统的配置中心，包括如下范围：

- SSH KEY

#### 日志
分为两种日志，系统本身运行的日志和用户操作日志。

### 运行环境

全系统使用的软件及版本如下：

- Python2.7
- Django==1.6.5
- Flask-0.10.1 
- Jinja2-2.8 
- MarkupSafe-0.23 
- Werkzeug-0.10.4 
- itsdangerous-0.24
- Flask-SQLAlchemy-2.0


### 基本设计概念和处理流程
总体结构图如下：

![结构图](images/mokuai.png)

各个子平台如下：
- Monitor
- Slow
- DBRT
- Report
- Job

先说下通用模块。

- 登录与权限
- 远程执行命令
- 消息通知（邮件、短信）
- 基础算法
- 订阅
- 报警

对于不同的模块，可使用不同的消息通知方法，如监控报警的消息通知可为邮件和短信，而 DBRT，Slow等模块只需使用邮件提醒即可。对于用户的操作部分，直接在页面提示。

- 搜索
- SQL解析与优化
- Job调度

### 数据设计
#### ER图
如下

![ER图](images/er.jpg)

#### 数据表定义如下

包括目前Mysql的各种分组，Redis集群中分组，Memcached分组，Hadoop群集的分组等

- 组类型表
组类型比较复杂，除了Mysql，Redis等分组外，对于自定义分组也是兼容的，如添加某部门的业务监控，在类型表中新增“业务”项，然后在`group`加部门即可。
该表数据最好同时在redis做存储以提高查询速度。
```
CREATE TABLE all_types {
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    type VARCHAR(30) NOT NULL DEFAULT '' COMMENT '类型名',
    primary key(id)
}ENGINE=INNODB DEFAULT CHARSET=utf8;
```

- 数据库表   
存取信息是各db所对应的gid。
```
CREATE TABLE all_dbs {
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    gid INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '组id',
    db VARCHAR NOT NULL DEFAULT '' COMMENT 'db名',
    primary key(id)
}ENGINE=INNODB DEFAULT CHARSET=utf8;
```
该表用来根据数据库名查询其所在的机器。其查询语句为`select gid from all_dbs where db='$DB_NAME'`。

- Group
存储各组，包括自定义的分组。其字段如下：

```
CREATE TABLE groups (
id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(50) NOT NULL DEFAULT '' COMMENT '组名',
type TINYINT NOT NULL DEFAULT 0 COMMENT '表all_types的id',
description VARCHAR(100) NOT NULL DEFAULT '' COMMENT '描述业务', 
scenario VARCHART(500) NOT NULL DEFAULT '' COMMENT '使用场景',
contacts VARCHAR(100) NOT NULL DEFAULT '' COMMENT '联系人', 
updatetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
index idx_type(type)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;
```

查询语句如下：
`SELECT id, name from groups where type='$TYPE';`

- Host
Host表主要存储机器物理方面的性质，其表结构如下：

```
CREATE TABLE hosts (
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
host VARCHAR(32) NOT NULL DEFAULT '' COMMENT '主机名',
cores INT NOT NULL DEFAULT 0 COMMENT 'cpu核数',
memory VARCHAR(30) NOT NULL DEFAULT 0 COMMENT '内存大小'
disk_type VARCHAR(50) NOT NULL DEFAULT '' COMEMNT '磁盘类型', 
disk_num VARCHAR(50) NOT NULL DEFAULT '' COMMENT '磁盘数,若多种类型磁盘，以空格做分隔',
disk_size VARCHAR(50) NOT NULL DEFAULT '' COMMENT '每种类型磁盘总大小，多种类型磁盘，以空格做分隔',
raid  SMALLINT NOT NULL DEFAULT 0 COMMENT '主要磁盘的raid级别，不包括系统盘',
ips VARCHAR(256) NOT NULL DEFAULT '' COMMENT '多个ip使用, 做分隔',
remote_ip VARCHAR(30) NOT NULL DEFAULT '' COMMENT '远程控制卡IP',
idc TINYINT NOT NULL DEFAULT 0 COMMENT '机房位置, IDC10: 0, IDC20: 1',
bbu_relearn_flag TINYINT(1) NOT NULL DEFAULT 0 COMMENT '电池充放电。不手动充放:0，手动充放:1',
bbu_relearn_date DATE NOT NULL DEFAULT '0000-00-00' COMMENT '下次充放电日期',
status TINYINT(1) NOT NULL DEFAULT 0 COMMENT '机器状态。offline:0，online:1',
remark VARCHAR(200) NOT NULL DEFAULT '' COMMENT '机器备注',
updatetime TIMESTAMP NOT NULL DEFAUTL CURRENT_TIMESTAMP ON UP CURRENT_TIMESTAMP
)ENGINE=INNODB DEFAULT CHARSET=UTF8 COMMENT='所有主机相关信息';
```

- mysql
mysql实例表：

```
CREATE TABLE mysql_instances (
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
gid INT NOT NULL DEFAULT 0 COMMENT '组id',
hid INT NOT NULL DEFAULT 0 COMMENT 'host_id',
port SMALLINT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'port号',
ips VARCHAR(256) NOT NULL DEFAULT '' COMMENT 'port对应的ip',
version VARCHAR(10) NOT NULL DEFAULT '' COMMENT '版本',
socket VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'socket pid',
role TINYINT(1) NOT NULL DEFAULT 0 COMMENT '角色。master: 1, slave: 2, backup: 3',
status TINYINT(1) NOT NULL DEFAULT 0 COMMENT '状态。online: 1, offline: 2',
remark VARCHAR(200) NOT NULL DEFAULT '' COMMENT '备注',
updatetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
KEY idx_id(gid, hid)
)ENGINE=INNODB DEFAULT CHARSET=UTF8 COMMENT='所有的实例表';
```

- redis
redis实例表：

```shell
CREATE TABLE redis_instances (
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
gid INT NOT NULL DEFAULT 0 COMMENT '组id',
hid INT NOT NULL DEFAULT 0 COMMENT 'host_id',
port SMALLINT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'port号',
ips VARCHAR(256) NOT NULL DEFAULT '' COMMENT 'port对应的ip',
memory VARCHAR(20) NOT NULL DEFAULT '' COMMENT '分配内存',
version VARCHAR(10) NOT NULL DEFAULT '' COMMENT '版本',
persistence TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否持久化，针对redis。否：0，是：1',
role TINYINT(1) NOT NULL DEFAULT 0 COMMENT '角色。master:1, slave:2, sentinel:3',
status TINYINT(1) NOT NULL DEFAULT 0 COMMENT '状态。online: 1, offline: 2',
remark VARCHAR(200) NOT NULL DEFAULT '' COMMENT '备注',
updatetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
KEY idx_id(gid, hid)
)ENGINE=INNODB DEFAULT CHARSET=UTF8 COMMENT='所有的实例表';
```

- memcached
memcached实例表：

```
CREATE TABLE memcached_instances (
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
gid INT NOT NULL DEFAULT 0 COMMENT '组id',
hid INT NOT NULL DEFAULT 0 COMMENT 'host_id',
port SMALLINT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'port号',
ips VARCHAR(256) NOT NULL DEFAULT '' COMMENT 'port对应的ip',
memory VARCHAR(20) NOT NULL DEFAULT '' COMMENT '分配内存',
version VARCHAR(10) NOT NULL DEFAULT '' COMMENT '版本',
parameters VARCHAR(100) NOT NULL DEFAULT '' COMMENT '命令启动的其他参数',
status TINYINT(1) NOT NULL DEFAULT 0 COMMENT '状态。online: 1, offline: 2',
remark VARCHAR(200) NOT NULL DEFAULT '' COMMENT '备注',
updatetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
KEY idx_id(gid, hid)
)ENGINE=INNODB DEFAULT CHARSET=UTF8 COMMENT='所有的实例表';
```

显示所有实例时，根据`groups`中的结果来查找所有实例，查询语句如下：
`SELECT * from instances where gid=$GROUP.id`。

- 监控表
图表monitor_charts分为三个层次的报警，分别是组，主机，实例，其表结构如下：

```
CREATE TABLE monitor_charts (
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT '图表ID',
chart_name VARCHAR(50) NOT NULL DEFAULT '' COMMENT '图表名称',
gid INT NOT NULL DEFAULT 0 COMMENT 'group id',
sid INT NOT NULL DEFAULT 0 COMMENT '二级id，类似host id，业务id等',
tid INT NOT NULL DEFAULT 0 COMMENT '三级id，类似各instance表id',
contacts VARCHAR(200) NOT NULL DEFAULT '' COMMENT '联系人or接警人邮箱，以 , 做分隔',
alarm_status TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否开启报警。开启：1，关闭：0',
interval INT NOT NULL DEFAULT 1 COMMENT '报警间隔，单位为分',
last INT NOT NULL DEFAULT 0 COMMENT '延时报警，单位为分',
mode TINYINT NOT NULL DEFAULT 0 COMMENT '接警方式，邮件：0，短信：1，微信：2',
threshold VARCAHR(200) NOT NULL DEFAULT '' COMMENT '报警阈值，差值的百分比：1，差值的绝对值：2，极值：3，斜率：4，以json保存',
key idx_id(gid, hid, tid)
)ENGINE=INNODB DEFAULT CHARSET=utf8 COMMENT '监控图表信息'
```

对于上述表结构，`gid`和`tid`联合保证了该行的唯一性，即使mysql和nosql的id相同，但其gid一定不同，因此记录不会是重复的。

- 数据源表
数据源monitor_ds表结构如下：

```
CREATE TABLE monitor_ds (
id  INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT '数据源ID',
name VARCHAR(50) NOT NULL DEFAULT '' COMMENT '数据源名称',
chart_id INT NOT NULL DEFAULT 0 COMMENT 'chart id',
)ENGINE=INNODB DEFAULT CHARSET=utf8 COMMENT '监控数据源的信息表';
```

- 每日数据源表
monitor_ds_YYYYmmdd表结构如下：

```
CREATE TABLE monitor_ds_YYYYmmdd (
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
ds_id INT NOT NULL DEFAULT 0 COMMENT '图表中数据源ID',
value INT NOT NULL DEFAULT 0 COMMENT '数据值',
updatetime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
INDEX idx_1(ds_id, updatetime)
)ENGINE=INNODB DEFAULT CHARSET=UTF8 COMMENT '监控数据源天表';
```
插入语句：  
- `INSERT INTO monitor_ds_YYYYMMDD (ds_id, value, updatetime) VALUES(1000100, 30, '2009-12-12 12:12:00');`
查询语句：  
- `SELECT value FROM monitor_ds_YYYYMMDD where chart_id=1000 and ds_id=1000100 and updatetime>='2009-12-12 12:00:00' and updatetime<='2009-12-12 13:00:00';`

一般而言，对最近1天，最近3天，最近1周，最近1个月，最近1年的查询是较多的，若都是天表，当查询天数越来越多时，需要查询的表也起来越多，响应时间会越来越长。因此对1周，
1个月，1年的情况，还需要单独建表，以提高查询速度，避免浏览器卡死。

- 周数据源表
对天表每隔5分钟偏量提取平均值放入周表中。
```
CREATE TABLE monitor_ds_YYYY_week (
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
ds_id INT NOT NULL DEFAULT 0 COMMENT '图表中数据源ID',
value INT NOT NULL DEFAULT 0 COMMENT '数据值',
updatetime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
INDEX idx_1(ds_id, updatetime)
)ENGINE=INNODB DEFAULT CHARSET=UTF8 COMMENT '监控数据源周表';
```

- 每月数据源表
对天表每隔30分钟偏量提取平均值放入月表中。
monitor_ds_YYYYmm表结构如下：

```
CREATE TABLE monitor_ds_YYYYmmdd (
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
ds_id INT NOT NULL DEFAULT 0 COMMENT '图表中数据源ID',
value INT NOT NULL DEFAULT 0 COMMENT '数据值',
updatetime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
INDEX idx_1(ds_id, updatetime)
)ENGINE=INNODB DEFAULT CHARSET=UTF8 COMMENT '监控数据源的月表';
```

- 年数据源表

对月表每10行提取平均值放入年表中。
```
CREATE TABLE monitor_ds_YYYY (
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
ds_id INT NOT NULL DEFAULT 0 COMMENT '图表中数据源ID',
value INT NOT NULL DEFAULT 0 COMMENT '数据值',
updatetime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
INDEX idx_1(ds_id, updatetime)
)ENGINE=INNODB DEFAULT CHARSET=UTF8 COMMENT '监控数据源年表';
```

- 搜索表
```
CREATE TABLE search (
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
skey VARCHAR(50) NOT NULL DEFAULT '' COMMENT '搜索字段',
value VARCHAR(100) NOT NULL DEFAULT '' COMMENT '搜索结果值',
weight INT NOT NULL DEFAULT 0 COMMENT '搜索权重值',
updatetime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
INDEX idx_1(skey)
)ENGINE=INNODB DEFAULT CHARSET=UTF8 COMMENT '搜索表';
```

对于单字段的查询，直接查询`skey`并返回`value`，`value`应能说明`skey`的大概，然后用户选择`value`后再去查询相关表。
对于多字段的查询，需要将所以查询返回结果求交集。若使用了redis做查询，还需要更新redis。
返回结果根据`weight`来排序。

##### 对于自定义监控的说明

业务发展到后期，对一些自定义监控的需求也会出现的，如监控某业务的情况，监控app机器，监控交换机等等。本系统提供接口做监控报警展示用，各应用方推送数据即可。下面分别说明。

- 对业务的监控展示

业务监控具体可抽象为`部门-->业务-->业务监控项`，其中`部门`项可添加到`group`表中，业务一项可添加到`host`表，也可再新建一张表，这里为统一起见，选择新建表。 
`业务监控项`再新建一张新的业务表。

- app机器监控展示

对于现有cmdb，pool对应group，主机信息对应`host`表，其他类推。

- 交换机监控展示

根据机房和机架来分组，各交换机放入host表，在host级别做监控即可。

### 具体设计
#### 监控

目前监控要展示的图表除了mysql，nosql一些信息外，还需要展示自定义的监控信息。mysql，nosql的组，主机，port好理解，这里说下自定义监控的实现。

自定义监控中不包含M/S这种关系，也不包括除展示字段外的其他信息，其纯粹是数据的展示而已。基本设计思路是有N个基项，如网络，PV等，当需要监控这些基项的数据时，需要创建子项，若子项直接是图表，则创建图表，否则仍可创建子项，直至最后为图表为止。如下：

![self_monitor](images/self_monitor.png)


#### ManagementCenter
ManagementCenter是配置管理中心。

- 查看机器角色
对于Mysql/redis，有Master/Slave之分，且该角色定义在端口上。但对于Hadoop而言，其角色名为NameNode/SecondNameNode/DataNode，一个主机也可同时做NameNode和DataNode，角色定位在主机上。Hbase角色为HMaster/RegionServer，角色定位在主机上。

#### 搜索
搜索常有的几种需求如下：
- 查找db所在的组
- 根据DBRT号查找DBRT
- 查找JOB
- 查看机器的监控
- 查看机器的slow

这里不考虑全文索引。目前所使用的方式是在相应表中再加一个字段，如对于查找db所在组的需求，其实现方法是在group表中加一个`db`字段，用以存放每个group对应的db，查询时使用 `WHERE db LIKE %key%` 的方式来实现。此方案对字段限制过于严格，只能满足对这一字段的搜索，对于其他字段的搜索还需另写SQL语句，不太适合全局搜索。

另外一种方案仍是每个表中再新加一个字段`search_field`，该字段存放的值是每行所有字段（不包括`search`字段本身）的合集，各字段之间以某一个delimiter分隔。查询时使用`WHERE search_field LIKE %key%`来实现。该方法能消除前一方法的限制，但仍有一些缺点。

- 数据冗余
- `LIKE %key%` 不能使用索引，且匹配多余数据，如 `LIKE %property_db%`，除了匹配 `propertys_db`，还会匹配`propertys_db_04`
- 不能满足同时有多个匹配的情况，即使满足多个匹配的情况，但匹配词序固定，对于`condition1 condition2`，只能是`LIKE %condition1%condition2%`，对于`condition2 condition1`的情况无法匹配出来。
- 无法自适应控制结果的重要顺序。对于所有结果返回的顺序一样，无法自适应调整优先级。

还有一种做法是建立一个搜索表，每次增删改时，同时更新搜索表。其方法为将需要搜索的字段都放在该表中，能满足多字段的搜索，同时能做到根据结果重要性排序返回。在使用该方法时，不希望使用 `LIKE`的方式，使用在搜索输入框中会用redis/jquery来做自动完成的功能。该方法的缺点是对于少部分情况会出现搜索不到的情况，不过对于这种情况，可以将待搜索字段加入到搜索表中即可。

当然，还可以开源的一些工具，如 solr, nutch, elasticsearch 等，这些工具对查询级别为千万以上表现良好，但增加了维护成本。

本系统做为内部系统，查询量相较而言不大太，因此这里使用搜索表的方式。

### 类设计
#### Message

`Message`类做为邮件，系统内提示消息等的父类。其类图关系如下：

![message类图](images/message.jpg)

```
Class Message(object):

    """
    All message classes' Base Class
    """

    def __init__(self):
        self._threshold = None
        self._content = None

    def condition(self, v):
        """ send message's trigger condition """
        return v?true:false

    @property
    def threshold(self):
        return self._threhold

    @threshold.setter
    def threshold(self, ts):
        self._threshold = ts

    @property
    def content(self)：
        return self._content

    @content.setter
    def content(self, con):
        self._content = con
        
    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, l):
        self._level = l

    def send(self):
        ...

```

`RemoteMessage`如下:

```
class RemoteMessage(Message):
    """ the message of email, mobile message and webchat etc.."""

    @property
    def mode(self):
        """
        mode: email, mobile message, webchat and so on
        """
        return self._mode

    @mode.setter
    def mode(self, m):
        self._mode = m

    @property
    def method(self):
        """
        method: extremum（极值），scope（范围），gradient（斜率）
        """
        return self._method

    @method.setter
    def method(self, meth):
        return self._method = meth

    @property
    def receiver(self):
        return self._reciver

    @receiver.setter
    def receiver(self, new_receiver):
        self._receiver.add(new_receiver)

    def add_receiver(self, new_receiver):
        receiver.setter(new_receiver)

    @receiver.deleter
    def receiver(self, del_receiver):
        del self._receiver[del_receiver]
```

#### Item 相关

如下图是监控类相关的一些类图：

![item相关类图](images/item.jpg)

### REST API的设计

REST设计中URI为一系列的资源，其通过HTTP方法来表示CRUD（对应POST, GET, PUT, DELETE四个http方法）。这里以monitor模块中的一些需求来说明URL。

- CREATE
在monitor模块下，新建一个组，使用POST方法，对应的RESTful URI为 `http://dba.corp.anjuke.com/monitor/groups`。这里需要注意group使用复数。

- READ
查找monitor中组号为G1，host=db10-001的主机信息，使用GET方法，RESTful URI为 `http://dba.corp.anjuke.com/monitor/mysql/groups/g1/hosts/db10-001`。而对于可选参数的URI，使用key-value的形式传入参数，如`http://dba.corp.anjuke.com/monitor?group=g1&contacts=mingma`。关于 REST API 和 Query String Parameter 的选择，可参考[REST API Best practices: Where to put parameters?](http://stackoverflow.com/questions/4024271/rest-api-best-practices-where-to-put-parameters)。

- UPDATE
更新monitor中组号为G1，host=db10-001的主机信息，使用PUT方法，RESTful URI为 `http://dba.corp.anjuke.com/monitor/mysql/groups/g1/hosts/db10-001`。

- DELETE
删除monitor中组号为G1，host=db10-001的hostname，使用DELETE方法，RESTful URI为 `http://dba.corp.anjuke.com/monitor/mysql/groups/g1/hosts/db10-001/hostname`

对于请求结果状态，使用[HTTP响应码](http://www.restapitutorial.com/httpstatuscodes.html)来表示。在HTTP方法中，GET, PUT, DELETE都是幂等的，对于DELETE方法而言，第二次调用时返回404。

参考
- [REST wiki](zh.wikipedia.org/zh/REST)
- [REST API](http://www.restapitutorial.com/)
- [django-rest-framework](http://www.django-rest-framework.org/)



