python3 -m venv cloudsecenv
. cloudsecenv/bin/activate
apt-get install python3-setuptools
pip3 install -e .
curl https://rclone.org/install.sh | sudo bash
deactivate
