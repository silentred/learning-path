
## elasticsearch
http://www.elastic.co/downloads
download and extract; install deb package; install dir is /usr/share/elasticsearch
NOTE: pay attension to config dir.

## Kibana
wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb http://packages.elastic.co/kibana/4.5/debian stable main" | sudo tee -a /etc/apt/sources.list
sudo apt-get update && sudo apt-get install kibana
// install at /opt/kibana

## logstash
echo "deb https://packages.elastic.co/logstash/2.3/debian stable main" | sudo tee -a /etc/apt/sources.list
sudo apt-get update && sudo apt-get install logstash
// install at /opt/logstash

## filebeat
curl -L -O https://download.elastic.co/beats/filebeat/filebeat_1.2.3_amd64.deb
sudo dpkg -i filebeat_1.2.3_amd64.deb



