# Updating Swarm Agent Implementation

## Current Issues

The Swarm agent is failing with the error:
```
AttributeError: 'NoneType' object has no attribute 'api_key'
```

This indicates that the Anthropic configuration is not properly set up, similar to issues we previously resolved in the basic agent.

## Required Changes

Based on the working basic agent implementation, we need to make the following updates to the Swarm agent:

### 1. Environment Configuration
- Add `.env` file loading support
- Ensure proper API key loading
```python
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(env_path)
```

### 2. Configuration File Updates

#### Current Basic Agent Config (Working)
```yaml
execution_engine: asyncio
logger:
  type: composite
  level: info
  console_enabled: "True"
  file_enabled: "True"
  http_enabled: "False"

mcp:
  servers:
    fetch:
      command: "uvx"
      args: ["mcp-server-fetch"]
    filesystem:
      command: "node"
      args: [
        "path_to_filesystem_server",
        "allowed_directory_1",
        "allowed_directory_2"
      ]

openai:
  default_model: "gpt-4o"
```

#### Required Updates for Swarm Agent
1. Update `mcp_agent.config.yaml`:
   - Add Anthropic configuration section
   - Update server configurations to match basic agent
   - Ensure proper logging configuration

2. Update `mcp_agent.secrets.yaml`:
   - Add Anthropic API key
   - Ensure all necessary API keys are present
   - Follow same structure as basic agent

### 3. Server Configuration
1. Update filesystem server paths:
```yaml
filesystem:
  command: "node"
  args: [
    "C:\\Users\\kevin\\AppData\\Roaming\\npm\\node_modules\\@modelcontextprotocol\\server-filesystem\\dist\\index.js",
    "C:/Users/kevin/ClaudeMCPFolder",
    "H:/temp storage",
    "C:/Users/kevin/OneDrive/Desktop"
  ]
```

### 4. Implementation Changes

1. Add environment loading to `main.py`:
```python
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path(__file__).resolve().parents[2] / '.env'
print(f"Loading .env from: {env_path}")
load_dotenv(env_path)
```

2. Update Anthropic configuration handling:
```python
# In main.py or relevant configuration file
anthropic_config = {
    "api_key": os.getenv("ANTHROPIC_API_KEY"),
    # Add other necessary Anthropic configurations
}
```

## Implementation Steps

1. Environment Setup
   - Copy `.env` file from basic agent
   - Verify API keys are properly loaded

2. Configuration Files
   - Update `mcp_agent.config.yaml`
   - Create/update `mcp_agent.secrets.yaml`
   - Verify server configurations

3. Code Updates
   - Add environment loading
   - Update configuration handling
   - Verify server connections

4. Testing
   - Test server connections
   - Verify API key loading
   - Test basic agent functionality

## Notes

- Keep existing Swarm agent functionality unchanged
- Only update configuration and environment handling
- Maintain compatibility with existing policies
- Follow the same error handling patterns as basic agent

## Additional Considerations

1. Error Handling
   - Add proper error messages for missing configurations
   - Implement graceful fallbacks where appropriate
   - Maintain existing error isolation patterns

2. Logging
   - Ensure consistent logging format
   - Maintain debug information
   - Follow basic agent logging patterns

3. Security
   - Keep API keys in appropriate configuration files
   - Use environment variables for sensitive data
   - Follow existing security patterns

## Future MCP Server Integrations

While the Swarm agent currently only requires the basic `fetch` and `filesystem` servers, we may want to integrate additional MCP servers in the future for enhanced functionality:

### Priority Integration Candidates
1. **Google Drive MCP**
   - Document storage and retrieval
   - Collaborative file access
   - Integration with Google Workspace

2. **GitHub MCP**
   - Code repository access
   - Issue tracking
   - Pull request management
   - Version control integration

3. **Postgres MCP**
   - Database operations
   - Structured data storage
   - Query execution
   - Data persistence

4. **Puppeteer MCP**
   - Web automation
   - UI testing
   - Web scraping
   - Browser interaction

5. **Qdrant MCP**
   - Vector storage
   - Similarity search
   - RAG implementation
   - Embedding management

### Integration Considerations
1. **Implementation Priority**
   - Start with most impactful integrations
   - Consider use case requirements
   - Evaluate community support

2. **Configuration Updates**
   - Each MCP will need its own config section
   - API keys and authentication
   - Server-specific settings

3. **Security Considerations**
   - Access control
   - API key management
   - Data privacy

4. **Performance Impact**
   - Connection pooling
   - Resource management
   - Scaling considerations

### Implementation Notes
- Check MCP community for pre-built implementations
- Consider building custom MCPs if needed
- Maintain compatibility with existing agent functionality
- Document each integration thoroughly
