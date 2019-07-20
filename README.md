# River Tam
Two by two, hands of blue.


## Cycle

- 02:00 Update to latest image
- 03:00 Run full analyze and email result

## Test
```
python -m pip install pipenv
pipenv install --ignore-pipfile
pipenv run python daemon.py --now
```

## Deploy
```
cp settings_template.json settings.json
vim settings.json
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
