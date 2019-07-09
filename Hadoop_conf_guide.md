# Build Hadoop/MapReduce Cluster

## 1.Configuring nodes
### 1.Add hadoop user to every node.
#### 1.Add hadoop user
```sh
$ sudo adduser hadoop
Enter new UNIX password:
Retype new UNIX password:
passwd: password updated successfully
```
#### 2.Change to hadoop user
```sh
$ su hadoop
Password:
hadoop@master ~ $
```
#### 3.Grant root privileges
```sh
hadoop@master ~ $ su #change to root
[master] chmod 777 /etc/sudoers
# add "hadoop hadoop ALL=(ALL:ALL) ALL" at the end of file
[master] chmod 440 /etc/sudoers
```
### 2.Configuring hostname of every node
#### 1.Change hostname
```sh
hadoop@master $ su
Password：
[master] hostname <name>
```
### 3. Configuring hosts
#### 1.Change to hadoop user and edit hosts file
```sh
hadoop@master ~ $ sudo vim /etc/hosts
# add IP address and name at the end of file
# Save and exit
```
For example:
```sh
127.0.0.1           localhost   #MasterNode
***.***.***.***     master      #MasterNode
***.***.***.***     lcc         #WorkerNode
***.***.***.***     yyt         #WorkerNode
```

### 4.Install JDK on every nodes
#### 1.Check JDK version and install
```sh
hadoop@master ~$ java -version
```
Check the version message like:
```sh
openjdk version "1.8.0_212"
OpenJDK Runtime Environment (build 1.8.0_212-8u212-b03-
0ubuntu1.16.04.1-b03)
OpenJDK 64-Bit Server VM (build 25.212-b03, mixed mode)
```

If jdk is not installed, Download java-8-*.gz and run following command:

```sh
hadoop@master ~$     tar -xvf java-8-*.gz
```
#### 2.Configuring java environment variables
Find java enviroment variable path:
```sh
hadoop@master ~$ echo $JAVA_HOME
/usr/lib/jvm/java-8-openjdk-amd64 #java path
```
If nothing appers, you should manually add java environment variables to your shell profile.

For example,
```sh
hadoop@master ~$ sudo vim .zshrc # .bashrc if you use bash
# Add following code at the end of file
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64 #<your java home path>
export PATH=$JAVA_HOME/bin:$PATH
```

### 5.Configure password-free login to Workers node

#### 1.Generate and handoff keys
```sh
hadoop@master ~ $ ssh-keygen -t rsa # Generate keys

# Append Public key to the end of authorized_keys
hadoop@master ~$ cat ~/.ssh/id_rsa.pub >>~/.ssh/authorized_keys 
hadoop@master ~$ cd .ssh
hadoop@master ~/.ssh $ sudo chmod 644 authorized_keys #Change privilage of authorized_keys
hadoop@master ~/.ssh $ scp authorized_keys hadoop@lcc:~/ # Copy keys to every Worker node

# Change to Worker terminal:
# Check there is no former authorized_keys file
hadoop@lcc ~ $ mv authorized_keys ~ /.ssh/

# Generate keys on worker nodes, change privilage of authorized_keys
hadoop@lcc ~ $ ssh-keygen -t rsa
hadoop@lcc ~/.ssh $ sudo chmod 600 authorized_keys

# Change privilage of .ssh to 755, /home/hadoop to 700
# Otherwise keys are not able to be read
hadoop@lcc ~ $ sudo chmod 755 .ssh
hadoop@lcc / $ sudo chmod 700 /home/hadoop
```

#### 2.Check whether password-free login works
```sh
hadoop@master ~$ ssh lcc
# If you are not asked to enter password, it should be works well.
```

### 6.Configuring Hadoop cluster

#### 1.Download hadoop source files from https://hadoop.apache.org/releases.html
**Since the latest version is extremely lacking in documentation, it is not recommended to download the latest version. I spent a lot of time configuring the latest version.**
**Following process is based on latest version hadoop-3.2.0**

