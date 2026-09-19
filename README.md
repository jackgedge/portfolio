# Portfolio

Portfolio is a Flask app designed to take a WebDav folder and present it as a photographic portfolio.   

## Requiresments 
Python 3.12+  
Anaconda3/Miniconda3  

### Run as systemd service  
`sudo systemctl link "$(pwd)/portfolio.service"`   
`sudo systemctl daemon-reload`  
`sudo systemctl enable portfolio`  
`sudo systemctl start portfolio`  

## Commands  

Export environment.yml  
`conda env export --no-builds | grep -v "^prefix: " > environment.yml`  

Create conda env
`conda env create -f environment.yml`

Run app
`python flask --app app:portfolio run --debug`  

Run as with test local webdav server  
`python /home/jack/Code/portfolio/app/scripts/webdav_test.py`  
`WEBDAV_TEST=true flask --app app:portfolio run --debug`  

## In Progress
`python deploy.py`  
or (dry run)  
`python deploy.py --dry-run`  

## TODO:
[] Deploy script  
[] Update environment.yml  
[] Dark mode  
[] Nav bar  
[] Photo sorting  
