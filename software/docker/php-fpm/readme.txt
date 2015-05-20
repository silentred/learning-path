±£´æ¾µÏñ£º
docker save -o /tmp/jason-php-fpm-v1.tar.gz jason/php-fpm:v1

ÔØÈë¾µÏñ
docker load -i /tmp/jason-php-fpm-v1.tar.gz

Æô¶¯£º
sudo docker run --name="fpm2" -p 9003:9000 -d -v /home/jason/shared/projects/:/home/jason/shared/projects/ jason/php-fpm:v1

