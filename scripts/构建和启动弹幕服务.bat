@echo off
cd D:\LLM\ordinaryroad-barrage-fly\.docker
# DOCKER_OPTS="--registry-mirror=https://mirror.ccs.tencentyun.com"
# 拉取最新版1.2.0
docker pull ordinaryroad-docker.pkg.coding.net/ordinaryroad-barrage-fly/docker-pub/ordinaryroad-barrage-fly:1.2.0
docker pull ordinaryroad-docker.pkg.coding.net/ordinaryroad-barrage-fly/docker-pub/ordinaryroad-barrage-fly-ui:1.2.0
docker tag ordinaryroad-docker.pkg.coding.net/ordinaryroad-barrage-fly/docker-pub/ordinaryroad-barrage-fly:1.2.0 ordinaryroad-barrage-fly
docker tag ordinaryroad-docker.pkg.coding.net/ordinaryroad-barrage-fly/docker-pub/ordinaryroad-barrage-fly-ui:1.2.0 ordinaryroad-barrage-fly-ui

docker compose -f .\compose-with-mysql.yaml up -d
exit