# Portfolio

Portfolio is a Flask app designed to take a WebDav folder and present it as a photographic portfolio. 

## Requiresments 
Python 3.12+
Anaconda3/Miniconda3

## Usage

`python deploy.py`
or (dry run)
`python deploy.py --dry-run`


### Run as systemd service
`sudo systemctl link "$(pwd)/portfolio.service"`
`sudo systemctl daemon-reload`
`sudo systemctl enable portfolio`
`sudo systemctl start portfolio`

## TODO:
- Deploy script
- Update environment.yml
- Dark mode
- Nav bar
- Photo sorting

## Commands

Export environment.yml
`conda env export --no-builds | grep -v "^prefix: " > environment.yml`
