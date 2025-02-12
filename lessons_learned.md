# MCP Agent Project - Lessons Learned

## Project Setup and Configuration

### Environment Management
1. Using UV Package Manager
   - Project uses UV for dependency management
   - Virtual environment is created with Python 3.12
   - Dependencies are managed through `pyproject.toml`
   - Installation command: `uv pip install -e .` for editable mode

### Configuration Files
1. MCP Agent Configuration
   - Moved `mcp_agent.config.yaml` to project root for proper loading
   - Configuration includes:
     - Fetch server using `uvx`
     - Filesystem server with multiple allowed directories:
       - `C:/Users/kevin/ClaudeMCPFolder`
       - `H:/temp storage`
       - `C:/Users/kevin/OneDrive/Desktop`
     - OpenAI model set to `gpt-4o`

2. Environment Variables
   - `.env` file in project root for API keys and configuration
   - Cleaned up unused API keys and configurations
   - Critical variables:
     - `OPENAI_API_KEY` for LLM functionality
     - Various other API keys for optional integrations

### Code Structure
1. Example Scripts
   - `examples/mcp_basic_agent/main.py` demonstrates basic agent usage
   - Environment variables loaded using `python-dotenv`
   - Explicit path resolution for `.env` file using `Path(__file__).resolve().parents[2]`

### Server Configuration
1. Filesystem Server
   - Node.js-based server for filesystem operations
   - Configured with specific allowed directories for security
   - Provides comprehensive file operations (read, write, list, search)

2. Fetch Server
   - Uses `uvx` command for URL fetching
   - Supports markdown extraction and content limiting

## Best Practices Identified
1. Environment Variables
   - Always load `.env` file explicitly with full path resolution
   - Verify environment variable loading with debug logging
   - Keep sensitive keys in `.env` and add to `.gitignore`

2. Configuration
   - Keep configuration files at project root for easier access
   - Use YAML for readable configuration
   - Document all server endpoints and allowed paths

3. Code Organization
   - Separate examples into their own directories
   - Use descriptive logging for debugging
   - Handle errors gracefully with informative messages

## Logging System Improvements

### Logger Validation and Type Safety (2025-02-12)
- Fixed validation error in logger configuration by enforcing single transport type
- Improved type safety in LoggerSettings class
- Enhanced error messages for configuration validation
- Added better documentation for logger configuration options

Key files modified:
- `src/mcp_agent/config.py`: Updated LoggerSettings validation
- `mcp_agent.config.yaml`: Fixed logger type configuration

Benefits:
- More reliable configuration validation
- Clearer error messages
- Better type safety
- Improved developer experience

### Multiple Transport Support (2025-02-12)
- Added `CompositeTransport` to support multiple logging outputs simultaneously
- Enhanced `LoggerSettings` with composite transport configuration
- Users can now enable/disable console, file, and HTTP outputs independently
- Improved configuration organization and documentation
- Added parallel event processing for multiple transports
- Added graceful error handling for transport failures

Key files modified:
- `src/mcp_agent/logging/transport.py`: Added CompositeTransport class
- `src/mcp_agent/config.py`: Updated LoggerSettings
- `mcp_agent.config.yaml`: Updated logger configuration

Benefits:
- More flexible logging configuration
- Better debugging capabilities with multiple outputs
- Improved error visibility
- Enhanced system observability

## Logging Configuration and Debugging (2025-02-12)

### Logging Level Configuration
1. Config File Method
   - Set in `mcp_agent.config.yaml`:
   ```yaml
   logger:
     type: composite
     level: debug  # or "info" for less verbose logging
     path: _logs/mcp-agent-{timestamp}.log
   ```

2. Environment Variable Method
   - Set using `MCP_AGENT__LOGGER__LEVEL=debug`
   - Takes precedence over config file setting

### Config File Loading
- Config file must be explicitly loaded in custom applications
- Use `get_settings()` to load and validate config:
```python
from pathlib import Path
from mcp_agent.config import get_settings
from mcp_agent.app import MCPApp

config_path = Path(__file__).parent / 'mcp_agent.config.yaml'
settings = get_settings(config_path)
app = MCPApp(name="app_name", settings=settings)
```

