# set static ip

sudo vim /etc/dhcpcd.conf 

interface wlan0
static ip_address=192.168.1.166

static routers=192.168.1.1
static domain_name_servers=75.75.75.75 75.75.76.76 2001:558:feed::1 2001:558:feed::2 8.8.8.8 192.168.1.1

# play mp3
omxplayer test.mp3

# install golang

wget -c https://storage.googleapis.com/golang/go1.6.3.linux-armv6l.tar.gz
tar -xzf go1.6.2.linux-armv6l.tar.gz -C ~/Download/projects
export GOROOT=~/Download/projects/go
export PATH="$PATH:$GOROOT/bin"

# install pathogen.vim

mkdir -p ~/.vim/autoload ~/.vim/bundle && \
curl -LSso ~/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim


# shell short cuts
ctrl + k # delete from cursor to the end of line
ctrl + u # delete from start to the cursor

Ctrl + A # Home move cursor to the beginning of the input
Ctrl + E # End  move cursor to the end of input
Ctrl + H # Backspace    delete a character before the cursor
Ctrl + D # Delete   delete a character after the cursor