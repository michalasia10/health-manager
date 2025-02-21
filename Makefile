APP_NAME := health-manager
RESET := \033[0m
RED := \033[31m
GREEN := \033[32m
YELLOW := \033[33m
BLUE := \033[34m
MAGENTA := \033[35m
CYAN := \033[36m

INFO_PREFIX := [INFO]
ERROR_PREFIX := [ERROR]
SUCCESS_PREFIX := [SUCCESS]

define echo_red
	@echo "$(RED)$(1)$(RESET)"
endef

define echo_green
	@echo "$(GREEN)$(1)$(RESET)"
endef

define echo_yellow
	@echo "$(YELLOW)$(1)$(RESET)"
endef

define echo_blue
	@echo "$(BLUE)$(1)$(RESET)"
endef

define echo_magenta
	@echo "$(MAGENTA)$(1)$(RESET)"
endef

define echo_cyan
	@echo "$(CYAN)$(1)$(RESET)"
endef


define e_info
	@echo "\\n$(BLUE)$(INFO_PREFIX) $(1)$(RESET)\\n"
endef

define e_error
	@echo "\\n$(RED)$(ERROR_PREFIX) $(1)$(RESET)\\n"
endef

define e_success
	@echo "\\n$(GREEN)$(SUCCESS_PREFIX) $(1)$(RESET)\\n"
endef

.PHONY: run-and-build
run-and-build:
	$(call e_info,"Building app AND RUNNING...")
	docker-compose up -d --build
	$(call e_success,"Done...")

.PHONY: make-migrations
make_migrations:
	$(call e_info,"Creating migrations...")
	docker-compose run --rm $(APP_NAME) python src/manage.py makemigrations
	$(call e_success,"Migrations...done..")

.PHONY: migrate
migrate:
	$(call e_info,"Migrating...")
	docker-compose run --rm $(APP_NAME) python src/manage.py migrate
	$(call e_success,"Migration done...")

.PHONY: add-app
add-app:
ifndef name
	$(call e_info,"Add `name` : make add-app name=new_name")
	@exit 1
endif
	$(call e_info,"Making $(name)...")
	@docker-compose exec -it $(APP_NAME) bash -c "cd src && python manage.py startapp $(name)"
	$(call e_success, "App $(name) added")


.PHONY: run-test
run-test:
	$(call e_info,"Running tests...")
	docker-compose run --rm $(APP_NAME) pytest --reuse-db $(ARGS)
	$(call e_success,"Tests done...")

.PHONY: build-ci-app
build-ci-app:
	$(call echo_info,"Build app...")
	docker build -t $(APP_NAME) .
	$(call echo_success,"Build app..done...")

.PHONY: run-ci-test
run-ci-test:
	$(call echo_info,"Running tests...")
	docker run --network host \
		-e POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) \
		-e POSTGRES_USER=$(POSTGRES_USER) \
		-e POSTGRES_DB=$(POSTGRES_DB) \
		-e POSTGRES_HOST=$(POSTGRES_HOST) \
		-e POSTGRES_PORT=$(POSTGRES_PORT) \
		$(APP_NAME) pytest -n 4 -vv
	$(call echo_success,"Tests done...")

.PHONY: lock-pckgs
lock-pckgs:
	$(call e_info,"Locking dependencies...")
	uv pip compile pyproject.toml -o requirements.txt
	$(call e_success,"Dependencies locked!")


.PHONY: format
format:
	$(call e_info,"Formatting code...")
	ruff format src
	$(call e_success,"Code formatted!")

.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  make-migrations: Create migrations"
	@echo "  migrate: Apply migrations"
	@echo "  run-test: Run tests"
	@echo "  build-ci-app: Build app for CI"
	@echo "  run-ci-test: Run tests in CI"
	@echo "  lock-pckgs: Lock dependencies"
	@echo "  format: Format code"
	@echo "  run-and-build: Build app and run"
	@echo "  help: Show this help message"
	@echo ""