### Debug Logging Features
1. Message Details
   - Full message structures before OpenAI API calls
   - Complete OpenAI API request/response details
   - Tool registration and capabilities
   - Function call details and results

2. Server Communication
   - MCP server initialization logs
   - Server capability negotiation
   - Tool registration process
   - Session management details

3. Log File Organization
   - Stored in `_logs` directory
   - Filename format: `mcp-agent-{timestamp}.log`
   - Both console and file logging supported
   - Automatic redaction of sensitive information

### Best Practices
1. Development and Debugging
   - Use debug level during development
   - Monitor both console and file outputs
   - Check logs for sensitive information leaks
   - Use log files for troubleshooting

2. Production Settings
   - Set appropriate log level ("info" recommended)
   - Configure log rotation if needed
   - Monitor log file sizes
   - Regular log cleanup

3. Security Considerations
   - Verify sensitive data redaction
   - Protect log file access
   - Regular log review for security
   - Proper log file permissions

### Known Issues and Solutions
1. Config Loading
   - Config file must be explicitly loaded
   - Path must be correctly resolved
   - Settings must be passed to MCPApp

2. Log Level Override
   - Environment variable takes precedence
   - Config file setting as fallback
   - Runtime changes possible through settings

### Future Improvements
1. Consider adding:
   - Log rotation configuration
   - Custom log formatters
   - Additional transport options
   - Enhanced security filtering

## Context Management System

### Core Architecture and Documentation (2025-02-12)
- Created comprehensive documentation of the context management system
- Added detailed implementation examples and best practices
- Documented core architecture and design patterns
- Added guidance for common use cases and patterns

Key files modified:
- `_kev-docs/understanding_context_revised_v2.md`: Added detailed system documentation
- `lessons_learned.md`: Updated with context management insights

Benefits:
- Better understanding of context management system
- Clear guidelines for implementation
- Documented best practices and patterns
- Improved maintainability and scalability
- Easier onboarding for new developers

### Core Architecture
1. Global Context
   - Implemented as a singleton accessible via `get_current_context()`
   - Contains shared resources like executors, model selectors, and registries
   - Initialized during MCPApp startup

2. Context Inheritance
   - `ContextDependent` mixin provides context access to components
   - Components can have instance-specific context or fall back to global
   - Clear error messages when context is missing

### Best Practices
1. Context Access
   - Always inherit from `ContextDependent` for components needing context
   - Use instance context when possible, fall back to global when needed
   - Handle missing context gracefully with informative error messages

2. Context Flow
   - Top-down: MCPApp initializes global context
   - Horizontal: Components share context within workflows
   - Bottom-up: Tasks update workflow state, propagate to global

3. Error Handling
   - Wrap context-dependent operations in try-except blocks
   - Provide clear error messages about missing context or resources
   - Use context managers for resource cleanup

### Advanced Features
1. Parallel Processing
   - Fan-out/fan-in pattern for parallel task execution
   - Each agent maintains its own context while sharing global resources
   - Context switching available for temporary operations

2. State Management
   - Workflow state persists across tasks
   - Error state captures full context
   - Metadata for custom state tracking

### Common Patterns
1. Sequential Processing
   ```python
   async with executor.execution_context():
       result = await model.generate(prompt)
   ```

2. Parallel Processing
   ```python
   fan_out = FanOut(agents=agents, context=context)
   results = await fan_out.generate(input)
   ```

3. Context Switching
   ```python
   with component.use_context(temp_context):
       result = await component.process()
   ```

### Known Limitations
1. Context must be initialized before component usage
2. Global context is shared across all components
3. Care needed when switching contexts in parallel operations

### Future Improvements
1. Consider adding context isolation for parallel operations
2. Implement context versioning for state management
3. Add more comprehensive error handling and recovery
4. Consider adding context validation mechanisms

## Next Steps and Improvements
1. Consider adding more example scripts for different use cases
2. Improve error handling for missing directories or permissions
3. Add documentation for common operations and configurations
4. Consider adding tests for configuration loading and server operations

## Known Limitations
1. Filesystem server only works within explicitly allowed directories
2. Configuration must be in project root
3. Some operations require specific environment variables to be set

## Dependencies
- Python 3.12
- UV package manager
- Node.js (for filesystem server)
- OpenAI API key
- Various optional API keys for additional functionality
