# River Tam
Two by two, hands of blue.


## Deploy
```
cp settings_template.json settings.json
vim settings.json
docker login registry.gitlab.com
docker swarm init
docker stack deploy -c docker-compose.yml river
```
