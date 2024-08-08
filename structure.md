## 平台搭建

##### 任务一：大数据平台搭建

本搭建模块对应虚拟机为：master、slave1、slave2
相关压缩包路径为：`/root/software/package`，对应的安装路径为`/root/software/`

修改主机名

```shell
 hostnamectl set-hostname master && bash
```



```shell
 hostnamectl set-hostname slave1 && bash
```

```
 hostnamectl set-hostname slave2 && bash
```



配置内网地址

```shell
echo "
172.18.12.43 master
172.18.12.41 slave1
172.18.12.40 slave2" >> /etc/hosts
```



解压缩jdk

```
tar -xzvf /root/software/package/jdk-8u212-linux-x64.tar.gz -C /root/software/
```

解压hadoop

```
tar -xzvf /root/software/package/hadoop-3.1.3.tar.gz -C /root/software/
```

在master上生成免密登陆

```
ssh-keygen
```

```shell
 ssh-copy-id -i /root/.ssh/id_rsa.pub master
  ssh-copy-id -i /root/.ssh/id_rsa.pub slave1
  ssh-copy-id -i /root/.ssh/id_rsa.pub slave2
```

分发jdk

```
scp -r /root/software/jdk1.8.0_212 root@slave1:/root/software/
scp -r /root/software/jdk1.8.0_212 root@slave1:/root/software/
```



配置jdk环境变量

```
vim /etc/profile
export JAVA_HOME=/root/software/jdk1.8.0_212
export PATH=$PATH:$JAVA_HOME/bin
source /etc/profile
```

分发jdk环境变量

```
scp -r /etc/profile root@slave1:/etc/profile
scp -r /etc/profile root@slave2:/etc/profile
```

hadoop配置

```
echo "export JAVA_HOME=/root/software/jdk1.8.0_212" >> /root/software/hadoop-3.1.3/etc/hadoop/hadoop-env.sh
```

配置 core-site.xml

```
vim /root/software/hadoop-3.1.3/etc/hadoop/core-site.xml
```

```
<property>
 <name>fs.defaultFS</name>
 <value>hdfs://master:9000</value>
</property>
<property>
 <name>hadoop.tmp.dir</name>
 <value>/root/software/hadoop-3.1.3/data</value>
</property>
<property>
 <name>hadoop.security.authorization</name>
 <value>true</value>
</property>
```

配置hdfs-site.xml

```
vim /root/software/hadoop-3.1.3/etc/hadoop/hdfs-site.xml
```

```
<property>
 <name>dfs.namenode.http-address</name>
 <value>master:9870</value>
</property>
<property>
 <name>dfs.replication</name>
 <value>3</value>
</property>
<property>
 <name>dfs.permissions.enabled</name>
 <value>true</value>
</property>
<property>
 <name>dfs.permissions.superusergroup</name>
 <value>root</value>
</property>
```

配置mapred-site.xml

```
vim /root/software/hadoop-3.1.3/etc/hadoop/mapred-site.xml
```

```
<property>
 <name>mapreduce.framework.name</name>
 <value>yarn</value>
</property>
<property>
 <name>yarn.app.mapreduce.am.env</name>
 <value>HADOOP_MAPRED_HOME=/root/software/hadoop-3.1.3</value>
</property>
<property>
 <name>mapreduce.map.env</name>
 <value>HADOOP_MAPRED_HOME=/root/software/hadoop-3.1.3</value>
</property>
<property>
 <name>mapreduce.reduce.env</name>
 <value>HADOOP_MAPRED_HOME=/root/software/hadoop-3.1.3</value>
</property>
```

配置yarn-site.xml

```
vim /root/software/hadoop-3.1.3/etc/hadoop/yarn-site.xml
```

```
<property>
 <name>yarn.nodemanager.aux-services</name>
 <value>mapreduce_shuffle</value>
</property>
<property>
 <name>yarn.resourcemanager.hostname</name>
 <value>master</value>
</property>
<property>
 <name>yarn.nodemanager.env-whitelist</name>
 <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME</value>
</property>
```

修改 workers 配置文件

```
echo "master
slave1
slave2" > /root/software/hadoop-3.1.3/etc/hadoop/workers
```

修改 hadoop-policy.xml 服务认证配置文件（授予只有root用户才可操作的权限，直接替换整个文件！！！）

```
[root@master hadoop]# touch policy-bak.xml
[root@master hadoop]# vim policy-bak.xml
[root@master hadoop]# mv hadoop-policy.xml policy-bak1.xml
[root@master hadoop]# mv policy-bak.xml hadoop-policy.xml
[root@master hadoop]# ll hadoop-policy.xml
```

