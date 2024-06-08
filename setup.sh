# setup.sh

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the Python dependencies
pip install --no-cache-dir -r requirements.txt

# Run the Python program
python load_data.py