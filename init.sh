sudo yum install python3 python3-setuptools
sudo yum groupinstall "Development Tools"

mkdir venv
virtualenv venv
source venv/bin/activate

sudo yum install -y libtiff-devel libjpeg-devel libzip-devel freetype-devel \
    lcms2-devel libwebp-devel tcl-devel tk-devel

pip install -r requirements.txt

mkdir BoulderDjangoDev/tmp/
