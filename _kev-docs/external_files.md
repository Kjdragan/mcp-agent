# External Files and Dependencies

This document explains all the external files and dependencies that the MCP Basic Agent relies on. Understanding these is crucial for proper agent operation.

## Configuration Files

### 1. mcp_agent.config.yaml

Location: `<project_root>/mcp_agent.config.yaml`

This is the main configuration file for the MCP agent. Here's a breakdown of its key sections:

```yaml
mcp:
  servers:
    fetch:
      transport: stdio
      command: uvx
      args:
        - mcp-server-fetch

    filesystem:
      transport: stdio
      command: node
      args:
        - <path_to_filesystem_server>
        - <allowed_directory_1>
        - <allowed_directory_2>
        - <allowed_directory_3>

execution_engine: asyncio
openai:
  default_model: gpt-4o
```

Key Components:
- **Server Configurations**: Defines how to connect to MCP servers
- **Execution Settings**: Specifies the async execution engine
- **Model Settings**: Configures the LLM provider and model

### 2. .env File

Location: `<project_root>/.env`

Contains sensitive configuration and API keys:

```shell
OPENAI_API_KEY=your_api_key_here
# Other API keys and configuration
```

Important Notes:
- Never commit this file to version control
- Use `.env.example` for documentation
- Required for API authentication

## Required Dependencies

### 1. Python Dependencies

The agent requires several Python packages:

```toml
# pyproject.toml
[project]
dependencies = [
    "python-dotenv",
    "pyyaml",
    "aiohttp",
    "pydantic",
    "openai"
]
```

Key Packages:
- **python-dotenv**: Environment variable management
- **pyyaml**: YAML configuration parsing
- **aiohttp**: Async HTTP client/server
- **pydantic**: Data validation
- **openai**: OpenAI API integration

### 2. External Dependencies

#### Node.js Filesystem Server
- Required for filesystem operations
- Installed globally via npm
- Provides secure file access

#### UV Package Manager
- Used for Python package management
- Handles virtual environment creation
- Manages dependencies efficiently

## Server Components

### 1. Fetch Server

The fetch server provides URL fetching capabilities:
- Handles HTTP/HTTPS requests
- Supports content extraction
- Manages request timeouts
- Handles various content types

Configuration:
```yaml
fetch:
  transport: stdio
  command: uvx
  args:
    - mcp-server-fetch
```

### 2. Filesystem Server

The filesystem server manages file operations:
- Restricted to allowed directories
- Provides file CRUD operations
- Handles directory listings
- Manages file permissions

Configuration:
```yaml
filesystem:
  transport: stdio
  command: node
  args:
    - <path_to_filesystem_server>
    - <allowed_directory_paths>
```

## Directory Structure

Important directories and their purposes:

```
project_root/
├── .env                    # Environment variables
├── .gitignore             # Git ignore patterns
├── mcp_agent.config.yaml  # Main configuration
├── pyproject.toml         # Python project configuration
├── examples/
│   └── mcp_basic_agent/  # Basic agent example
└── schema/               # JSON schemas for validation
```

## Security Considerations

### 1. API Keys
- Store in `.env` file
- Never commit to version control
- Rotate regularly
- Use appropriate permissions

### 2. Filesystem Access
- Restrict to allowed directories
- Use absolute paths
- Validate file operations
- Handle permissions properly

### 3. Server Security
- Use secure transports
- Validate inputs
- Handle errors gracefully
- Log security events

## Logging and Debugging

### 1. Log Files
- Default location: `mcp-agent.log`
- Configurable via YAML
- Contains detailed operation logs
- Useful for troubleshooting

### 2. Debug Configuration
```yaml
logger:
  type: console
  level: info
  path: mcp-agent.log
```

## Common Issues and Solutions

### 1. Configuration Loading
Problem: Configuration not found
Solution: Ensure `mcp_agent.config.yaml` is in the project root

### 2. API Authentication
Problem: API key not loaded
Solution: Check `.env` file and environment variable loading

### 3. Server Connection
Problem: Server not connecting
Solution: Verify server paths and permissions

### 4. File Access
Problem: Permission denied
Solution: Check allowed directories in configuration

## Best Practices

1. **Configuration Management**
   - Use version control for configs (except secrets)
   - Document all configuration options
   - Use environment variables for sensitive data

2. **Security**
   - Follow principle of least privilege
   - Regularly update dependencies
   - Monitor security logs

3. **Maintenance**
   - Keep dependencies updated
   - Monitor log files
   - Regular security audits

## Next Steps

Now that you understand both the code and its external dependencies:
1. Try running the basic agent
2. Experiment with different configurations
3. Explore the available tools
4. Build your own agent implementations

Remember to always refer to this documentation when setting up new agents or troubleshooting issues.
