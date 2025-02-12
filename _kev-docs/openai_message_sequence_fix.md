# OpenAI Message Sequence Fix

## Issue Description
We encountered errors from the OpenAI API regarding invalid message sequences:
```
Error: Invalid parameter: messages with role 'tool' must be a response to a preceeding message with 'tool_calls'
```

The error occurred because the message sequence wasn't properly maintaining the relationship between tool_calls and their corresponding tool responses.

## Root Cause
1. Messages with role 'tool' were being added without proper validation of their corresponding 'tool_calls'
2. The sequence of messages wasn't maintaining the required OpenAI API format:
   - Assistant messages with tool_calls must precede their tool responses
   - Each tool message must reference a valid tool_call_id
   - Content cannot be null in messages

## Implementation Fix
We added message sequence validation in `augmented_llm_openai.py` that:

1. **Validates Message Sequence**:
```python
def _validate_message_sequence(self, messages: List[Message]) -> None:
    tool_call_ids = set()
    for i, msg in enumerate(messages):
        if msg.has_tool_calls:
            # Track tool_call_ids from assistant messages
            for tool_call in msg.tool_calls:
                tool_call_ids.add(tool_call.id)
        elif msg.tool_call_id:
            # Validate tool messages reference existing tool_calls
            if msg.tool_call_id not in tool_call_ids:
                raise ValueError(f"Message at index {i} references non-existent tool_call_id")
```

2. **Improved Message Sanitization**:
- Only removes tool_calls after confirming their tool messages exist
- Maintains proper message sequence
- Ensures content is never null

3. **Enhanced Error Logging**:
- Shows detailed message structure before API calls
- Provides specific error messages for sequence validation failures
- Helps track message flow for debugging

## Benefits
1. **Reliability**: Messages now properly maintain their sequence and relationships
2. **Debugging**: Better error messages make issues easier to identify
3. **Compliance**: Ensures compliance with OpenAI API requirements
4. **Maintainability**: Clear validation logic makes future updates easier

## Testing
The fix was verified by running the workflow swarm example:
```python
& .\.venv\Scripts\python.exe .\examples\workflow_swarm\main.py
```

The test completed successfully with no message sequence errors.

## Best Practices
1. Always validate message sequences before API calls
2. Maintain proper relationships between tool_calls and tool responses
3. Use detailed logging during development to track message flow
4. Handle edge cases in message sequence validation

## Future Improvements
Consider:
1. Adding more detailed logging for message flow tracking
2. Implementing additional validation checks
3. Adding unit tests for message sequence validation
4. Enhancing error messages with more context
