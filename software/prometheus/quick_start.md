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

### 数据模型
- metric name and labels 

metric name: name starting with letter; label (key / value map)

- samples (a float64 value + a millisecond-precision timestamp)

- notation 

<metric name>{<label name>=<label value>, ...}
(e.g. api_http_requests_total{method="POST", handler="/messages"} )

### Metric Type

- Counter 计数
- Gauge 上下浮动的数字，例如 内存使用率，cpu使用率
- Histogram (e.g. request durations or response sizes)
- Summary (e.g. request durations and response sizes)

### PromQL 查询API

http_requests_total{environment=~"staging|testing|development",method!="GET"}
意义为： 查询 metric name 为 http_requests_total, http_requests_total 为 staging 或者 testing ....
method 不等于 GET 的记录

=~ 不能匹配 空字符串, 例如 {method=~".*"} 就不合法
时间范围： <metric_name>{<label_name>=<label_value>}[time_range], e.g [5m] 表示 last 5 minutes







## Grafana
$ brewn install grafana
$ git clone https://github.com/percona/grafana-dashboards.git

