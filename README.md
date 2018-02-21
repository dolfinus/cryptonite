# Cryptonite
## Description
Collection of open source cipher and digital signature modules with simple web UI.
Based on Flask & Vue.js

## Install

```bash
pip3 install -r requirements
cd app/client
npm install
```

## Run

```bash
cd app/client
npm run build
cd ../..
uwsgi --yaml config.yml
```

And visit ```http://localhost:5050```.
Another way is to use ```python3 app.py``` to run application with native Flask web server Werkzeug.