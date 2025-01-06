INSTALL:

cd ~/git/galatae_ps3
python3 -m venv venv
source venv/bin/activate
pip install inputs
pip install pyserial

LAUNCH:
cd ~/git/galatae_ps3
source venv/bin/activate
python main.py