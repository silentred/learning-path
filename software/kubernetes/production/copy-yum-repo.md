# copy yum repo

wget -r -np -nH https://packages.cloud.google.com/yum/doc

wget -r -np -nH https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64/repodata

php list.php | xargs -i wget '{}'


```
<?php

$hrefs = [];
$xml = simplexml_load_file('primary.xml');

foreach ($xml->package as $value) {
	$attr = $value->location->attributes();
	$hrefs[] = $attr['href'];
}


foreach ($hrefs as $value) {
	echo 'https://packages.cloud.google.com/yum/' . substr($value, 6) . "\n";
}
```

# copy debs

wget -O - https://packages.cloud.google.com/apt/dists/kubernetes-xenial/main/binary-amd64/Packages | grep Filename | grep -E '1.6.1|docker|kubernetes-cni_0.5.1' | awk '{print $2}' | xargs -i wget https://packages.cloud.google.com/apt/'{}'