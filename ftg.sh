pkg install apt -y
apt install root-repo gnupg unstable-repo x11-repo wget tsu git python python-tkinter ncurses-utils -y
apt install xorg-xauth -y
tsudo pip install --upgrade pip
tsudo termux-setup-storage
apt update -y;apt upgrade -y
apt --fix-broken install
apt install clang -y
tsudo pip install future-fstrings
tsudo pip install git+https://gitlab.com/mattia.basaglia/tgs@master
tsudo pip install gitpython
tsudo pip install gtts
tsudo pip install hachoir
tsudo pip install pyfiglet
tsudo pip install pythondialog
tsudo pip install pyyandextranslateapi
tsudo pip install babel
tsudo pip install telethon
tsudo git clone https://github.com/friendly-telegram/friendly-telegram
cd f*am;tsudo python -m f*am --setup
