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
./scripts/run_server.sh
```
This will exit and remove any old river servers, it will build and run current checkout. Pull before execution to get latest and greatest River.

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
