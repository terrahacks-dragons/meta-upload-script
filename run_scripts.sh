#!/bin/bash

# Activate the virtual environment
source /Users/ammarmahmood/Desktop/python-automation-script/venv/bin/activate

# Run script1.py
python3 whatsapp_photo_downloader.py
if [ $? -ne 0 ]; then
    echo "Error: whatsapp_photo_downloader.py failed."
    exit 1
fi

# Run script2.py
python3 upload_to_server.py
if [ $? -ne 0 ]; then
    echo "Error: upload_to_server.py failed."
    exit 1
fi

# Deactivate the virtual environment
deactivate

