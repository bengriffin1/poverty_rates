SHELL=/bin/sh
development_cluster=kind-kind
flyway_tag=poverty-rates-backend-flyway:0.0.1
namespace=poverty-rates

build-backend: ## Builds docker image and pushes to kind for development
	docker build --build-arg SQL_FOLDER=backend/migrations . -t $(flyway_tag) -f kubernetes/postgraphile_backend/Dockerfile
	kind load --loglevel trace docker-image $(flyway_tag)

upgrade-backend: ## Deploys to development kubernetes cluster
	- kubectl create namespace $(namespace)
	helm upgrade --install $(namespace) --values kubernetes/postgraphile_backend/values.yaml --values backend/values-development.yaml kubernetes/postgraphile_backend --namespace $(namespace) --set namespace=$(namespace) --set app=$(namespace)

delete-development: ## Deletes development Helm release
	helm delete $(namespace) --namespace $(namespace)

forward: ## Forwards traffic from postgres to local
	kubectl port-forward service/poverty-rates-postgresql -n poverty-rates 5432:5432