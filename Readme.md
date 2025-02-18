# Zupra Runtime | Agentic Applications Runtime

Welcome to Zupra AI Runtime for Agentic Tools! This project provides a robust runtime environment for managing both autonomous and non-autonomous LLM agents, tools, threads, and more.

## Table of Contents

- [Zupra Runtime | Agentic Applications Runtime](#zupra-runtime--agentic-applications-runtime)
  - [Table of Contents](#table-of-contents)
  - [Architecture](#architecture)
  - [🚀   Getting Started](#---getting-started)
    - [👀  Prerequisites](#--prerequisites)
    - [🔨  Run for Devs](#--run-for-devs)
    - [Installation](#installation)
    - [Configuration](#configuration)
    - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)
  - [Additional Resources](#additional-resources)

## Architecture

![Architecture](https://github.com/zupra-ai/zupra-ai-agents-runtime/blob/main/assets/architecture.png)

## 🚀   Getting Started

Follow these steps to set up and run the project:

### 👀  Prerequisites

- Docker
- Docker Compose

### 🔨  Run for Devs

```make up-s``` for run basic services

```make dev-api``` for run Rest API

### Installation

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/zupra-ai/zupra-ai-agents-runtime.git
    cd zupra-ai-agents-runtime
    ```

2. **Build and Run the Docker Containers**:

    ```bash
    docker-compose up --build
    ```

3. **Access the FastAPI Documentation**:
    Open your browser and navigate to `http://localhost:8000/docs` to explore the API documentation.

### Configuration

Configure your agents, tools, and threads in the `config` directory. Update the `config.yaml` file to suit your needs.

### Usage

1. **Register an Agent**:

Use the FastAPI endpoint to register a new agent.
    ```bash
    curl -X POST "http://localhost:8000/agents/" -H "Content-Type: application/json" -d '{"name": "agent_name", "type": "autonomous"}'
    ```

2. **Manage Tools**:
    Add or remove tools using the provided API endpoints.

3. **Monitor Threads**:
    Check the status of threads and manage them as needed.

## Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contact

For any questions or feedback, please open an issue on GitHub or contact us at support@zupra.ai.

Happy coding!
## Additional Resources

- [LICENSE](LICENSE)
- [CONTRIBUTING](CONTRIBUTING.md)
