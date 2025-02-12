# Understanding Context in MCP Agent (Revised)

## 1. Core Data Models

The MCP Agent uses several core data models for managing context and state:

### Global Application Context
```python
class Context(BaseModel):
    """
    Context that is passed around through the application.
    This is a global context that is shared across the application.
    """
    config: Optional[Settings] = None
    executor: Optional[Executor] = None
    human_input_handler: Optional[HumanInputCallback] = None
    signal_notification: Optional[SignalWaitCallback] = None
    upstream_session: Optional[ServerSession] = None
    model_selector: Optional[ModelSelector] = None
    server_registry: Optional[ServerRegistry] = None
    task_registry: Optional[ActivityRegistry] = None
    decorator_registry: Optional[DecoratorRegistry] = None
    tracer: Optional[trace.Tracer] = None
```

### Agent Implementation
```python
class Agent(MCPAggregator):
    """
    An Agent is an entity that has access to a set of MCP servers and can interact with them.
    Each agent should have a purpose defined by its instruction.
    """
    def __init__(
        self,
        name: str,
        instruction: str | Callable[[Dict], str],
        server_names: List[str] = None,
        functions: List[Callable] = None,
        connection_persistence: bool = True,
        human_input_callback: HumanInputCallback = None,
        context: Optional["Context"] = None,
        **kwargs,
    ):
        # ... initialization code
```

## 2. Context Usage in the Application

### How Context Flows
1. **Application Level**:
   - The `MCPApp` class initializes the global context
   - Context is shared across the application through `get_current_context()`

2. **Agent Level**:
   - Agents receive context during initialization
   - They use it to access shared resources and services

3. **Workflow Level**:
   - Workflows maintain their own state through `WorkflowState`
   - They can access global context through their executor

Example of context flow:
```python
# Application initialization
app = MCPApp(name="mcp_application")

# Getting global context
context = get_current_context()

# Creating an agent with context
agent = Agent(
    name="helper",
    instruction="You are a helpful agent",
    context=context
)
```

## 3. State Management

### Workflow State
```python
class WorkflowState(BaseModel):
    """
    Simple container for persistent workflow state.
    This can hold fields that should persist across tasks.
    """
    status: str = "initialized"
    metadata: Dict[str, Any] = Field(default_factory=dict)
    updated_at: float | None = None
    error: Dict[str, Any] | None = None
```

### State Updates
```python
class Workflow(ABC, Generic[T]):
    async def update_state(self, **kwargs):
        """Syntactic sugar to update workflow state."""
        for key, value in kwargs.items():
            self.state[key] = value
            setattr(self.state, key, value)
        self.state.updated_at = datetime.utcnow().timestamp()
```

## Best Practices
1. **Global Context**:
   - Access through `get_current_context()`
   - Use for application-wide services and configurations

2. **Workflow State**:
   - Use for task-specific data
   - Update through the `update_state()` method
   - Record errors using `record_error()`

3. **Agent Context**:
   - Pass context during agent initialization
   - Use for accessing shared resources and services

## Key Differences from Previous Documentation
1. The actual implementation uses a global application context (`Context` class) rather than conversation-specific context
2. State management is primarily handled through `WorkflowState` rather than message history
3. The Agent class focuses on MCP server interactions rather than conversation management
