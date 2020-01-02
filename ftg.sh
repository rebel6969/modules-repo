pkg install apt -y
apt install root-repo gnupg unstable-repo x11-repo wget tsu git python python-tkinter ncurses-utils -y
apt install xorg-xauth -y
tsudo pip install --upgrade pip
tsudo termux-setup-storage
apt update -y;apt upgrade -y
apt --fix-broken install
tsudo git clone https://github.com/friendly-telegram/friendly-telegram
apt install clang -y
tsudo pip install pillow==2.9.0
cd f*am;tsudo pip install -r https://raw.githubusercontent.com/rebel6969/modules-repo/master/ftg-basic-req.txt
tsudo python -m f*am --setup
