# River Tam
Two by two, hands of blue.


## Daemon Mode
03:00 UTC - Run full analyze and email result


## Getting Started
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
Instead of starting a server daemon, you can run it directly once.

- Run locally
Requires python 3.6. (Use run_container.sh if you do not have it installed.)

Install dependencies:
```
python3 -m pip install pipenv
python3 -m pipenv sync

Run:
```
./scripts/run_local.sh --auth-file auth.json --config-file config.json
```

- Run once as Container
Recommended if you do not have python 3.6 installed.
```
./scripts/run_container.sh --auth-file auth.json--config-file config.json
```
Containers can only use the file paths ./auth.json, ./config.json and ./cache.db.


## Advanced usage
- Inspect image
```
docker save --output test.tar <imageid>
```

- Read log
```
docker logs river
```
