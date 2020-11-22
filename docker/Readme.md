# Docker tutorial

## Required steps
First of all init all `.env` files via
```bash
make init
```

## Build and run app locally
Next step is to build project images with following command
```bash
make build
```

To run project:
```bash
make up
```

Note that on the production environment API is served via nginx:
```bash
docker-compose -f live.yml -d up
```

stop docker containers:
```bash
docker stop $(docker ps -a -q)
```