```xml
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<!--
      
 Licensed to the Apache Software Foundation (ASF) under one
 or more contributor license agreements.  See the NOTICE file
 distributed with this work for additional information
 regarding copyright ownership.  The ASF licenses this file
 to you under the Apache License, Version 2.0 (the
 "License"); you may not use this file except in compliance
 with the License.  You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.

-->

<!-- Put site-specific property overrides in this file. -->

<configuration>
  <property>
    <name>security.client.protocol.acl</name>
    <value>root</value>
    <description>ACL for ClientProtocol, which is used by user code
    via the DistributedFileSystem.
    The ACL is a comma-separated list of user and group names. The user and
    group list is separated by a blank. For e.g. "alice,bob users,wheel".
    A special value of "*" means all users are allowed.</description>
  </property>

  <property>
    <name>security.client.datanode.protocol.acl</name>
    <value>root</value>
    <description>ACL for ClientDatanodeProtocol, the client-to-datanode protocol
    for block recovery.
    The ACL is a comma-separated list of user and group names. The user and
    group list is separated by a blank. For e.g. "alice,bob users,wheel".
    A special value of "*" means all users are allowed.</description>
  </property>

  <property>
    <name>security.datanode.protocol.acl</name>
    <value>root</value>
    <description>ACL for DatanodeProtocol, which is used by datanodes to
    communicate with the namenode.
    The ACL is a comma-separated list of user and group names. The user and
    group list is separated by a blank. For e.g. "alice,bob users,wheel".
    A special value of "*" means all users are allowed.</description>
  </property>

  <property>
    <name>security.inter.datanode.protocol.acl</name>
    <value>root</value>
    <description>ACL for InterDatanodeProtocol, the inter-datanode protocol
    for updating generation timestamp.
    The ACL is a comma-separated list of user and group names. The user and
    group list is separated by a blank. For e.g. "alice,bob users,wheel".
    A special value of "*" means all users are allowed.</description>
  </property>

  <property>
    <name>security.namenode.protocol.acl</name>
    <value>*</value>
    <description>ACL for NamenodeProtocol, the protocol used by the secondary
    namenode to communicate with the namenode.
    The ACL is a comma-separated list of user and group names. The user and
    group list is separated by a blank. For e.g. "alice,bob users,wheel".
    A special value of "*" means all users are allowed.</description>
  </property>

 <property>
    <name>security.admin.operations.protocol.acl</name>
    <value>*</value>
    <description>ACL for AdminOperationsProtocol. Used for admin commands.
    The ACL is a comma-separated list of user and group names. The user and
    group list is separated by a blank. For e.g. "alice,bob users,wheel".
    A special value of "*" means all users are allowed.</description>
  </property>

  <property>
    <name>security.refresh.user.mappings.protocol.acl</name>
    <value>*</value>
    <description>ACL for RefreshUserMappingsProtocol. Used to refresh
    users mappings. The ACL is a comma-separated list of user and
    group names. The user and group list is separated by a blank. For
    e.g. "alice,bob users,wheel".  A special value of "*" means all
    users are allowed.</description>
  </property>

  <property>
    <name>security.refresh.policy.protocol.acl</name>
    <value>*</value>
    <description>ACL for RefreshAuthorizationPolicyProtocol, used by the
    dfsadmin and mradmin commands to refresh the security policy in-effect.
    The ACL is a comma-separated list of user and group names. The user and
    group list is separated by a blank. For e.g. "alice,bob users,wheel".
    A special value of "*" means all users are allowed.</description>
  </property>

  <property>
    <name>security.ha.service.protocol.acl</name>
    <value>*</value>
    <description>ACL for HAService protocol used by HAAdmin to manage the
      active and stand-by states of namenode.</description>
  </property>

  <property>
    <name>security.zkfc.protocol.acl</name>
    <value>*</value>
    <description>ACL for access to the ZK Failover Controller
    </description>
  </property>

  <property>
    <name>security.qjournal.service.protocol.acl</name>
    <value>*</value>
    <description>ACL for QJournalProtocol, used by the NN to communicate with
    JNs when using the QuorumJournalManager for edit logs.</description>
  </property>

  <property>
    <name>security.interqjournal.service.protocol.acl</name>
    <value>*</value>
    <description>ACL for InterQJournalProtocol, used by the JN to
    communicate with other JN
    </description>
  </property>

  <property>
    <name>security.mrhs.client.protocol.acl</name>
    <value>*</value>
    <description>ACL for HSClientProtocol, used by job clients to
    communciate with the MR History Server job status etc. 
    The ACL is a comma-separated list of user and group names. The user and
    group list is separated by a blank. For e.g. "alice,bob users,wheel".
    A special value of "*" means all users are allowed.</description>
  </property>

  <!-- YARN Protocols -->

  <property>
    <name>security.resourcetracker.protocol.acl</name>
    <value>*</value>
    <description>ACL for ResourceTrackerProtocol, used by the
    ResourceManager and NodeManager to communicate with each other.
    The ACL is a comma-separated list of user and group names. The user and
    group list is separated by a blank. For e.g. "alice,bob users,wheel".
    A special value of "*" means all users are allowed.</description>
  </property>

  <property>
    <name>security.resourcemanager-administration.protocol.acl</name>
    <value>*</value>
    <description>ACL for ResourceManagerAdministrationProtocol, for admin commands. 
    The ACL is a comma-separated list of user and group names. The user and
    group list is separated by a blank. For e.g. "alice,bob users,wheel".
    A special value of "*" means all users are allowed.</description>
  </property>

  <property>
    <name>security.applicationclient.protocol.acl</name>
    <value>root</value>
    <description>ACL for ApplicationClientProtocol, used by the ResourceManager 
    and applications submission clients to communicate with each other.
    The ACL is a comma-separated list of user and group names. The user and
    group list is separated by a blank. For e.g. "alice,bob users,wheel".
    A special value of "*" means all users are allowed.</description>
  </property>

  <property>
    <name>security.applicationmaster.protocol.acl</name>
    <value>*</value>
    <description>ACL for ApplicationMasterProtocol, used by the ResourceManager 
    and ApplicationMasters to communicate with each other.
    The ACL is a comma-separated list of user and group names. The user and
    group list is separated by a blank. For e.g. "alice,bob users,wheel".
    A special value of "*" means all users are allowed.</description>
  </property>

  <property>
    <name>security.containermanagement.protocol.acl</name>
    <value>*</value>
    <description>ACL for ContainerManagementProtocol protocol, used by the NodeManager 
    and ApplicationMasters to communicate with each other.
    The ACL is a comma-separated list of user and group names. The user and
    group list is separated by a blank. For e.g. "alice,bob users,wheel".
    A special value of "*" means all users are allowed.</description>
  </property>

  <property>
    <name>security.resourcelocalizer.protocol.acl</name>
    <value>*</value>
    <description>ACL for ResourceLocalizer protocol, used by the NodeManager 
    and ResourceLocalizer to communicate with each other.
    The ACL is a comma-separated list of user and group names. The user and
    group list is separated by a blank. For e.g. "alice,bob users,wheel".
    A special value of "*" means all users are allowed.</description>
  </property>

  <property>
    <name>security.job.task.protocol.acl</name>
    <value>*</value>
    <description>ACL for TaskUmbilicalProtocol, used by the map and reduce
    tasks to communicate with the parent tasktracker.
    The ACL is a comma-separated list of user and group names. The user and
    group list is separated by a blank. For e.g. "alice,bob users,wheel".
    A special value of "*" means all users are allowed.</description>
  </property>

  <property>
    <name>security.job.client.protocol.acl</name>
    <value>*</value>
    <description>ACL for MRClientProtocol, used by job clients to
    communciate with the MR ApplicationMaster to query job status etc. 
    The ACL is a comma-separated list of user and group names. The user and
    group list is separated by a blank. For e.g. "alice,bob users,wheel".
    A special value of "*" means all users are allowed.</description>
  </property>

  <property>
    <name>security.applicationhistory.protocol.acl</name>
    <value>*</value>
    <description>ACL for ApplicationHistoryProtocol, used by the timeline
    server and the generic history service client to communicate with each other.
    The ACL is a comma-separated list of user and group names. The user and
    group list is separated by a blank. For e.g. "alice,bob users,wheel".
    A special value of "*" means all users are allowed.</description>
  </property>

  <property>
    <name>security.collector-nodemanager.protocol.acl</name>
    <value>*</value>
    <description>ACL for CollectorNodemanagerProtocol, used by nodemanager
    if timeline service v2 is enabled, for the timeline collector and nodemanager
    to communicate with each other.
    The ACL is a comma-separated list of user and group names. The user and
    group list is separated by a blank. For e.g. "alice,bob users,wheel".
    A special value of "*" means all users are allowed.</description>
  </property>

  <property>
    <name>security.applicationmaster-nodemanager.applicationmaster.protocol.acl</name>
    <value>*</value>
    <description>ACL for ApplicationMasterProtocol, used by the Nodemanager
        and ApplicationMasters to communicate.
        The ACL is a comma-separated list of user and group names. The user and
        group list is separated by a blank. For e.g. "alice,bob users,wheel".
        A special value of "*" means all users are allowed.</description>
  </property>

  <property>
    <name>security.distributedscheduling.protocol.acl</name>
    <value>*</value>
    <description>ACL for DistributedSchedulingAMProtocol, used by the Nodemanager
        and Resourcemanager to communicate.
        The ACL is a comma-separated list of user and group names. The user and
        group list is separated by a blank. For e.g. "alice,bob users,wheel".
        A special value of "*" means all users are allowed.</description>
    </property>
</configuration>
```

