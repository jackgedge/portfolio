# Portfolio

Portfolio is a Flask app designed to take a WebDav folder and present it as a photographic portfolio.   

## Requiresments 
Python 3.12+  
Anaconda3/Miniconda3  

## Usage  

Export environment.yml  
`conda env export --no-builds | grep -v "^prefix: " > environment.yml`  

Create conda env
`conda env create -f environment.yml`

Run app
`python flask --app app:portfolio run --debug`  

Run as with test local webdav server  
`python ../app/scripts/webdav_test.py`  
`WEBDAV_TEST=true flask --app app:portfolio run --debug`  

## Environment variables (.env)
```
WEBDAV_HOSTNAME=""  
WEBDAV_LOGIN=""  
WEBDAV_PASSWORD=""  
PORTFOLIO_DIR=""  

WEBDAV_TEST_HOSTNAME="http://127.0.0.1:8080"
WEBDAV_TEST_LOGIN="test"
WEBDAV_TEST_PASSWORD="password"
PORTFOLIO_TEST_DIR="/"
```

## Assumed WebDav root folder structure  
root  
|  
|---folder  
        |  
        |---image1.jpeg  
        |---image2.jpeg...  

## In Progress
### Deploy Script  
`python deploy.py`   
or (dry run)  
`python deploy.py --dry-run`   

### Run as systemd service  
`sudo systemctl link "$(pwd)/portfolio.service"`   
`sudo systemctl daemon-reload`  
`sudo systemctl enable portfolio`  
`sudo systemctl start portfolio`  

## TODO:
[] Deploy script  
[] Update environment.yml  
[] Dark mode  
[] Nav bar  
[] Photo sorting  

.
├── app
│   ├── __init__.py
│   ├── resources
│   │   ├── __init__.py
│   │   └── webdav.py
│   ├── routes.py
│   ├── scripts
│   │   ├── create_thumbnails.py
│   │   ├── delete_thumbnails.py
│   │   ├── __init__.py
│   │   ├── webdav_test.py
│   │   └── webdav-test.yaml
│   ├── static
│   │   ├── css
│   │   │   └── styles.css
│   │   ├── fry_broken.jpg
│   │   └── index.js
│   ├── templates
│   │   ├── base.html
│   │   ├── broken.html
│   │   ├── folder.html
│   │   ├── image.html
│   │   └── index.html
│   └── webdav-test
│       └── publish
│           ├── folder
│               └── images.jpg
├── deploy.py
├── environment.yml
├── portfolio.service
└── README.md

