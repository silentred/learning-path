# Quick Start

## prometheus
brew install prometheus
go get github.com/prometheus/mysqld_exporter
go get github.com/prometheus/node_exporter

under this dir:
$ prometheus // default config file is prometheus.yml
$ node_exproter // another terminal
$ mysqld_exporter -config.my-cnf=".my.cnf" // third terminal

visit localhost:9090/targets, all is running


## Grafana
$ brewn install grafana
$ git clone https://github.com/percona/grafana-dashboards.git

