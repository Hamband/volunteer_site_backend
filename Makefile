build:
	docker build -t hamband_volunteer_api .

deploy:
	docker stack deploy -c docker-compose.yml hamband_volunteer_api

rm:
	docker stack rm hamband_volunteer_api