#### 2.Extract the compression package
Since the hadoop is large, it is not recommended to put it in the home directory.You can extract the package to external hard disk and build a soft-connection to the home directory.
```sh
hadoop@master ~$ cd <path to external hard disk>
hadoop@master ~<path to external hard disk> $ tar -xvf ~/hadoop-3.2.0tar.gz
hadoop@master ~<path to external hard disk>$ cd
hadoop@master ~$ ln -s <path to hadoop home> hadoop-3.2.0
# The hadoop file on the external hard disk can be accessed in the home/hadoop/
# but it does not occupy the main system hard disk space.
hadoop@master ~$ cd /home/hadoop/hadoop-3.2.0/
hadoop@master ~$ ls
# You will see following files  if extract successful
bin  lib	  LICENSE.txt  NOTICE.txt  sbin 
etc  include	 libexec  logs	       README.txt  share  
```
#### 3.Configuring environments variable hadoop-env.sh
Run following command:
```sh
hadoop@master ~$ sudo vim /home/hadoop/hadoop-3.2.0/etc/hadoop/hadoop-env.sh
```
Find the following codes:
```sh
export JAVA_HOME=${JAVA_HOME}
# Replace ${JAVA_HOME} by your java home, save and exit
```
#### 4.Configuring yarn-env.sh
Run following command:
```sh
hadoop@master ~$ sudo vim /home/hadoop/hadoop-3.2.0/etc/hadoop/yarn-env.sh
```
Find the following codes:
```sh
export JAVA_HOME=${JAVA_HOME}
# Replace ${JAVA_HOME} by your java home, save and exit
```
#### 5.Configuring core-site.xml
This file is used to configure the file system that manages hadoop -- HDFS.
Run following command:
```sh
hadoop@master ~$ sudo vim /home/hadoop/hadoop-3.2.0/etc/hadoop/core-site.xml
```
This is my configuration:

```sh
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://master:9800</value>
    </property>
    
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/home/hadoop/hadoop-3.2.0/hadoopdata</value>
    </property>
</configuration>
```

* The value of `fs.defaultFS` is the webUI address of HDFS file system.`master` is the hostname of masternode.`9800` is the port number, which can be set arbitrarily.
* `hadoop.tmp.dir` is the directory which is used to store temporary file of hadoop.Before it works, it should be created first.

#### 6.Configuring hdfs-site.xml
This file is used to configure the properties of the HDFS file sytem.
Run following command:
```sh
hadoop@master ~$ sudo vim /home/hadoop/hadoop-3.2.0/etc/hadoop/core-site.xml
```
Here is my configuration:
```sh
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.storage.policy.satisfier.retry.max.attempts</name>
        <value>100</value>
        <final>false</final>
        <source>hdfs-default.xml</source>
    </property>
</configuration>
```

* The value of `dfs.replication` is `1`, which is used to control the number of copy in every datanode.
* The value of `dfs.storage.policy.satisfier.retry.max.attempts` is `100`,Which is used to control the number of reconnection after a datanode disconneted.

#### 7.Configuring yarn-site.xml
This file is used to configure the mapping ports for various log files.
Run following command:
```sh
hadoop@master ~$ sudo vim /home/hadoop/hadoop-3.2.0/etc/hadoop/yarn-site.xml
```
Here is my configuration:
```sh
<configuration>
    <property>
        <name>yarn.resourcemanager.address</name>
        <value>master:18040</value>
    </property>
    <property>
        <name>yarn.resourcemanager.scheduler.address</name>
        <value>master:18030</value>
    </property>
    <property>
        <name>yarn.resourcemanager.resource-tracker.address</name>
        <value>master:18025</value>
    </property>
    <property>
        <name>yarn.resourcemanager.admin.address</name>
        <value>master:18141</value>
    </property>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
        <value>org.apache.hadoop.mapred.ShuffleHandler</value>
    </property>
    <property>
        <name>yarn.nodemanager.disk-health-checker.max-disk-utilization-per-disk-
        percentage</name>
        <value>99</value>
    </property>
    <property>
        <name>yarn.scheduler.minimum-allocation-mb</name>
        <value>1</value>
    </property>
    <property>
        <name>yarn.scheduler.maximum-allocation-mb</name>
        <value>8192</value>
    </property>
    <property>
        <name>yarn.nodemanager.resource.memory-mb</name>
        <value>20480</value>
    </property>
</configuration>
```
* `yarn.resourcemanager.address` is the webUI address of hadoop computing resource management system.`master:18040` is the hostname and the port number of master node.The port number can be set arbitrarily.
* `yarn.resourcemanager.scheduler.address` is the webUI address of hadoop computing resource scheduling management system.
* `yarn.resourcemanager.resource-tracker.address` is the webUI address of hadoop task tracker.
* `yarn.resourcemanager.admin.address` is the webUI address of tasks management.
* `yarn.nodemanager.disk-health-checker.max-disk-utilization-per-disk-
percentage` is a threshold which is used to determinate whether the available space of disk is sufficient.If not, datanode will be set on safemode.
* `yarn.scheduler.minimum-allocation-mb` is the minimum value of  space that can be allocated to cantainer.
* `yarn.scheduler.maximum-allocation-mb` is the maximum value of  space that can be allocated to cantainer.
* `yarn.nodemanager.resource.memory-mb` is the size of the memory space available to each node.
* `yarn.application.classpath` is class address of yarn application.Each machine is different, just fill in the address on the master node.

