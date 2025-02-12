# Code Walkthrough: MCP Basic Agent

This document provides a detailed walkthrough of the MCP Basic Agent implementation, focusing on the code in `examples/mcp_basic_agent/main.py`.

## Project Structure

```
examples/mcp_basic_agent/
├── main.py                 # Main agent implementation
└── mcp_agent.config.yaml   # Agent configuration (moved to root)
```

## Main Script Analysis

Let's break down the main.py file section by section:

### 1. Imports and Setup

```python
import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(env_path)

from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM
```

Key Points:
- Uses `pathlib` for cross-platform path handling
- Loads environment variables from the project root's `.env` file
- Imports necessary MCP components

### 2. Application Initialization

```python
app = MCPApp(name="mcp_basic_agent")
```

The `MCPApp` class:
- Manages the agent's lifecycle
- Handles configuration loading
- Sets up logging
- Provides context management

### 3. Main Example Function

```python
async def example_usage():
    async with app.run() as agent_app:
        logger = agent_app.logger
        context = agent_app.context

        logger.info("Current config:", data=context.config.model_dump())
```

This section:
- Uses async context manager for proper resource management
- Gets logger and context from the app
- Logs the current configuration for debugging

### 4. Agent Creation and Configuration

```python
        finder_agent = Agent(
            name="finder",
            instruction="""You are an agent with access to the filesystem, 
            as well as the ability to fetch URLs. Your job is to identify 
            the closest match to a user's request, make the appropriate tool calls, 
            and return the URI and CONTENTS of the closest match.""",
            server_names=["fetch", "filesystem"],
        )
```

The Agent configuration:
- Gives the agent a name ("finder")
- Provides instructions for its behavior
- Specifies which servers it can access

### 5. Agent Usage

```python
        async with finder_agent:
            logger.info("finder: Connected to server, calling list_tools...")
            result = await finder_agent.list_tools()
            logger.info("Tools available:", data=result.model_dump())
```

This section:
- Uses context manager for agent lifecycle
- Lists available tools from connected servers
- Logs tool information for debugging

### 6. LLM Integration

```python
            llm = await finder_agent.attach_llm(OpenAIAugmentedLLM)
            result = await llm.generate_str(
                message="List all files in C:/Users/kevin/ClaudeMCPFolder",
            )
            logger.info(f"Result: {result}")
```

LLM usage:
- Attaches OpenAI's LLM to the agent
- Sends a message for processing
- Logs the result

### 7. Main Entry Point

```python
if __name__ == "__main__":
    import time
    start = time.time()
    asyncio.run(example_usage())
    end = time.time()
    t = end - start
```

Entry point:
- Measures execution time
- Uses asyncio.run() to handle async code
- Provides timing information

## Understanding the Code Flow

Let's walk through how the code actually works in practice:

### 1. Startup Sequence

When you run `main.py`, this is what happens behind the scenes:

```python
# 1. Environment Loading
env_path = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(env_path)
```
This loads your OpenAI API key and other secrets. Without this, the agent can't authenticate with OpenAI.

