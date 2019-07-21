# River Tam
Two by two, hands of blue.


## Cycle

- 03:00 UTC Run full analyze and email result

## Run locally
```
cd src/
python -m pip install pipenv
pipenv install --ignore-pipfile
pipenv run python daemon.py --now
```

## Deploy
```
cp src/settings_template.json src/settings.json
vim src/settings.json
docker login registry.gitlab.com
docker swarm init
docker stack deploy -c docker-compose.yml river
```


## Push new image
```
docker login registry.gitlab.com
docker build -t registry.gitlab.com/dosshell/river:latest .
docker push registry.gitlab.com/dosshell/river:latest
```


## Update server
```
docker run --rm --name watchtower -v ~/.docker/config.json:/config.json -v /var/run/docker.sock:/var/run/docker.sock registry.gitlab.com/dosshell/river/watchtower --debug --run-once --label-enable --cleanup
```


## Inspect image
```
docker save --output test.tar <imageid>
```
