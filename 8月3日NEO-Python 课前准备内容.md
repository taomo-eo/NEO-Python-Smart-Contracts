## 0-准备

> 教程基于macOS或[Linux Ubuntu](https://www.ubuntu.com/download/desktop)，windows用户需要使用[linux虚拟机](https://www.virtualbox.org/wiki/Downloads)。

- **Linux Ubuntu**

1.首先确认基本的apt和curl都已安装/更新，执行

```
sudo apt-get update
sudo apt-get install curl
```

2.安装docker，以备运行私链容器(neo-privatenet)，执行

```
sudo apt install docker.io
```

3.安装docker compose，执行

```
sudo curl -L https://github.com/docker/compose/releases/download/1.22.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
```
*([因版本可能更新，具体命令以docker的Github页面为准](https://github.com/docker/compose/releases))*

*此命令可能需要翻墙，如果下载时间过长，见3.0.1,否则见3.1*

3.0.1. 手动从[Github](https://github.com/docker/compose/releases)下载此项目，并将文件重命名为`docker-compose`，放在/usr/local/bin/

```
sudo cp *docker-compose的下载路径*/docker-compose usr/local/bin
```

3.1. 设定权限

```
sudo chmod +x /usr/local/bin/docker-compose
```



- **Mac OS**

下载[Docker for Mac](https://store.docker.com/editions/community/docker-ce-desktop-mac)，Docker以及Docker Compose均整合在安装文件里。




## 1-环境搭建

#### NEO-Local

进入想要把neo-local加载到的文件夹，比如：

```
cd Documents/neo/
```

下载Github上的NEO-Local, COZ制作的整合包，整合了NEO-Python钱包的所有依赖包，可以一键搭建neo-python和私链。执行：

```
git clone https://github.com/CityOfZion/neo-local.git
```

进入neo-local所在的路径

```
cd ./neo-local
```



启动docker

```
sudo service docker start
```



运行neo-local: 

```
sudo docker-compose up -d --build --remove-orphans
```

​	*注：第一次运行时需要下载4.4G的内容，可能需要翻墙*

运行neo-python钱包：

```
sudo docker exec -it neo-python np-prompt -p -v
```

出现如下界面进入了**NEO CLI 命令行**，那么恭喜你已经成功搭建好所有环境。

![neo-python-running](https://raw.githubusercontent.com/taomo-eo/NEO-Python-Smart-Contracts/master/neo-python-running.png)


退出钱包:

```
quit
```

停止运行neo-local:

```
docker-compose down
```



*注：若想要不使用整合包的搭建环境方法，可见此教程https://blog.gallifrey.cn/?p=419*