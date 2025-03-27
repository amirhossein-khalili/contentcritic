# ContentCritic

ContentCritic is a simple tool that analyzes textual content and provides various content-related insights. You can quickly get started and develop it locally or inside Docker containers using the provided scripts and files.

## Getting Started

- Clone the repository.
- You can find a Postman collection in the `documents` directory to test the available endpoints.

## Docker Usage

- Use the `dockerize.sh` script to build and run the Docker container.
- If you **are not in Iran**, remove `docker.arvancloud.ir/` from the `Dockerfile` and `docker-compose.yml` before running Docker commands.

## Makefile

- A `Makefile` is available to simplify common tasks (e.g., building, running, and stopping containers).
- Just run `make` commands in your terminal for easy development and management of the project.
