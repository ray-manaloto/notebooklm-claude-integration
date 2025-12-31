.PHONY: codex-skill-e2e
.PHONY: codex-ask-all
.PHONY: codex-ask-all-subagents
.PHONY: codex-validate
.PHONY: codex-bootstrap-parallel
.PHONY: codex-bootstrap-auth

codex-skill-e2e:
	./scripts/codex-skill-e2e.sh

codex-ask-all:
	./scripts/codex-ask-all.sh

codex-ask-all-subagents:
	./scripts/codex-ask-all-subagents.sh

codex-validate:
	./scripts/codex-validate-setup.sh

codex-bootstrap-parallel:
	./scripts/codex-bootstrap-parallel.sh

codex-bootstrap-auth:
	./scripts/codex-bootstrap-auth.sh
