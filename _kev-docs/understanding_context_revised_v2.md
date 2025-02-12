# Understanding Context in MCP Agent (Revised V2)

## 1. Core Data Models

### Global Application Context
The MCP Agent uses a hierarchical context system:

```python
class Context(BaseModel):
    """
    Global context shared across the application.
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

### Context-Dependent Components
```python
class ContextDependent:
    """
    Mixin class for components that need context access.
    Provides both global fallback and instance-specific context support.
    """
    def __init__(self, context: Optional["Context"] = None, **kwargs):
        self._context = context
        super().__init__(**kwargs)

    @property
    def context(self) -> "Context":
        """Get context, with graceful fallback to global context if needed."""
        if self._context is not None:
            return self._context
        return get_current_context()
```

## 2. Context Usage in Practice

### 1. Application Initialization
```python
# Initialize the application
app = MCPApp(
    name="mcp_application",
    settings=settings,
    human_input_callback=console_input_callback
)

# Context is automatically initialized
context = get_current_context()
```

### 2. Agent Creation and Context Access
```python
class Agent(MCPAggregator):
    """
    An Agent that can interact with MCP servers.
    """
    def __init__(
        self,
        name: str,
        instruction: str,
        context: Optional["Context"] = None,
        **kwargs,
    ):
        super().__init__(context=context, **kwargs)
        self.name = name
        self.instruction = instruction
```

### 3. Workflow State Management
```python
class WorkflowState(BaseModel):
    """Persistent workflow state container"""
    status: str = "initialized"
    metadata: Dict[str, Any] = Field(default_factory=dict)
    updated_at: float | None = None
    error: Dict[str, Any] | None = None
```

## 3. Advanced Context Features

### 1. Temporary Context Switching
```python
@contextmanager
def use_context(self, context: "Context"):
    """Temporarily use a different context."""
    old_context = self._context
    self._context = context
    try:
        yield
    finally:
        self._context = old_context
```

### 2. Context in Parallel Processing
The Fan-Out/Fan-In pattern uses context for parallel task execution:
```python
class FanOut(AugmentedLLM):
    def __init__(
        self,
        agents: List[Agent],
        context: Optional["Context"] = None,
    ):
        super().__init__(context=context)
        self.executor = self.context.executor
        self.agents = agents
```

### 3. Error Handling with Context
```python
def record_error(self, error: Exception) -> None:
    self.error = {
        "type": type(error).__name__,
        "message": str(error),
        "timestamp": datetime.utcnow().timestamp(),
    }
```

## 4. Context Flow in MCP Architecture

### 1. Component Hierarchy
```
MCPApp
  ├── Global Context
  │     ├── Settings
  │     ├── Executor
  │     └── Registries
  │
  ├── Agents
  │     ├── Instance Context
  │     └── Server Connections
  │
  └── Workflows
        ├── Workflow State
        └── Task Context
```

### 2. Context Propagation
1. **Top-Down Flow**:
   - MCPApp initializes global context
   - Components inherit context from parent
   - Each level can override context

2. **Horizontal Flow**:
   - Agents share context within workflow
   - Parallel tasks maintain context isolation
   - Fan-Out/Fan-In preserves context

3. **Bottom-Up Updates**:
   - Tasks update workflow state
   - Workflows report to global context
   - Errors propagate up the chain

## 5. Advanced Context Implementation

### 1. Context Dependent Components
The `ContextDependent` mixin is a fundamental building block that provides context access to components:

```python
class ContextDependent:
    """
    Mixin class for components that need context access.
    Provides both global fallback and instance-specific context support.
    """
    def __init__(self, context: Optional["Context"] = None, **kwargs):
        self._context = context
        super().__init__(**kwargs)

    @property
    def context(self) -> "Context":
        """
        Get context, with graceful fallback to global context if needed.
        Raises clear error if no context is available.
        """
        # First try instance context
        if self._context is not None:
            return self._context

        try:
            # Fall back to global context if available
            from mcp_agent.context import get_current_context
            return get_current_context()
        except Exception as e:
            raise RuntimeError(
                f"No context available for {self.__class__.__name__}. "
                "Either initialize MCPApp first or pass context explicitly."
            ) from e
```

### 2. Agent Context Usage
Agents are a prime example of context-dependent components:

```python
class Agent(MCPAggregator):
    """An Agent that can interact with MCP servers."""
    def __init__(
        self,
        name: str,
        instruction: str | Callable[[Dict], str] = "You are a helpful agent.",
        server_names: List[str] = None,
        functions: List[Callable] = None,
        connection_persistence: bool = True,
        human_input_callback: HumanInputCallback = None,
        context: Optional["Context"] = None,
        **kwargs,
    ):
        super().__init__(
            context=context,
            server_names=server_names or [],
            connection_persistence=connection_persistence,
            **kwargs,
        )
        
        self.name = name
        self.instruction = instruction
        self.functions = functions or []
