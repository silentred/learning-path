#rtmp

## ffmpeg

```
ffmpeg -re -i 1.mp4 -f flv "rtmp://a.rtmp.youtube.com/live2/7m1g-rb39-krfc-1h1r"

// list webcam dev
ffmpeg -f avfoundation -list_devices true -i ""

// 
ffmpeg -f avfoundation -framerate 30 -i "0" -f flv "rtmp://a.rtmp.youtube.com/live2/7m1g-rb39-krfc-1h1r"

rtmp://ps3.live.panda.tv/live_panda/fa00285944e719d749a960fbab59262f?sign=bbbe58e6dd47ff285c9bab666469c233&time=1485962211&wm=2&wml=1&vr=0
```