```python
# 2. App Creation
app = MCPApp(name="mcp_basic_agent")
```
The app is created and immediately:
- Loads `mcp_agent.config.yaml` from the project root
- Sets up logging (you'll see this in your terminal)
- Initializes the execution engine (asyncio)

### 2. Real-World Example: File Listing

Let's break down what happens when the agent lists files:

```python
async with finder_agent:
    # 1. Server Connection
    # The agent connects to both the filesystem and fetch servers
    # You'll see log messages for each connection
    
    # 2. Tool Discovery
    result = await finder_agent.list_tools()
    # This shows you what operations are available
    # e.g., read_file, list_directory, fetch_url, etc.
    
    # 3. LLM Attachment
    llm = await finder_agent.attach_llm(OpenAIAugmentedLLM)
    
    # 4. File Listing Request
    result = await llm.generate_str(
        message="List all files in C:/Users/kevin/ClaudeMCPFolder",
    )
    # The LLM:
    # a) Understands the natural language request
    # b) Chooses the appropriate tool (filesystem-list_directory)
    # c) Calls the tool with the correct path
    # d) Formats the response for human reading
```

### 3. Behind the Scenes: Server Communication

When the agent talks to servers, here's what's happening:

```python
# 1. Filesystem Server
filesystem_server = {
    "transport": "stdio",  # Uses standard I/O for communication
    "command": "node",     # Runs a Node.js server
    "args": [
        # The server is given specific allowed directories
        "C:/Users/kevin/ClaudeMCPFolder",
        "H:/temp storage",
        "C:/Users/kevin/OneDrive/Desktop"
    ]
}

# 2. Communication Flow
# When you request "List files in directory":
# a) Agent → LLM: "What tool should I use?"
# b) LLM → Agent: "Use filesystem-list_directory"
# c) Agent → Filesystem Server: JSON request with path
# d) Server: Checks if path is allowed
# e) Server → Agent: JSON response with file list
# f) Agent → LLM: "Format this response"
# g) LLM → User: Formatted file list
```

### 4. Error Handling Examples

Here's how the agent handles common issues:

```python
# 1. Invalid Directory
try:
    result = await llm.generate_str(
        message="List files in C:/NotAllowed",
    )
except Exception as e:
    # The filesystem server will reject this
    # You'll see: "Path not in allowed directories"
    logger.error(f"Access denied: {e}")

# 2. API Key Issues
if not os.getenv("OPENAI_API_KEY"):
    # The agent will fail early with a clear message
    # You'll see: "OpenAI API key not found"
    logger.error("Missing API key")

# 3. Server Connection Issues
async with finder_agent:
    try:
        # If the filesystem server isn't running
        # You'll see: "Failed to connect to server"
        await finder_agent.connect()
    except ConnectionError as e:
        logger.error(f"Server connection failed: {e}")
```

### 5. Debugging Tips

When something goes wrong, here's what to check:

1. **Check the Logs**
   ```python
   # Look for these log messages:
   "Loading .env from: ..."        # Confirms env loading
   "Current config: ..."           # Shows loaded config
   "Connected to server ..."       # Server connections
   "Tools available: ..."          # Available operations
   ```

2. **Common Issues**
   - If OpenAI calls fail: Check `.env` and `OPENAI_API_KEY`
   - If file operations fail: Check allowed directories in config
   - If servers won't connect: Check Node.js installation

3. **Adding Debug Logging**
   ```python
   # Add these to debug issues:
   logger.info("Config loaded:", data=context.config.model_dump())
   logger.info("Attempting server connection...")
   logger.info("Tool call result:", data=result.model_dump())
   ```

### 6. Tool Usage Examples

Here's how different tools are used:

```python
# 1. Reading a File
result = await llm.generate_str(
    message="Read the contents of config.txt",
)
# The agent will:
# a) Check if the file is in an allowed directory
# b) Use filesystem-read_file
# c) Return the contents

# 2. Fetching a URL
result = await llm.generate_str(
    message="Get content from https://example.com",
)
# The agent will:
# a) Use the fetch server
# b) Download and process the content
# c) Return formatted results

# 3. Combined Operations
result = await llm.generate_str(
    message="Find config files and check their URLs",
)
# The agent will:
# a) List directories for config files
# b) Read found files
# c) Extract and verify URLs
# d) Return a summary
```

## Key Concepts Demonstrated

### 1. Async/Await Pattern
- Uses Python's async/await for non-blocking operations
- Properly manages async contexts
- Handles concurrent operations efficiently

### 2. Resource Management
- Uses context managers (`async with`)
- Properly initializes and cleans up resources
- Handles connections systematically

### 3. Error Handling
- Implements proper error handling patterns
- Uses logging for debugging
- Manages exceptions appropriately

### 4. Configuration Management
- Loads environment variables
- Uses configuration files
- Manages server settings

### 5. Tool Discovery and Usage
- Lists available tools
- Uses tools through the agent
- Handles tool responses

## Common Patterns

### 1. Initialization Pattern
```python
app = MCPApp(name="mcp_basic_agent")
async with app.run() as agent_app:
    # Use agent_app
```

### 2. Agent Creation Pattern
```python
agent = Agent(name="name", instruction="instruction", server_names=["server1", "server2"])
async with agent:
    # Use agent
```

### 3. LLM Usage Pattern
```python
llm = await agent.attach_llm(LLMClass)
result = await llm.generate_str(message="message")
```

## Best Practices Demonstrated

1. **Configuration Management**
   - External configuration files
   - Environment variables for secrets
   - Clear separation of concerns

2. **Resource Management**
   - Proper use of context managers
   - Clean resource cleanup
   - Explicit resource allocation

3. **Error Handling**
   - Comprehensive logging
   - Proper exception handling
   - Debugging information

4. **Code Organization**
   - Clear function separation
   - Logical component organization
   - Well-structured async code

## Next Steps

Now that you understand the code implementation, proceed to [External Files and Dependencies](./external_files.md) to learn about the supporting files and systems that make the agent work.
