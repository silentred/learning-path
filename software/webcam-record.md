# Webcam record

brew install ffmpeg

- 查看device列表

ffmpeg -f avfoundation -list_devices true -i ""

- 录制

ffmpeg -f avfoundation -r 30 -i "0" out.mpg
-r 表示 frame rate. 默认为29，不支持。支持30.



mediafilesegmenter -f ~/Downloads/stream  out.mpg