# zupra.ai Agents Runtime

Welcome to Zupra AI Runtime for Agentic Tools! This project provides a robust runtime environment for managing both autonomous and non-autonomous LLM agents, tools, threads, and more.

## Features

- **Autonomous and Planned Agents Runtime**: Seamlessly manage different types of agents.
- **Tool Management**: Integrate and manage various tools required by your agents.
- **Thread Management**: Efficiently handle multiple threads for concurrent processing.
- **Scalable and Flexible**: Built with Docker, FastAPI, and Redis for scalability and flexibility.

## Getting Started

Follow these steps to set up and run the project:

### Prerequisites

- Docker
- Docker Compose

### Run for Devs
``` make up-s``` for run basic services

``` make dev-api ``` for run Rest API

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
