up_poc:
	docker build -t sidecar_poc:1 poc && \
	echo "\n" >> poc/script.sh && \
	docker build -t sidecar_poc:2 poc && \
	docker run -d sidecar_poc:1
