# Cryptonite
## Description
Collection of open source cipher and digital signature modules with simple web UI.
Based on Flask & Vue.js

## Install and run with [docker-compose https://docs.docker.com/compose/]

```bash
docker-compose up -d
```
And visit http://localhost:80

Default admin login and password you can find in app/config/config.yml file in app.default.admin section.

## Install from scratch
Firstly, install [autoenv https://github.com/kennethreitz/autoenv].

Then install backend requrements:
```bash
cd app
virtualenv -v venv
cd api && cd .. #for activating environment
pip install -r requirements.txt
```

And also frontend requirements:
```bask
cd web
npm install
```

Run the application:
```bash
#build JS and CSS with webpack
cd web
npm run build

cd ../app
#migrate or create your DB
flash createdb #initialize DB for first run
flask db migrate
flask db upgrade

#run web-server
uwsgi --yaml config/config.yml
#or
gunicorn -b localhost:5000 app:app
#or
python app.py
```

You can also simply run entrypoint.sh instead of manual backend prepare and run.

Finally visit ```http://localhost:5000```.
