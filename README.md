# Scrap Project

This project uses Python, Playwright, and pytest for browser automation testing.

## Prerequisites
- Docker installed ([Linux](https://docs.docker.com/engine/install/), [Windows](https://docs.docker.com/desktop/install/windows-install/))

## Build the Docker Image

```bash
docker build -t scrap-test .
```

## Run the Tests (Default: Smoke and Full Run)

```bash
docker run --rm -v $(pwd)/reports:/app/reports scrap-test
```
- The HTML report will be available in your local `reports/` directory after the run.

## Run Only Smoke or Only Smoke and Full Run Tests

- **Smoke tests only:**
  Uncomment the last line in the Dockerfile or override the command:
  ```bash
  docker run --rm scrap-test pytest -m smoke --html=reports/report.html --self-contained-html
  ```

  ```
- **Both suites together (default):**
  ```bash
  docker run --rm scrap-test
  # or
  docker run --rm scrap-test pytest -m "smoke or full_run" --html=reports/report.html --self-contained-html
  ```

## View Logs

Test logs are saved in the `logs/app.log` file inside the container. To view logs after a run:

### On Linux

```bash
docker run --rm -v $(pwd)/logs:/app/logs scrap-test
cat logs/app.log
```

### On Windows (PowerShell)

```powershell
docker run --rm -v ${PWD}/logs:/app/logs scrap-test
Get-Content logs/app.log
```

## Custom Test Run

To run a different test file, override the default command:

```bash
docker run --rm scrap-test pytest tests/test_base.py
```

## Reports

Test reports are saved in the `reports/` directory. Screenshots for failed tests are automatically embedded in the HTML report.

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
- Use `pytest -m smoke` or `pytest -m "smoke or full_run"` to select test groups.

---

For more details, see the source files and configuration in this repository.
