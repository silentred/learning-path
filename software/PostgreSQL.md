PostgreSQL

## install

yum install postgresql-server postgresql postgresql94-contrib postgresql94-devel

## init

sudo service postgres initdb

## create db

sudo -u postgres psql
CREATE DATABASE testdb;
\l

## select db
\c testdb;

## create password
\password

## quit
\q

## permission config file
sudo su 
vim /var/lib/pgsql/data/pg_hba.conf
注意9.4版本的位置在 /var/lib/pgsql/9.4/data/pg_hba.conf

local all all trust
host all 127.0.0.1/32 trust
Ident都改为 trust

退出root
psql -d testdb -U postgres
-W password, 会被忽略

## 开放端口和权限
在 /var/lib/pgsql/9.4/data/pg_hba.conf 中加入：
host    all             all             10.0.0.2/16             trust

表示ip段可以访问

在 /var/lib/pgsql/9.4/data/postgresql.conf 中 找到 listen_address, 改为 '*', 监听所有host


