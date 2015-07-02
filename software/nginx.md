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

#### 关于image_filter_buffer

默认为 1M
可出现的位置: http, server, location

原图最大2M，要裁剪的图片超过2M返回415错误，需要调节参数image_filter_buffer 
image_filter_buffer 2M;        
