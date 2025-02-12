from mcp_agent.workflows.swarm.swarm import Swarm
from mcp_agent.workflows.llm.augmented_llm import RequestParams
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM
from mcp_agent.logging.logger import get_logger
import re
from openai.types.chat import ChatCompletionMessage, ChatCompletionMessageParam, ChatCompletionAssistantMessageParam

logger = get_logger(__name__)


class OpenAISwarm(Swarm, OpenAIAugmentedLLM):
    """
    MCP version of the OpenAI Swarm class (https://github.com/openai/swarm.), using OpenAI's ChatCompletion as the LLM.
    """

    @staticmethod
    def _sanitize_name(name: str) -> str:
        """Sanitize name to match OpenAI's required pattern ^[a-zA-Z0-9_-]+$"""
        if not name:
            return "agent"
        # Replace any character that's not alphanumeric, underscore, or hyphen with underscore
        sanitized = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
        return sanitized

    @classmethod
    def convert_message_to_message_param(
        cls, message: ChatCompletionMessage, **kwargs
    ) -> ChatCompletionAssistantMessageParam:
        """Convert a response object to an input parameter object with sanitized name."""
        if 'name' in kwargs:
            kwargs['name'] = cls._sanitize_name(kwargs['name'])
        return ChatCompletionAssistantMessageParam(
            role="assistant",
            content=message.content,
            audio=message.audio,
            refusal=message.refusal,
            **kwargs,
        )

    async def generate(self, message, request_params: RequestParams | None = None):
        params = self.get_request_params(
            request_params,
            default=RequestParams(
                model="gpt-4o",
                maxTokens=8192,
                parallel_tool_calls=False,
            ),
        )
        iterations = 0
        response = None
        agent_name = self._sanitize_name(str(self.aggregator.name)) if self.aggregator else None

        while iterations < params.max_iterations and self.should_continue():
            response = await super().generate(
                message=message
                if iterations == 0
                else "Please resolve my original request. If it has already been resolved then end turn",
                request_params=params.model_copy(
                    update={"max_iterations": 1}  # TODO: saqadri - validate
                ),
            )
            logger.debug(f"Agent: {agent_name}, response:", data=response)
            agent_name = self._sanitize_name(str(self.aggregator.name)) if self.aggregator else None
            iterations += 1

        # Return final response back
        return response
