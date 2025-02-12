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
