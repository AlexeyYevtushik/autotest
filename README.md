# Sauce Demo E2E – CI‑First Edition

Enterprise‑grade end‑to‑end framework powered by Python + Playwright + pytest.
All tests run inside Docker and in GitHub Actions with a single command.

Run Locally (<2 min)

### Build image & run tests, reports saved to ./reports
```markdown
docker build -t autotest .
docker run --rm -v ${PWD}/reports:/app/reports autotest
```
## CI / CD (GitHub Actions)

Workflow .github/workflows/ci.yml triggers on:

push (any branch)

pull_request

manual Run workflow button

The job re‑uses the Docker image:

- name: E2E
  run: |
    docker build -t autotest .
    docker run --rm -v ${{ github.workspace }}/reports:/app/reports autotest

If the container exits with code 0 the build passes; HTML and visual‑diff reports are uploaded as artifacts.

## Repo Map (excerpt)
```markdown
/
├── Dockerfile                  # autotest image
├── playwright.config.py        # global Playwright options
├── conftest.py                 # pytest fixtures
└── tests/
    ├── smoke/                  # @pytest.mark.smoke
    │   └── login_test.py
    ├── regression/             # @pytest.mark.full_run
    │   ├── cart_test.py
    │   └── checkout_test.py
    └── visual/
        └── visual_regression_test.py
```
## Highlights & Trade‑offs

Multi‑user coverage – standard, locked‑out, problem, performance‑glitch, error and visual users.

Visual regression – pixel‑perfect diffs via PIL; auto‑attach to HTML report.

Fast feedback – smoke <30 s, full suite ≈ 7 min on GitHub runners.

Docker‑first – no local Python/Node needed; browsers pre‑installed.

CI‑optimised – single image cache keeps runners warm; mounts reports as artifacts.

Limited scope – no mobile emulation or load tests (time‑boxed).

Happy shipping!

