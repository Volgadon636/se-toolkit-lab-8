# Project Setup Guide

This guide outlines the steps to set up the development environment for this project.

## Prerequisites

Ensure you have the following tools installed on your system:

*   **Docker & Docker Compose**: For running services in containers.
    *   [Install Docker](https://docs.docker.com/engine/install/)
    *   [Install Docker Compose](https://docs.docker.com/compose/install/)
*   **Nix (Optional, Recommended)**: For managing development environments and dependencies.
    *   [Install Nix](https://nixos.org/download/)
*   **Direnv (Optional, Recommended)**: To automatically load/unload environment variables.
    *   [Install Direnv](https://direnv.net/)

## 1. Environment Setup

### Using Nix (Recommended)

If you have Nix installed, you can set up the development environment by simply running the following command in the project root:

```bash
nix develop
```

This will provision all necessary tools and dependencies (like Python, Node.js, pnpm, uv) defined in `flake.nix`.

If you are using `direnv`, after installing Nix, you can enable it for the project:

```bash
direnv allow
```

### Manual Setup (Alternative)

If you prefer not to use Nix or encounter issues, you can set up the backend and frontend environments manually.

#### Backend (`backend/`)

1.  **Install `uv`**: If not already available (e.g., via Nix), install `uv`.
    ```bash
    pip install uv
    ```
2.  **Install Python Dependencies**: Navigate to the `backend/` directory and install dependencies.
    ```bash
    cd backend
    uv sync
    ```
3.  **Environment Variables**: Create a `.env` file based on the example.
    ```bash
    cp .env.tests.e2e.example .env.tests.e2e
    cp .env.tests.unit.example .env.tests.unit
    # You might need to create a general .env for local development if one is not provided, consulting documentation or other examples.
    ```

#### Frontend (`client-web-react/`)

1.  **Install `pnpm`**: If not already available (e.g., via Nix), install `pnpm`.
    ```bash
    npm install -g pnpm
    ```
2.  **Install Node.js Dependencies**: Navigate to the `client-web-react/` directory and install dependencies.
    ```bash
    cd client-web-react
    pnpm install
    ```
3.  **Environment Variables**: Create a `.env` file based on the example.
    ```bash
    cp .env.example .env
    ```

## 2. Running the Application with Docker Compose

Once the prerequisites are met and your environment is set up (either via Nix or manually), you can start all services using Docker Compose from the project root directory:

```bash
docker-compose up --build
```

This command will:
*   Build Docker images (if not already built or if `--build` is specified).
*   Start all services defined in `docker-compose.yml` (e.g., backend, frontend, database, Caddy gateway, etc.).

## 3. Accessing the Application

After `docker-compose up` completes, you should be able to access the different parts of the application:

*   **Frontend**: Typically available at `http://localhost:3000` (or similar, check `client-web-react` configuration).
*   **Backend API**: Typically available at `http://localhost:8000` (or similar, check `backend` configuration).
*   **Caddy Gateway**: If configured, it might serve as a reverse proxy for both frontend and backend.

Consult individual service documentation or configuration files for exact ports and paths.