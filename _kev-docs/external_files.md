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

## Configuration Examples

### 1. Common Configuration Patterns

#### Basic Configuration
```yaml
# Minimal working configuration
mcp:
  servers:
    filesystem:
      transport: stdio
      command: node
      args:
        - <filesystem_server_path>
        - "./allowed/path1"
    fetch:
      transport: stdio
      command: uvx
      args:
        - mcp-server-fetch

openai:
  default_model: gpt-4o
```

#### Advanced Configuration
```yaml
# Production-ready configuration
mcp:
  servers:
    filesystem:
      transport: stdio
      command: node
      args:
        - <filesystem_server_path>
        - "./data"
        - "./configs"
        - "./output"
      read_timeout_seconds: 30
      env:
        NODE_ENV: production
    
    fetch:
      transport: stdio
      command: uvx
      args:
        - mcp-server-fetch
      read_timeout_seconds: 60

execution_engine: asyncio
openai:
  default_model: gpt-4o
  base_url: https://api.openai.com/v1

logger:
  type: console
  level: info
  path: logs/mcp-agent.log
  batch_size: 100
```

### 2. Environment Variables Best Practices

#### Basic .env
```shell
# Minimum required
OPENAI_API_KEY=sk-...

# Optional but recommended
MCP_LOG_LEVEL=info
NODE_ENV=development
```

#### Production .env
```shell
# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...
GOOGLE_API_KEY=...

# Configuration
MCP_LOG_LEVEL=info
NODE_ENV=production
MCP_TIMEOUT_SECONDS=60
MCP_MAX_RETRIES=3

# Paths
MCP_CONFIG_PATH=/etc/mcp/config.yaml
MCP_LOG_PATH=/var/log/mcp/agent.log
```

## Real-World Configuration Scenarios

### 1. Development Setup
```yaml
# mcp_agent.config.yaml
mcp:
  servers:
    filesystem:
      transport: stdio
      command: node
      args:
        - "./dev/data"
        - "./dev/temp"
      env:
        NODE_ENV: development
logger:
  level: debug
  console_debug: true
```

### 2. Production Setup
```yaml
# mcp_agent.config.yaml
mcp:
  servers:
    filesystem:
      transport: stdio
      command: node
      args:
        - "/data/prod"
        - "/data/backup"
      env:
        NODE_ENV: production
logger:
  level: info
  path: /var/log/mcp/agent.log
  batch_size: 1000
```

### 3. Testing Setup
```yaml
# mcp_agent.config.yaml
mcp:
  servers:
    filesystem:
      transport: stdio
      command: node
      args:
        - "./test/fixtures"
      env:
        NODE_ENV: test
logger:
  level: debug
  console_debug: true
```

## Configuration Troubleshooting

### 1. YAML Validation Errors

```yaml
# ❌ Invalid Configuration
mcp:
  servers:
    filesystem:
      transport: invalid  # Error: must be 'stdio'
      command: node
      args:
        - path1
        - path2

# ✅ Fixed Configuration
mcp:
  servers:
    filesystem:
      transport: stdio    # Fixed: using valid transport
      command: node
      args:
        - path1
        - path2
```

### 2. Path Resolution Issues

```yaml
# ❌ Problematic Paths
filesystem:
  args:
    - "C:\Program Files\data"  # Error: backslashes
    - "./relative/path"        # Warning: relative path

# ✅ Fixed Paths
filesystem:
  args:
    - "C:/Program Files/data"  # Fixed: forward slashes
    - "/absolute/path"         # Fixed: absolute path
```

### 3. Environment Loading Issues

```python
# ❌ Common Problems
env_path = '.env'  # Error: relative path
load_dotenv(env_path)

# ✅ Fixed Loading
env_path = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(env_path)
```

## Server Configuration Patterns

### 1. Filesystem Server

#### Basic Access
```yaml
filesystem:
  transport: stdio
  command: node
  args:
    - "./data"  # Single directory
```

#### Multi-Directory Access
```yaml
filesystem:
  transport: stdio
  command: node
  args:
    - "./data"          # Main data
    - "./temp"          # Temporary files
    - "./user_files"    # User uploads
```

#### Restricted Access
```yaml
filesystem:
  transport: stdio
  command: node
  args:
    - "./data/read_only"     # Read-only data
    - "./data/temp"          # Temporary storage
  env:
    RESTRICT_WRITE: "true"   # Enable write restrictions
```

### 2. Fetch Server

#### Basic Setup
```yaml
fetch:
  transport: stdio
  command: uvx
  args:
    - mcp-server-fetch
```

#### With Timeouts
```yaml
fetch:
  transport: stdio
  command: uvx
  args:
    - mcp-server-fetch
    - --timeout=30
  read_timeout_seconds: 30
```

#### With Rate Limiting
```yaml
fetch:
  transport: stdio
  command: uvx
  args:
    - mcp-server-fetch
    - --rate-limit=10
    - --rate-window=60
```

## Best Practices Checklist

### 1. Security
- [ ] Use absolute paths
- [ ] Restrict directory access
- [ ] Keep API keys in .env
- [ ] Set appropriate timeouts
- [ ] Enable logging

### 2. Performance
- [ ] Configure batch sizes
- [ ] Set appropriate timeouts
- [ ] Enable caching if needed
- [ ] Configure rate limits

### 3. Maintenance
- [ ] Use clear directory structure
- [ ] Document all configurations
- [ ] Set up logging
- [ ] Configure error handling
