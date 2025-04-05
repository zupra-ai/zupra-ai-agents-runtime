 
# Zupra MCP
 

### 👀  Prerequisites

- Docker
- Docker Compose

## 🔨  Run for Devs

### Run Basic Services

```make ups```

### Run Rest API

```make dev-api``` reachable at [FastAPI Swagger](http://localhost:9000/docs)

### Run Web Application

```make dev``` reachable at [Web Manager](http://localhost:3000)

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

For any questions or feedback, please open an issue on GitHub or contact us at [support@zupra.ai](mailto:support@zupra.ai) or [contact@maxwellsr.com](mailto:contact@maxwellsr.com).

## Additional Resources

- [LICENSE](LICENSE)
- [CONTRIBUTING](CONTRIBUTING.md)
