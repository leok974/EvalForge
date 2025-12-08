.PHONY: setup web api deploy

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

web:
	. .venv/bin/activate && adk web arcade_app

api:
	. .venv/bin/activate && adk api_server arcade_app

deploy:
	@[ -n "$$GOOGLE_CLOUD_PROJECT" ] || (echo "Set GOOGLE_CLOUD_PROJECT"; exit 1)
	@[ -n "$$GOOGLE_CLOUD_LOCATION" ] || (echo "Set GOOGLE_CLOUD_LOCATION"; exit 1)
	. .venv/bin/activate && adk deploy cloud_run \
		--project=$$GOOGLE_CLOUD_PROJECT \
		--region=$$GOOGLE_CLOUD_LOCATION \
		--service_name=arcade-agents \
		--app_name=arcade \
		--with_ui \
		arcade_app
.PHONY:
boss-smoke
boss-smoke:
.\__pycache__\./scripts/run_boss_smoke.sh
