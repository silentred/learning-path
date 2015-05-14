FROM silentred/laravel:latest
MAINTAINER Jason W <silentred3@gmail.com>
WORKDIR /tmp
#RUN yum -y update

#RUN rpm -Uvh https://mirror.webtatic.com/yum/el7/epel-release.rpm; rpm -Uvh https://mirror.webtatic.com/yum/el7/webtatic-release.rpm

#RUN yum -y groupinstall "Development Tools"

RUN yum -y install php56w php56w-opcache php56w-cli php56w-common php56w-devel php56w-fpm php56w-gd  php56w-mbstring  php56w-mcrypt php56w-pdo php56w-mysqlnd php56w-pecl-xdebug php56w-pecl-memcache

RUN yum -y install nginx

RUN systemctl stop firewalld; systemctl disable firewalld

# PORTS
EXPOSE 80
EXPOSE 443