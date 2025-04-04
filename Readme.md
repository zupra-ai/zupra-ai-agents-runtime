![Logo](https://github.com/zupra-ai/zupra-ai-agents-runtime/blob/main/assets/logo.png)

# Zupra MCP

Welcome to Zupra AI Runtime for Agentic Tools! This project provides a robust runtime environment for  autonomous and planned LLM Agents, tools, threads and memory.

## Table of Contents

- [Zupra MCP](#zupra-mcp)
  - [Table of Contents](#table-of-contents)
  - [Architecture](#architecture)
  - [🚀   Getting Started](#---getting-started)
    - [👀  Prerequisites](#--prerequisites)
  - [🔨  Run for Devs](#--run-for-devs)
    - [Run Basic Services](#run-basic-services)
    - [Run Rest API](#run-rest-api)
    - [Run Web Application](#run-web-application)
    - [Installation](#installation)
    - [Configuration](#configuration)
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

## 🔨  Run for Devs

### Run Basic Services

```make ups```

### Run Rest API

```make dev-api``` reachable at [FastAPI Swagger](http://localhost:9000/docs)

### Run Web Application

```make dev-web``` reachable at [Web Manager](http://localhost:5173)

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

### Configuration

Configure your agents, tools, and threads in the `config` directory. Update the `config.yaml` file to suit your needs.
 
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