分发hadoop

```
scp -r /root/software/hadoop-3.1.3 root@slave1:/root/software/
scp -r /root/software/hadoop-3.1.3 root@slave2:/root/software/
```



配置hadoop环境变量

```
vim /etc/profile
```

```
export HADOOP_HOME=/root/software/hadoop-3.1.3
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export HADOOP_CLASSPATH=$(hadoop classpath)
export HDFS_NAMENODE_USER=root
export HDFS_DATANODE_USER=root
export HDFS_SECONDARYNAMENODE_USER=root
export YARN_RESOURCEMANAGER_USER=root
export YARN_NODEMANAGER_USER=root
export HDFS_JOURNALNODE_USER=root
export HDFS_ZKFC_USER=root
```

分发环境变量配置文件

 ```
 scp /etc/profile root@slave1:/etc/profile
 scp /etc/profile root@slave2:/etc/profile
 ```

使三台机器的环境变量生效

```
[root@master hadoop]# source /etc/profile
[root@master hadoop]# ssh slave1
Last login: Sun Aug  4 11:22:48 2024 from 172.18.12.43

Welcome to Alibaba Cloud Elastic Compute Service !

[root@slave1 ~]# source /etc/profile
[root@slave1 ~]# exit
登出
Connection to slave1 closed.
[root@master hadoop]# ssh slave2
Last login: Sun Aug  4 11:10:16 2024 from 182.88.142.119

Welcome to Alibaba Cloud Elastic Compute Service !

[root@iZ2zeifjpad6pqi71q7j8uZ ~]# source /etc/profile
[root@iZ2zeifjpad6pqi71q7j8uZ ~]#
```



