# Start memcached service
brew services start memcached

# Setup virtual environment for Python
python3.10 -m venv projvenv

# Activate the virtual environment for Python
source projvenv/bin/activate

# Install required packages
pip install -r requirements.txt

