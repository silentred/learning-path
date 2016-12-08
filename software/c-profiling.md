# c profiling

## install tools

```
sudo apt-get install valgrind python-pip graphviz

//如果 pip 有问题，删除 python-pip ， sudo easy_install pip

sudo pip install gprof2dot
`
sudo apt-get install libtcmalloc-minimal4
```

## compile with debug info

`g++ -g -o main main.cpp -ltcmalloc`


## profile

```
valgrind --tool=callgrind ./main

gprof2dot -f callgrind -n 0 callgrind.out.* | dot -Tsvg -o profile.svg

```