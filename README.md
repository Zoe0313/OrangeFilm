# 橙子电影网 - 前后端分离项目部署

### 1、选择自己喜欢的云服务器
	因为是练手项目，我选择的是腾讯云服务器，免费15天体验版。
	微信登录的话需要重置密码，重新登录后就可以看到Linux终端界面了。
	这是一个纯净版的ubuntu。

### 2、安装配置运行环境

- 安装pip3并更新版本
```shell
	sudo apt-get install python3-pip
	pip3 install --upgrade pip
```
- 修改pip3文件
```shell
	sudo vi /usr/bin/pip3
```
```python
from pip import __main__

if __name__ == '__main__'：
    sys.exit(__main__._main())
```
	这样就能顺利使用pip3了。

- 安装Django
```shell
	sudo pip3 install Django==1.11.8
```
- 安装jwt
```shell
	sudo pip3 install pyjwt
```
- 安装uwsgi
```shell
	sudo pip3 install uwsgi
```
- 安装pymql
```shell
	sudo pip3 install pymysql
```
- 因为直接pip3下载安装cors会强制升级Django版本，所以手动官网下载django-cors-headers-3.0.2.tar
```shell
	wget https://files.pythonhosted.org/packages/6b/17/bdd7e2610d5c5b36194524926e4b00abc7113f968d4614c4ff98f2d74737/django-cors-headers-3.0.2.tar.gz
```
- 下载文件到当前路径后，解压安装：
```shell
	tar -zxvf django-cors-headers-3.0.2.tar
	cd django-cors-headers-3.0.2
	sudo python3 setup.py install
```
- 安装nginx
```shell
	sudo apt-get install nginx
```
- 安装mysql
```shell
	sudo apt-get install mysql-server
```
- 初始化mysql配置
```shell
	sudo mysql_secure_installation
```
```shell
	#1
	VALIDATE PASSWORD PLUGIN can be used to test passwords...
	Press y|Y for Yes, any other key for No: N (我的选项)
	#2
	Please set the password for root here...
	New password: (输入密码)
	Re-enter new password: (重复输入)
	#3
	By default, a MySQL installation has an anonymous user,
	allowing anyone to log into MySQL without having to have
	a user account created for them...
	Remove anonymous users? (Press y|Y for Yes, any other key for No) : N (我的选项)
	#4
	Normally, root should only be allowed to connect from
	'localhost'. This ensures that someone cannot guess at
	the root password from the network...
	Disallow root login remotely? (Press y|Y for Yes, any other key for No) : Y (我的选项)
	#5 默认情况下，MySQL附带一个test的数据库，任何人都可以访问，可以选择是否需要删除
	By default, MySQL comes with a database named 'test' that
	anyone can access...
	Remove test database and access to it? (Press y|Y for Yes, any other key for No) : Y(我的选项)
	#6
	Reloading the privilege tables will ensure that all changes
	made so far will take effect immediately.
	Reload privilege tables now? (Press y|Y for Yes, any other key for No) : Y (我的选项)
	#7
	检查mysql服务状态
	systemctl status mysql.service
```
- 默认情况下，mysql是只允许本地访问的，如果想要其他机器也能访问需要进行配置。
```shell
	sudo mysql -uroot -p
	GRANT ALL PRIVILEGES ON *.* TO root@localhost IDENTIFIED BY "123456";
```
	其中root@localhost，localhost就是本地访问，配置成%就是所有主机都可连接，%代表所有主机，也可以是具体的ip；第二个'123456'为你给新增权限用户设置的密码。
- 新建数据库和用户
```mysql
	# 1.创建电影网项目的数据库
	CREATE DATABASE douban_server;
	# 2.创建用户ubuntu并允许用户可以从任意机器上查看douban_server数据库
	GRANT ALL PRIVILEGES ON douban_server.* TO ubuntu@"%" IDENTIFIED BY "123456";
```

