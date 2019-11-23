# River Tam
Two by two, hands of blue.

03:00 UTC - Run full analyze and email result


## Get started

- Create a config file
```
cp src/settings_template.json settings.json
vim settings.json
```

- Start server
```
./scripts/start_server.sh
```

## Update River to Latest
Run script (will pull git to latest)
```
./scripts/update_server.sh
```


## Run River Manually

- Run locally
```
./scripts/run_local.sh -c ../settings.json [-d --mail --fetch]
```


- Run as container
```
scripts/run_container.sh -c settings.json [-d --mail --fetch]
```


## Advanced usage

- Inspect image
```
docker save --output test.tar <imageid>
```

- Read log
```
docker logs river
```
