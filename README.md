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

## Running Tests with Docker

1. **Build the Docker image:**
   ```sh
   docker build -t myimage .
   ```
2. **Run the tests and generate the HTML report:**
   ```sh
   docker run --rm -v $(pwd)/reports:/app/reports myimage
   ```
   - The test report will be available on your host in the `reports/` directory as `report.html`.

3. **Test selection:**
   - To run only smoke tests, edit the `CMD` in the Dockerfile to:
     ```dockerfile
     CMD ["pytest","-m smoke", "--html=reports/report.html", "--self-contained-html"]
     ```
   - To run both smoke and full_run tests, use:
     ```dockerfile
     CMD ["pytest","-m smoke or full_run", "--html=reports/report.html", "--self-contained-html"]
     ```

4. **Requirements:**
   - Ensure `pytest-html` is listed in your `requirements.txt`.
   - The Dockerfile creates and sets permissions for the `reports/` directory automatically.

5. **Accessing the report:**
   - After the container finishes, open `reports/report.html` in your browser to view the results and screenshots for failed tests.

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
- Full run takes less then 7 minutes. Smoke run takes about 30 seconds

---

For more details, see the source files and configuration in this repository.
