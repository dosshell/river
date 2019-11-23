# River Tam
Two by two, hands of blue.


## Cycle
- 03:00 UTC Run full analyze and email result


## Create a config file
```
cp src/settings_template.json settings.json
vim settings.json
```


## Run River
After you created a config file you can run River locally or in a container. Please note that it exists a `scripts` folder to get you started.


### Run locally
```
./scripts/run_local.sh -c ../settings.json
```


### Run as container
```
scripts/run_container.sh
```


### Start River as a docker daemon
```
./scripts/update_container.sh
```


### Update River
To update the container of an already running docker daemon container:
```
./scripts/update_server.sh
```


## Advanced usage
This section will describe detailed commands of different actions.

### Run daemon from registry
```
docker login registry.gitlab.com
docker pull registry.gitlab.com/dosshell/river:latest
docker run --name river -v $PWD/settings.json:/app/settings.json --restart=unless-stopped -d registry.gitlab.com/dosshell/river:latest --mail
```


### Push new image
```
docker login registry.gitlab.com
docker build -t registry.gitlab.com/dosshell/river:latest .
docker push registry.gitlab.com/dosshell/river:latest
```


### Update server manually
```
docker stop river
docker rm river
docker pull registry.gitlab.com/dosshell/river:latest
```
And then use the run daemon container code.


### Inspect image
```
docker save --output test.tar <imageid>
```

