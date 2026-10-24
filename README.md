# 🏎️ PitStop — Docker Healthchecks & Restart Policy Lab

PitStop is a hands-on DevOps reliability lab that simulates a motorsports telemetry service. It demonstrates how to containerize a Python application, monitor application health, inject controlled faults, and observe Docker's restart behavior.

The goal is to understand the difference between **a running container, a healthy application, and an automatically restarted process**.

## 🎯 Project objectives

- Build a lightweight HTTP service using Python.
- Package the application using Docker.
- Use Docker Compose to configure healthchecks and restart policies.
- Simulate application faults and recovery.
- Test application behavior with Python unit tests.
- Automate testing, configuration validation, and image builds with GitHub Actions.

## 🧰 Tech stack

- Python 3.12
- Docker and Docker Compose
- Docker healthchecks
- Python `unittest`
- Git and GitHub
- GitHub Actions

## 🏗️ Architecture

The PitStop telemetry API exposes endpoints for service status and controlled health failures.

- `GET /` — service information
- `GET /health` — returns HTTP 200 when healthy and HTTP 503 when unhealthy
- `POST /fault/on` — simulates a health failure
- `POST /fault/off` — restores health

A marker file represents the injected fault. The health endpoint checks whether this file exists.

## 🚀 Run locally

Clone the repository and move into the project directory:

```bash
git clone <YOUR_REPOSITORY_URL>
cd pitstop
```

Build and start the service:

```bash
docker compose up -d --build
```

Check the container:

```bash
docker compose ps
docker compose logs
```

Test the API:

```bash
curl http://localhost:8080/
curl -i http://localhost:8080/health
```

The API is bound to `127.0.0.1:8080` on the host for local testing.

## 🧪 Experiment 1: Healthcheck failure

Inject a simulated fault:

```bash
curl -X POST http://localhost:8080/fault/on
```

Wait for the configured healthcheck retries, then inspect the container:

```bash
docker inspect pitstop-api \
  --format 'Status={{.State.Status}} Health={{.State.Health.Status}} Restarts={{.RestartCount}}'
```

The healthcheck should eventually report `unhealthy`, while the container remains running.

Restore the service:

```bash
curl -X POST http://localhost:8080/fault/off
```

After the next successful healthcheck attempts, the status should return to `healthy`.

**Key learning:** a failed Docker healthcheck does not, by itself, cause Docker to restart a container under the `unless-stopped` restart policy.

## 🔄 Experiment 2: Automatic restart

The project uses this Compose setting:

```yaml
restart: unless-stopped
```

During development, a temporary `POST /crash` endpoint was used to make the main Python process exit intentionally. This endpoint must be removed from the final version.

After triggering the test, inspect the container:

```bash
docker inspect pitstop-api \
  --format 'Status={{.State.Status}} Restarts={{.RestartCount}}'
```

The observed restart count increased from `0` to `1`, and the container returned to `running`.

**Key learning:** Docker's restart policy responds to the main process exiting. It does not automatically restart a container solely because its health status becomes `unhealthy`.

Do not include the temporary `/crash` endpoint in the published version.

## 🧪 Run unit tests

The health logic is tested using Python's built-in `unittest` framework:

```bash
python3 -m unittest -v
```

The tests cover:
- Healthy status when no fault marker exists
- Unhealthy status when the marker exists
- Recovery after the marker is removed

## ⚙️ Continuous integration

The GitHub Actions workflow runs on pushes and pull requests. It:

1. Checks out the repository.
2. Sets up Python 3.12.
3. Runs the unit tests.
4. Validates the Docker Compose configuration.
5. Builds the Docker image.

## 🧹 Stop the project

```bash
docker compose down
```

## 📚 What I learned

- How to package and run a Python service in Docker.
- How Docker healthchecks monitor application health.
- Why `unhealthy` and `exited` are different container states.
- How Docker restart policies respond to main-process failures.
- How to validate application behavior with unit tests.
- How to automate checks and image builds with GitHub Actions.

## 🔭 Future improvements

- Add structured application logging and metrics.
- Add integration tests for HTTP endpoints.
- Publish the image to a container registry.
- Add a dashboard for health and restart events.
- Explore dedicated health-monitoring and remediation mechanisms.

---

**Built as a hands-on DevOps learning project with a motorsports telemetry theme.**
