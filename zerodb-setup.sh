#!/bin/bash
# Author=Elias Hazboun
# A script to create zerodb on ilab computers
# it builds python3.5 as default
# it installs pip3
# it builds zerodb and zerodb-server

#add default route
ip r add default via 192.168.38.254

#check if repo has been added before:
check=$(tail -1 /etc/apt/sources.list)
if [ "$check" != "deb-src http://ppa.launchpad.net/fkrull/deadsnakes/ubuntu trusty main" ]
then
   #add pubkey of repo to trusted keys.
   sudo -u ilab wget "http://keyserver.ubuntu.com:11371/pks/lookup?op=get&search=0x5BB92C09DB82666C"
   apt-key add "lookup?op=get&search=0x5BB92C09DB82666C"
   rm -f "lookup?op=get&search=0x5BB92C09DB82666C"
   #add repo to sources.list
   echo deb http://ppa.launchpad.net/fkrull/deadsnakes/ubuntu trusty main >> /etc/apt/sources.list
   echo deb-src http://ppa.launchpad.net/fkrull/deadsnakes/ubuntu trusty main >> /etc/apt/sources.list
   apt-get update
fi

#setup python3.5
apt-get --yes --force-yes install python3.5 python3.5-dev libncurses5-dev
mv /usr/bin/python3 /usr/bin/python3-old
ln -s /usr/bin/python3.5 /usr/bin/python3

#install pip3
sudo -u ilab wget "https://bootstrap.pypa.io/get-pip.py"
python3 get-pip.py
rm -f get-pip.py

pip3 install setuptools --upgrade
pip3 install ipython

#setup ZeroDB
apt-get --yes --force-yes install python3-pip build-essential python3-dev libffi-dev libssl-dev
pip3 install zerodb-server==0.2.0b2
pip3 install zerodb==0.99.0b1

#setup ZeroDB server
cd /home/ilab
sudo -u ilab mkdir zerodb
cd zerodb
sudo -u ilab git clone "https://github.com/zerodb/zerodb-server.git"
cd zerodb-server/demo
pip3 install -r requirements.txt

#install TCL
cd /home/ilab/Downloads
sudo -u ilab wget http://downloads.sourceforge.net/tcl/tcl8.6.6-src.tar.gz


cd tcl8.6.6 

sudo -u ilab export SRCDIR=`pwd` &&

cd unix &&

sudo -u ilab ./configure --prefix=/usr           \
            --mandir=/usr/share/man \
            $([ $(uname -m) = x86_64 ] && echo --enable-64bit) &&
sudo -u ilab make &&

sudo -u ilab sed -e "s#$SRCDIR/unix#/usr/lib#" \
    -e "s#$SRCDIR#/usr/include#"  \
    -i tclConfig.sh               &&

sudo -u ilab sed -e "s#$SRCDIR/unix/pkgs/tdbc1.0.4#/usr/lib/tdbc1.0.4#" \
    -e "s#$SRCDIR/pkgs/tdbc1.0.4/generic#/usr/include#"    \
    -e "s#$SRCDIR/pkgs/tdbc1.0.4/library#/usr/lib/tcl8.6#" \
    -e "s#$SRCDIR/pkgs/tdbc1.0.4#/usr/include#"            \
    -i pkgs/tdbc1.0.4/tdbcConfig.sh                        &&

sudo -u ilab sed -e "s#$SRCDIR/unix/pkgs/itcl4.0.5#/usr/lib/itcl4.0.5#" \
    -e "s#$SRCDIR/pkgs/itcl4.0.5/generic#/usr/include#"    \
    -e "s#$SRCDIR/pkgs/itcl4.0.5#/usr/include#"            \
    -i pkgs/itcl4.0.5/itclConfig.sh                        &&

sudo -u ilab unset SRCDIR

make install &&
make install-private-headers &&
ln -v -sf tclsh8.6 /usr/bin/tclsh &&
chmod -v 755 /usr/lib/libtcl8.6.so

#install Expect
cd /home/ilab/Downloads
sudo -u ilab wget http://prdownloads.sourceforge.net/expect/expect5.45.tar.gz
sudo -u ilab tar -xvf expect5.45.tar.gz
cd expect5.45

sudo -u ilab ./configure --prefix=/usr --with-tcl=/usr/lib --enable-shared --mandir=/usr/share/man --with-tclinclude=/usr/include
sudo -u ilab make

make install &&
ln -svf expect5.45/libexpect5.45.so /usr/lib


#install tshark
apt-get install tshark

#install iproute
apt-get install iproute