格式化文件系统（在master节点执行）

```
hdfs namenode -format
```

启动集群（在master节点执行）

```shell
# 开启集群

start-all.sh

# 启动 hdfs

 start-dfs.sh

# 启动 yarn

 start-yarn.sh

# 启动历史服务器

 mr-jobhistory-daemon.sh start historyserver
```



##### 子任务二：MySQL安装配置

```shell
# 解压数据库
tar -xvf /root/software/package/mysql-5.7.25-1.el7.x86_64.rpm-bundle.tar -C /root/software/
# 删除依赖库
yum remove -y mariadb-libs
# 安装mysql各个组件
cd /root/software/
rpm -ivh mysql-community-common-5.7.25-1.el7.x86_64.rpm 
rpm -ivh mysql-community-libs-5.7.25-1.el7.x86_64.rpm
rpm -ivh mysql-community-libs-compat-5.7.25-1.el7.x86_64.rpm
rpm -ivh mysql-community-client-5.7.25-1.el7.x86_64.rpm
rpm -ivh mysql-community-server-5.7.25-1.el7.x86_64.rpm
# 初始化
/usr/sbin/mysqld --initialize-insecure --console --user=mysql
# 启动服务
systemctl start mysqld.service
# 进入数据库（自行修改密码及权限，注意刷新权限）
mysql -uroot

# 修改用户密码
mysql> alter user 'root'@'localhost' identified by '123456';
Query OK, 0 rows affected (0.00 sec)
# 修改远程登录权限
mysql> update mysql.user set host='%' where host='localhost';
Query OK, 3 rows affected (0.00 sec)
Rows matched: 3  Changed: 3  Warnings: 0
# 刷新权限
mysql> flush privileges;
Query OK, 0 rows affected (0.00 sec)
# 退出
mysql> exit;
```



##### 子任务三：Hive安装配置