#### 8.Configuring mapred-site.xml

This file is used to configure hadoop computing yarn system framwork.
We need to copy mapred-site-template.xml as mapred-site.xml:
```sh
hadoop@master ~$ cd /home/hadoop/hadoop-3.2.0/etc/hadoop
hadoop@master ~$ cp mapred-site-template.xml mapred-site.xml
hadoop@master ~$ sudo vim mapred-site.xml
```
Here is my configuration:
```sh
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
    <property>
        <name>yarn.app.mapreduce.am.env</name>
        <value>HADOOP_MAPRED_HOME=/home/hadoop/hadoop-
3.2.0/hadoopdata</value>
    </property>
    <property>
        <name>mapreduce.map.env</name>
        <value>HADOOP_MAPRED_HOME=/home/hadoop/hadoop-
3.2.0/hadoopdata</value>
    </property>
    <property>
        <name>mapreduce.reduce.env</name>
        <value>HADOOP_MAPRED_HOME=/home/hadoop/hadoop-
3.2.0/hadoopdata</value>
    </property>
    <property>
        <name>mapreduce.jobhistory.address</name>
        <value>master:10020</value>
    </property>
    <property>
        <name>mapreduce.jobhistory.webapp.address</name>
        <value>master:19888</value>
    </property>
    <property>
        <name>yarn.app.mapreduce.am.command-opts</name>
        <value>-Xmx983m</value>
    </property>
    <property>
        <name>mapreduce.map.memory.mb</name>
        <value>8192</value>
    </property>
    <property>
        <name>mapreduce.reduce.memory.mb</name>
        <value>8192</value>
    </property>
    <property>
        <name>mapreduce.map.java.opts</name>
        <value>-Xmx983m</value>
    </property>
    <property>
        <name>mapreduce.reduce.java.opts</name>
        <value>-Xmx983m</value>
    </property>
</configuration>
```

* `mapreduce.framework.name` means using yarn system framwork.
* `HADOOP_MAPRED_HOME` is the temporary directory that we created earlier.
* `mapreduce.map.memory.mb` is the memory that schedulr allocated to datanode during map process.
* `mapreduce.reducememory.mb `is the memory that schedulr allocated to datanode during reduce process.

#### 9.Configuring workers file.
Run following command:
```sh
hadoop@master ~$ cd /home/hadoop/hadoop-3.2.0/etc/hadoop/
hadoop@master ~$ sudo vim workers
```
Fill the workers file with IP address of datanode.Since we have set the mapping rules between IP address and IP name, we can just write the name.
```sh
lcc
yyt
#save and exit
```
#### 10.Distribute the configured hadoop to each worker node.
Run following command:
```sh
hadoop@master ~$ cd /home/hadoop/
hadoop@master ~$ scp -r hadoop-3.2.0 lcc:<external hard disk>

# Switch to lcc
hadoop@lcc ~$ cd
hadoop@lcc ~$ ln -s <external hard disk> hadoop-3.2.0

hadoop@master ~$ cd /home/hadoop/
hadoop@master ~$ scp -r hadoop-3.2.0 yyt:<external hard disk>

# Switch to yyt
hadoop@yyt ~$ cd
hadoop@yyt ~$ ln -s <external hard disk> hadoop-3.2.0

#The same scp operation to other datanodes
...
```
### 7.Start hadoop cluster
#### 1.Configuring hadoop environment variables on every node.

```sh

# open shell profile,zsh is .zshrc, bash is .bashrc.
hadoop@master ~$ sudo vim .zshrc
# Add following codes.
export HADOOP_HOME=/home/hadoop/hadoop-3.2.0
export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH
#Make variables take effect
hadoop@master ~$ source .zshrc
```

#### 2.Format the hdfs file system.
Run following command on masternode.
```sh
hadoop@master ~$ hdfs namenode -format
```