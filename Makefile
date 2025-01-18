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


.PHONY: make-migrations
make_migrations:
	$(call e_info,"Creating migrations...")
	docker-compose run --rm $(APP_NAME) python src/manage.py makemigrations

.PHONY: migrate
migrate:
	$(call e_info,"Migrating...")
	docker-compose run --rm $(APP_NAME) python src/manage.py migrate

.PHONY: run-test
run_test:
	$(call e_info,"Running tests...")
	docker-compose run --rm $(APP_NAME) pytest $(ARGS)

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