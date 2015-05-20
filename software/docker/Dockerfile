FROM centos:latest
MAINTAINER Jason W <silentred3@gmail.com>
WORKDIR /tmp
RUN yum -y update

RUN rpm -Uvh https://mirror.webtatic.com/yum/el7/epel-release.rpm; rpm -Uvh https://mirror.webtatic.com/yum/el7/webtatic-release.rpm

#RUN yum -y groupinstall "Development Tools"
RUN systemctl stop firewalld; systemctl disable firewalld

RUN yum -y install php56w php56w-opcache php56w-cli php56w-common php56w-devel php56w-fpm php56w-gd  php56w-mbstring  php56w-mcrypt php56w-pdo php56w-mysqlnd php56w-pecl-xdebug php56w-pecl-memcache

RUN yum -y install nginx

RUN yum -y install openssh-server supervisor

RUN mkdir -p /etc/nginx/vhost
#加入网站配置
ADD laravel.conf /etc/nginx/vhost/laravel.conf
ADD supervisord.ini /etc/supervisord.d/nginx-php.ini

#ADD start.php /var/www/start.php
#RUN chmod u=rwx /var/www/start.php

#配置nginx, non-daemon
RUN sed -i '/conf.d\/\*.conf;/a include /etc/nginx/vhost/*.conf;' /etc/nginx/nginx.conf && \
	sed -i '/worker_processes/a daemon  off;' /etc/nginx/nginx.conf

#设置fpm，non-daemon 
RUN sed -i "s/;date.timezone =.*/date.timezone = UTC/" /etc/php.ini && \
    sed -i "s/display_errors = Off/display_errors = stderr/" /etc/php.ini && \
    sed -i "s/upload_max_filesize = 2M/upload_max_filesize = 30M/" /etc/php.ini && \
    sed -i -e "s/;daemonize\s*=\s*yes/daemonize = no/g" /etc/php-fpm.conf && \
    sed -i '/^listen = /clisten = 9000' /etc/php-fpm.d/www.conf && \
    sed -i '/^listen.allowed_clients/c;listen.allowed_clients =' /etc/php-fpm.d/www.conf
	
#sed -i "s/;cgi.fix_pathinfo=1/cgi.fix_pathinfo=0/" /etc/php.ini
#sed -i '/^user = /c user=root' /etc/php-fpm.d/www.conf && \
#sed -i '/^group = /c user=root' /etc/php-fpm.d/www.conf   
#sed -i '/^;catch_workers_output/ccatch_workers_output = yes' /etc/php-fpm.d/www.conf

#supervoder非daemon
RUN sed -i "s/nodaemon=false/nodaemon=true/" /etc/supervisord.conf

#RUN php /var/www/start.php

RUN mkdir -p /home/www/ && \
	chmod -R 755 /home/www/
VOLUME ["/home/www/"]
# PORTS
EXPOSE 22 80 443 9000

#ENTRYPOINT ["php /var/www/start.php"]
CMD ["/usr/bin/supervisord"]






