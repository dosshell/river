# River Tam
Two by two, hands of blue.


## Cycle

- 02:00 Update to latest image
- 03:00 Run full analyze and email result


## Deploy
```
cp settings_template.json settings.json
vim settings.json
docker login registry.gitlab.com
docker swarm init
docker stack deploy -c docker-compose.yml river
```


## Update image
```
docker login registry.gitlab.com
docker build -t registry.gitlab.com/dosshell/river:latest .
docker push registry.gitlab.com/dosshell/river:latest
```
