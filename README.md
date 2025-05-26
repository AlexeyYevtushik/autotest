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

---

For more details, see the source files and configuration in this repository.