```shell
# 解压安装包
tar -xzvf /root/software/package/apache-hive-3.1.2-bin.tar.gz -C /root/software/
# 设置环境变量
# 编辑
vim /etc/profile
# 文件底部追加以下内容：
export HIVE_HOME=/root/software/apache-hive-3.1.2-bin
export PATH=$PATH:$HIVE_HOME/bin

# 生效环境变量
source /etc/profile

# 查看hive版本
hive --version

# 配置相关文件，添加依赖包
# hive-env.sh 配置文件
cd /root/software/apache-hive-3.1.2-bin/conf
mv hive-env.sh.template hive-env.sh
# 相关配置直接追加到 hive-env.sh 文件
echo "
HADOOP_HOME=/root/software/hadoop-3.1.3
export HIVE_CONF_DIR=/root/software/apache-hive-3.1.2-bin/conf
export HIVE_AUX_JARS_PATH=/root/software/apache-hive-3.1.2-bin/lib" >> /root/software/apache-hive-3.1.2-bin/conf/hive-env.sh

# 配置 hive-site.xml 文件
vim /root/software/apache-hive-3.1.2-bin/conf/hive-site.xml

<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
<property>
 <name>javax.jdo.option.ConnectionURL</name>
 <value>jdbc:mysql://master:3306/hivedb?createDatabaseIfNotExist=true&amp;useSSL=false&amp;useUnicode=true&amp;characterEncoding=UTF-8</value>
</property>
<property>
 <name>javax.jdo.option.ConnectionDriverName</name>
 <value>com.mysql.jdbc.Driver</value>
</property>
<property>
 <name>javax.jdo.option.ConnectionUserName</name>
 <value>root</value>
</property>
<property>
 <name>javax.jdo.option.ConnectionPassword</name>
 <value>123456</value>
</property>
</configuration>

# 添加 mysql-connector 驱动
cp /root/software/package/mysql-connector-java-5.1.47-bin.jar  /root/software/apache-hive-3.1.2-bin/lib/

# 初始化元数据库
schematool -dbType mysql -initSchema
```

##### 子任务一：创建数据库及相关数据表

```shell
(base) [root@iZ2zeajfihj3uxpzya8rw0Z ~]# systemctl start mysqld.service
(base) [root@iZ2zeajfihj3uxpzya8rw0Z ~]# mysql -uroot -p123456
```

```sql
CREATE DATABASE test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS fooditems (  
    id INT AUTO_INCREMENT PRIMARY KEY,  
    city VARCHAR(255) NOT NULL,  
    food_name VARCHAR(255) NOT NULL,  
    likelihood_of_liking INT,  
    restaurant_list TEXT,  
    food_detail_link TEXT,  
    food_image_link TEXT,  
    food_description TEXT  
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS shopping (  
    id INT AUTO_INCREMENT PRIMARY KEY,  
    city VARCHAR(255) NOT NULL,  
    shop_name VARCHAR(500) NOT NULL,  
    address VARCHAR(50) NOT NULL,  
    contact_phone VARCHAR(100),  
    business_hours VARCHAR(100),  
    ranking VARCHAR(100),  
    overall_rating VARCHAR(50),  
    reviews_count VARCHAR(50),  
    review_category VARCHAR(100),  
    visitor_rating VARCHAR(100),  
    visitor_review TEXT  
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

##### 子任务二：添加数据记录

```sql
load data local infile '/root/travel/hotel/shopping.csv'
into table shopping fields terminated  by ',' 
lines terminated by '\n'
ignore 1 rows ;


load data local infile '/root/travel/hotel/fooditems.csv'
into table fooditems fields terminated  by ',' 
lines terminated by '\n'
ignore 1 rows ;
```



```sql
CREATE VIEW view_table01 AS  
SELECT   
    visitor_rating AS '环境评分'  
FROM   
    shopping  
WHERE   
    shop_name = '果戈里书店';
    
    
    CREATE VIEW view_table02 AS  
SELECT   
    COUNT(DISTINCT food_name) AS '美食个数'  
FROM   
    fooditems  
WHERE   
    city = '北京';
```

```sql
ALTER TABLE shopping ADD overall_rating_new varchar (255) ;
UPDATE shopping SET overall_rating_new=SUBSTRING(overall_rating,1,LOCATE('分',overall_rating)-1);

create view view_table03 as 
select count(*)  '个数'
from shopping
where overall_rating_new > 4.5 and ranking != '';

create view view_table04 as
select city from fooditems where food_name='麻豆腐'
```



## 数据获取与处理

##### 任务一：数据获取与清洗

```
hadoop fs -mkdir /file2_1

(base) [root@bigdata ~]# hadoop fs -chmod 777 /file2_1
(base) [root@bigdata ~]# hadoop fs -get /file2_1 /root
```



