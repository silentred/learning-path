### image_filter

```
location ~* ^/simg/(\d+)_(\d+)/attachment/.*$ {
			set $width $1;
			set $height $2;
			root  /home/1188meishi_image;
			rewrite ^/simg/(\d+)_(\d+)/(.*)$ /$3 break;
			image_filter crop $width $height;
            error_page 415 = /nopic.jpg;
			expires 3d;
		}
```
