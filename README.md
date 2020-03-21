# River Tam
Two by two, hands of blue.

## Daemon Mode
03:00 UTC - Run full analyze and email result


## Get Started

- Create a config-file and an auth-file
```
cp auth.template.json auth.json
cp config.template.json config.json
vim auth.json
vim config.json
```

- Start Server
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
./scripts/run_local.sh --auth-file ../auth.json
```


- Run as Container
```
scripts/run_container.sh --config-file ../config.json --daemon-off
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