```

### 3. Parallel Processing with Context
The Fan-Out/Fan-In pattern demonstrates advanced context usage:

```python
class ParallelLLM:
    """
    LLMs can sometimes work simultaneously on a task (fan-out)
    and have their outputs aggregated programmatically (fan-in).
    
    When to use this workflow:
        Parallelization is effective when the divided subtasks can be parallelized
        for speed (sectioning), or when multiple perspectives or attempts are needed for
        higher confidence results (voting).
    """
    def __init__(
        self,
        fan_in_agent: Agent | AugmentedLLM | Callable[[FanInInput], Any],
        fan_out_agents: List[Agent | AugmentedLLM] | None = None,
        fan_out_functions: List[Callable] | None = None,
        llm_factory: Callable[[Agent], AugmentedLLM] = None,
        context: Optional["Context"] = None,
        **kwargs,
    ):
        self.fan_in = FanIn(
            aggregator_agent=fan_in_agent,
            llm_factory=llm_factory,
            context=context,
        )
        self.fan_out = FanOut(
            agents=fan_out_agents,
            functions=fan_out_functions,
            llm_factory=llm_factory,
            context=context,
        )
```

## 6. Practical Examples

### 1. Intent Classification with Context
```python
class LLMIntentClassifier:
    """
    An intent classifier that uses an LLM to determine the user's intent.
    Particularly useful when you need:
    - Flexible understanding of natural language
    - Detailed reasoning about classifications
    - Entity extraction alongside classification
    """
    def __init__(
        self,
        llm: AugmentedLLM,
        intents: List[Intent],
        classification_instruction: str | None = None,
        context: Optional["Context"] = None,
        **kwargs,
    ):
        super().__init__(intents=intents, context=context, **kwargs)
        self.llm = llm
        self.classification_instruction = classification_instruction
```

### 2. Context in Workflow Execution
```python
class Executor:
    @contextmanager
    def execution_context(self):
        """Context manager for execution setup/teardown."""
        try:
            # Set up execution context
            self._setup_execution()
            yield
        finally:
            # Clean up resources
            self._cleanup_execution()
```

## 7. Best Practices and Patterns

### 1. Context Initialization
```python
# Initialize the application with context
app = MCPApp(
    name="mcp_application",
    settings=settings,
    human_input_callback=console_input_callback
)

# Access context in components
class MyComponent(ContextDependent):
    def process(self):
        executor = self.context.executor
        model = self.context.model_selector.select()
```

### 2. Context Switching
```python
class AdvancedProcessor(ContextDependent):
    async def process_with_context(self, temp_context: Context):
        with self.use_context(temp_context):
            # Operations using temporary context
            result = await self.process()
        # Back to original context
        return result
```

### 3. Error Handling
```python
def safe_context_operation(self):
    try:
        executor = self.context.executor
        result = executor.run()
    except AttributeError:
        raise RuntimeError(
            "Executor not available in context. "
            "Ensure MCPApp is initialized with proper settings."
        )
    return result
```

## 8. Context Flow Examples

### 1. Sequential Processing
```python
async def process_workflow(self):
    # Access shared resources
    executor = self.context.executor
    model = self.context.model_selector.select()
    
    # Execute with context
    async with executor.execution_context():
        result = await model.generate(self.prompt)
    
    return result
```

### 2. Parallel Processing
```python
async def parallel_process(self):
    fan_out = FanOut(
        agents=self.processing_agents,
        context=self.context
    )
    
    # Each agent gets context access
    results = await fan_out.generate(self.input)
    
    # Aggregate results with shared context
    aggregator = self.context.get_aggregator()
    final_result = await aggregator.combine(results)
    
    return final_result
```

## Best Practices

1. **Context Access**:
   ```python
   # Prefer instance context
   self.context.executor

   # Fallback to global
   context = get_current_context()
   ```

2. **State Management**:
   ```python
   # Update workflow state
   await self.update_state(
       status="running",
       current_step="processing"
   )
   ```

3. **Error Handling**:
   ```python
   try:
       await self.process()
   except Exception as e:
       self.state.record_error(e)
   ```

## Key Implementation Notes

1. **Context vs State**:
   - Context: Application-wide services and configuration
   - State: Task-specific data and progress

2. **Context Inheritance**:
   - Components inherit from `ContextDependent`
   - Automatic fallback to global context
   - Temporary context switching available

3. **State Persistence**:
   - Workflow state persists across tasks
   - Error state captures full context
   - Metadata for custom state tracking
