# dans-license-service

poetry build; poetry install; docker rm -f dans-license-service; docker rmi ekoindarto/dans-license-service:0.1.0; docker build --no-cache -t ekoindarto/dans-license-service:0.1.0 -f Dockerfile . ; docker run -d -p 33163:33163 --name dans-license-service ekoindarto/dans-license-service:0.1.0; docker exec -it dans-license-service /bin/bash
