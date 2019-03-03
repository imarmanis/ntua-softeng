#!/bin/bash

# Create virtual environment
python3 -m venv venv
# Activate virtual environment
source venv/bin/activate
# Upgrade pip
pip install --upgrade pip
# Install dependencies
pip install -r requirements.txt
# Set up HTTPS certificates
openssl req -x509 -newkey rsa:4096 -nodes -out secret/cert.pem -keyout \
	secret/key.pem -days 365 \
	-subj '/C=GR/ST=Attica/L=Athens/O=Ntua'
# Reminder for the database
echo '
********************************************************************************

PostgreSQL should be running on port 5432 (the default)

********************************************************************************'
# Run the server (NOT in the background, so we can kill it with a simple CTR-C)
flask run
