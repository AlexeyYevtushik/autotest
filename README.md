# Scrap Project

This project uses Python, Playwright, and pytest for browser automation testing.

## Prerequisites
- Docker installed ([Linux](https://docs.docker.com/engine/install/), [Windows](https://docs.docker.com/desktop/install/windows-install/))

## Build the Docker Image

```
docker build -t scrap-test .
```

## Run the Tests

```
docker run --rm scrap-test
```

## View Logs

Test logs are saved in the `logs/app.log` file inside the container. To view logs after a run:

### On Linux

1. Run the container and mount the logs directory:
   ```
   docker run --rm -v $(pwd)/logs:/app/logs scrap-test
   cat logs/app.log
   ```

### On Windows (PowerShell)

1. Run the container and mount the logs directory:
   ```
   docker run --rm -v ${PWD}/logs:/app/logs scrap-test
   Get-Content logs/app.log
   ```

## Custom Test Run

To run a different test file, override the default command:

```
docker run --rm scrap-test pytest tests/test_base.py
```

## Reports

Test reports are saved in the `reports/` directory.

## Running with Docker

1. Build the Docker image:
   ```bash
   docker build -t swag-e2e .
   ```

2. Run the tests in a container:
   ```bash
   docker run --rm -v $(pwd)/reports:/app/reports swag-e2e
   ```
   - The HTML report will be available in your local `reports/` directory after the run.

## Requirements
- Python 3.12 (or as specified in Dockerfile)
- [pytest](https://docs.pytest.org/)
- [pytest-html](https://pypi.org/project/pytest-html/)
- [playwright](https://playwright.dev/python/)

All dependencies are listed in `requirements.txt` and installed automatically in Docker.

## Manual Local Run
If you want to run tests locally (not in Docker):

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install --with-deps chromium
   ```
2. Run tests and generate HTML report:
   ```bash
   pytest --html=reports/report.html --self-contained-html
   ```

## Notes
- Screenshots for failed tests are automatically embedded in the HTML report.
- Configuration is in `config.json`.
- Test results and reports are in the `reports/` directory.

---

For more details, see the source files and configuration in this repository.
