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
```mysql
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
# 3.查看mysql的user表里用户ubuntu是否存在
show user;
```

- 上传写好的前后端项目到云服务器
```shell
# 1.打包前后端项目
后端打包：tar -zcf douban_server.tar.gz douban_server
前端打包：tar -zcf douban_client.tar.gz douban_client
# 2.用sftp上传云服务器
mac系统自带 终端->建立远程连接->sftp 功能
- 新建连接：填入云主机ip
- 用户：填入云主机用户名 我的是ubuntu
- 点击“连接”
- 输入云服务器登录密码
- 上传tar包
	put 路径+douban_server.tar.gz
	put 路径+douban_client.tar.gz

	这里用不到下载命令，不过了解一下：
	get 云服务器文件路径 本地下载路径
	参考：https://www.jianshu.com/p/f034817a7837
# 3.在云服务器上解压tar包
	cd tar包所在路径
	tar -xf douban_server.tar.gz -C mywebsite
	tar -xf douban_client.tar.gz -C mywebsite
	这里统一将前后端项目解压到mywebsite文件夹下，方便以后备份管理。
```
- django后端的迁移操作
```shell
cd mywebsite/douban_server
python3 manage.py makemigrations
python3 manage.py migrate
```
- 在mysql中插入数据
这里我将事先爬虫爬取到的电影信息准备好放在txt中，复制内容后到数据库中粘贴
```mysql
use douban_server;
show tables;# 查看迁移成功的表名
# 粘贴txt中的内容，在film表中插入若干条数据
```

- 配置uwsgi文件
用 uwsgi 替代python3 manage.py runserver 方法启动服务器，可以在后台运行。
使用 python manage.py runserver 通常只在开发和测试环境中使用，当开发结束后，完善的项目代码需要在一个高效稳定的环境中运行。
这时可以使用uWSGI，uWSGI是WSGI的一种，它可以让Django、Flask等开发的web站点运行其中。

1.前端uwsgi配置
```shell
cd mywebsite/douban_client
vi uwsgi.ini
```
在新建文件中输入：
```python
[uwsgi]
socket=127.0.0.1:5000
chdir=/home/ubuntu/mywebsite/douban_client
module=douban_client.wsgi:application
master=true
daemonize=/home/ubuntu/mywebsite/douban_client/run.log
```
uwsgi运行起来后，会在该目录下生成run.log日志文件。

2.后端uwsgi配置
```shell
cd mywebsite/douban_server
vi uwsgi.ini
```
在新建文件中输入：
```python
[uwsgi]
# IP地址:端口号
http = 0.0.0.0:8000
#socket=127.0.0.1:8000
# 项目当前工作目录
chdir = /home/ubuntu/mywebsite/douban_server
# 项目中wsgi.py文件的目录，相对于当前工作目录
wsgi-file = douban_server/wsgi.py
# 进程个数
process=4
# 每个进程的线程个数
threads=2
# 服务的pid记录文件
pidfile = uwsgi.pid
# 服务的目志文件位置
daemonize=uwsgi.log
```
uwsgi运行起来后，会在该目录下生成uwsgi.log日志文件和uwsgi.pid服务进程文件。

3.uwsgi的启动和停止命令
来到前后端相应目录下，启动uwsgi
```shell
sudo uwsgi --ini uwsgi.ini
ps -ef | grep uwsgi # 查看是否启动成功
```
停止后端uwsgi
```shell
sudo uwsgi --stop uwsgi.pid
```
由于前端没有pid文件，用杀进程的方式停止
```shell
ps -ef | grep uwsgi # 查看pid
kill -9 [pid]
```

- 配置nginx
到这里，服务器布置已经差不多，但我们的网站总有一个端口号让我们感觉有点low low的。那就让再来布置一个新的东西：nginx。
Nginx是轻量级的高性能的HTTP和反向代理web服务器，提供了诸如HTTP代理和反向代理、负载均衡、缓存等一系列重要特性，使用广泛。因为它是C语言编写，所以执行效率高。

```txt
1.首先nginx是都对外的服务接口，外部浏览器通过url访问nginx。
2.nginx接收到浏览器发送过来的http请求，将包进行解析，分析url，如果是静态文件请求就直接访问用户给nginx配置的静态文件目录，直接返回用户请求的静态文件。
如果不是静态文件，而是一个动态的请求，那么nginx就将请求发个uwsgi，uwsgi接收到请求后将包进行处理，处理成wsgi可以接受的格式，并发给wsgi，wsgi根据请求调用应用程序的某个文件，某个文件的某个函数，最后处理完将返回值再次交给wsgi，wsgi将返回值打包，打包成uwsgi能够接收的格式，uwsgi接收wsgi发送的请求，并转发给nginx，nginx最终将返回值返回给浏览器。

3.要知道第一级的nginx并不是必须的，uwsgi完全可以完成整个的和浏览器交互的流程，但是要考虑到某种情况。

4.安全问题，程序不能直接被浏览器访问到，而是通过nginx，nginx只开放某个接口，uwsgi本身是内网接口，这样运维人员在nginx上加上安全性的限制，可以达到保护程序的作用。
5.负载均衡问题，一个uwsgi很可能不够用，即使开了多个work也是不行，毕竟一台机器的cpu和内存都是有限的，有了nginx做代理，一个nginx可以代理多台uwsgi完成uwsgi的负载均衡。
6.静态文件问题，用django或是uwsgi这种东西来负责静态文件的处理是很浪费的行为，而且他们本身对文件的处理也不如nginx好，所以整个静态文件的处理都直接有nginx完成，静态文件的访问完全不去经过uwsgi以及后面的东西。
```
大致总结了一下运行流程：
浏览器请求nginx（非静态文件） -> nginx请求uwsgi -> wsgi -> 运行django下的代码 -> wsgi -> uwsgi -> nginx -> 浏览器
浏览器请求nginx（静态文件）-> 静态文件目录 -> 返回静态文件到浏览器

1.修改nginx 的配置文件 /etc/nginx/sites-available/default，修改前最好备份一下
```python
server {...
        server_name xxx.xxx.xxx.xxx;#公网IP或者域名
        location / {
            # First attempt to serve request as file, then
            # as directory, then fall back to displaying a 404.
            # try_files $uri $uri/ =404;
            include uwsgi_params; # 将所有的参数转到uwsgi下
            uwsgi_pass 127.0.0.1:5000; # 重定向到127.0.0.1的8000端口
        }
        location /static {
            alias /home/ubuntu/mywebsite/douban_client/static; # static文件夹所在的绝对路径
        }
...}
```
注意：
	一定要注释掉try_files $uri $uri/ =404;这句话。
	在location /和location /static的后面是有空格的。

2.nginx的相关命令
```shell
# 启动
# 方式一：
$ sudo /etc/init.d/nginx start
# 方式二：
$ sudo service nginx start

# 重启
# 方式一：
$ sudo /etc/init.d/nginx restart
# 方式二：
$ sudo service nginx restart

# 查看进程
# 方式一：
$ ps aux | grep nginx
# 方式二：
$ sudo /etc/init.d/nginx status
# 方式三：
$ sudo service nginx status

# 停止
# 方式一：
$ sudo /etc/init.d/nginx stop
# 方式二：
$ sudo service nginx stop
```

- 检查后端django中的settings.py
```python
DEBUG = False
ALLOWED_HOSTS = ['*']
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'douban_server',
        'USER': 'ubuntu',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}
```

- 重启uwsgi和nginx，完成！