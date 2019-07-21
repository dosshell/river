# River Tam
Two by two, hands of blue.


## Cycle
- 03:00 UTC Run full analyze and email result


## Create a config file
```
cp src/settings_template.json settings.json
vim settings.json
```


## Run locally
```
cd src/
python -m pip install pipenv
pipenv install --ignore-pipfile
pipenv run python daemon.py --now -c ../settings.json
```


## Build and run container
```
docker build -t registry.gitlab.com/dosshell/river:latest .
docker run --name river -v $PWD/settings.json:/app/settings.json --restart=unless-stopped -d registry.gitlab.com/dosshell/river:latest
```

you could also add `--rm` and `--now` to run it once:
```
docker run --rm --name river -v $PWD/settings.json:/app/settings.json --restart=unless-stopped -d registry.gitlab.com/dosshell/river:latest --now
```


## Run from registry
```
docker login registry.gitlab.com
docker pull registry.gitlab.com/dosshell/river:latest
docker run --name river -v $PWD/settings.json:/app/settings.json --restart=unless-stopped -d registry.gitlab.com/dosshell/river:latest
```


## Push new image
```
docker login registry.gitlab.com
docker build -t registry.gitlab.com/dosshell/river:latest .
docker push registry.gitlab.com/dosshell/river:latest
```


## Update server
```
docker stop river
docker rm river
docker pull registry.gitlab.com/dosshell/river:latest
```
And then use the run container code.


## Inspect image
```
docker save --output test.tar <imageid>
```
