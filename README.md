# huya

1. 安装并启动docker
   yum install docker -y
   systemctl start docker
   
2. 安装docker-compose
   yum install python3 -y
   pip3 install --upgrade pip
   pip3 install docker-compose

3. 把仓库的docker/docker-compose.yaml、start.sh、stop.sh 放到/root

4. 修改执行权限 
  chmod 755 start.sh
  chmod 755 stop.sh
 
 5. 启动服务
   ./start.sh
