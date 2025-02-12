from mcp import ListToolsResult
import streamlit as st
import asyncio
import os
import sys
import traceback
from pathlib import Path
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
import datetime
from streamlit.logger import get_logger
import nest_asyncio

from mcp_agent.app import MCPApp
from mcp_agent.config import Settings, get_settings
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm import RequestParams
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM

# Apply nest_asyncio to handle async operations in Streamlit
nest_asyncio.apply()

@st.cache_resource
def get_app_instance():
    """Get or create a cached MCPApp instance"""
    if not hasattr(st.session_state, 'app'):
        env_path = Path(__file__).resolve().parents[2] / '.env'
        load_dotenv(env_path)
        config_path = Path(__file__).parent / 'mcp_agent.config.yaml'
        settings = get_settings(config_path)
        st.session_state.app = MCPApp(name="mcp_basic_agent", settings=settings)
        asyncio.run(st.session_state.app.initialize())
    return st.session_state.app

@st.cache_resource
def get_agent_instance():
    """Get or create a cached Agent instance"""
    if not hasattr(st.session_state, 'agent'):
        app = get_app_instance()
        finder_agent = Agent(
            name="finder",
            instruction="""You are an agent with access to the filesystem.
            Your job is to identify the closest match to a user's request,
            make the appropriate tool calls, and return the URI and CONTENTS
            of the closest match.""",
            server_names=["filesystem"],
        )
        asyncio.run(finder_agent.initialize())
        llm = asyncio.run(finder_agent.attach_llm(OpenAIAugmentedLLM))
        st.session_state.agent = finder_agent
        st.session_state.llm = llm
    return st.session_state.agent, st.session_state.llm

@st.cache_resource
def setup_logging():
    """Configure logging with Streamlit's cache to prevent duplicate handlers"""
    log_dir = Path(__file__).parent / '_logs'
    log_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    mcp_log_file = log_dir / f'mcp_agent_{timestamp}.log'
    streamlit_log_file = log_dir / f'streamlit_{timestamp}.log'
    
    # Configure MCP logger
    mcp_logger = logging.getLogger('mcp_agent')
    mcp_logger.setLevel(logging.DEBUG)
    
    # Clear any existing handlers to prevent duplicates
    if mcp_logger.hasHandlers():
        mcp_logger.handlers.clear()
    
    # Configure Streamlit logger
    streamlit_logger = get_logger(__name__)
    streamlit_logger.setLevel(logging.DEBUG)
    
    # Clear any existing handlers to prevent duplicates
    if streamlit_logger.hasHandlers():
        streamlit_logger.handlers.clear()
    
    # Create handlers
    mcp_file_handler = RotatingFileHandler(
        mcp_log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    streamlit_file_handler = RotatingFileHandler(
        streamlit_log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    
    # Create formatters and add it to handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    mcp_file_handler.setFormatter(formatter)
    streamlit_file_handler.setFormatter(formatter)
    
    # Add handlers to loggers
    mcp_logger.addHandler(mcp_file_handler)
    streamlit_logger.addHandler(streamlit_file_handler)
    
    return mcp_logger, streamlit_logger

def format_list_tools_result(list_tools_result: ListToolsResult):
    res = ""
    for tool in list_tools_result.tools:
        res += f"- **{tool.name}**: {tool.description}\n\n"
    return res

def main():
    """Main Streamlit application"""
    try:
        # Set up logging first
        mcp_logger, streamlit_logger = setup_logging()
        
        mcp_logger.info("Starting MCP Agent application")
        streamlit_logger.info("Starting Streamlit application")
        
        # Get or create the cached instances
        finder_agent, llm = get_agent_instance()
        
        mcp_logger.info("Listing tools...")
        tools = asyncio.run(finder_agent.list_tools())
        tools_str = format_list_tools_result(tools)
        mcp_logger.info("Tools listed successfully")

        streamlit_logger.info("Starting Streamlit UI setup...")
        st.title("💬 Basic Agent Chatbot")
        st.caption("🚀 A Streamlit chatbot powered by mcp-agent")

        with st.expander("View Tools"):
            st.markdown(tools_str)

        if "messages" not in st.session_state:
            streamlit_logger.info("Initializing session state")
            st.session_state["messages"] = [
                {"role": "assistant", "content": "How can I help you?"}
            ]

        for msg in st.session_state["messages"]:
            streamlit_logger.debug(f"Displaying message: {msg['role']}")
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input("Type your message here..."):
            streamlit_logger.info(f"Received user prompt: {prompt}")
            st.session_state["messages"].append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)

            with st.chat_message("assistant"):
                response = ""
                try:
                    request_params = RequestParams(
                        messages=[{"role": "user", "content": prompt}]
                    )
                    response = asyncio.run(llm.complete(request_params))
                    st.session_state["messages"].append(
                        {"role": "assistant", "content": response}
                    )
                    st.write(response)
                except Exception as e:
                    error_msg = f"Error processing request: {str(e)}"
                    mcp_logger.error(error_msg)
                    mcp_logger.error(traceback.format_exc())
                    st.error(error_msg)
                    
    except Exception as e:
        error_msg = f"Application error: {str(e)}"
        if 'mcp_logger' in locals():
            mcp_logger.error(error_msg)
            mcp_logger.error(traceback.format_exc())
        st.error(error_msg)

if __name__ == "__main__":
    mcp_logger, streamlit_logger = setup_logging()
    mcp_logger.info("Starting program...")
    main()