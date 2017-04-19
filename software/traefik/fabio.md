# Fabio 

## Usage

```
git get github.com/eBay/fabio

make build

# edit fabio.properties

registry.backend = file
registry.file.path = rule.ini

# edit rule.ini

route add service-a www.mp.dev/accounts/ http://host-a:11050/ tags "a,b"
route add service-a www.kjca.dev/accounts/ http://host-a:11050/ tags "a,b"

# start 

./fabio -cfg=fabio.properties

# visit admin panel at localhost:9998 
```