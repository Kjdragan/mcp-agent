# Understanding Context in MCP Agent

## 1. Core Data Models

### ConversationContext
```python
class ConversationContext(BaseModel):
    messages: List[Message] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Message
```python
class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)
```

## 2. LLM Context Usage

The LLM uses context to:
- Maintain conversation history
- Track user preferences
- Store session-specific data
- Handle multi-turn interactions

Example Flow:
```python
# Initialize context
context = ConversationContext()

# Add system message
context.messages.append(Message(
    role="system",
    content="You are a helpful assistant"
))

# Add user message
context.messages.append(Message(
    role="user",
    content="Explain MCP architecture"
))
```

## 3. Accessing and Modifying Context

### Accessing Context
```python
# Get current context
current_context = agent.get_context()

# Read messages
for message in current_context.messages:
    print(f"[{message.role}] {message.content}")
```

### Modifying Context
```python
# Add metadata
current_context.metadata["user_preferences"] = {
    "language": "English",
    "detail_level": "technical"
}

# Update message
current_context.messages[-1].metadata["source"] = "web_interface"
```

## Best Practices
- Always append to context rather than overwrite
- Use metadata for extensible context storage
- Regularly prune context to maintain performance
