import os
import logging

from google.adk.agents.llm_agent import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseServerParams

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ray Serve config
RAY_SERVICE_NAME = "llama-31-8b-serve-svc"
RAY_SERVE_PORT = 8000
api_base_url = f"http://{RAY_SERVICE_NAME}:{RAY_SERVE_PORT}/v1"
logger.debug(f"Connecting to RayServe vLLM at: {api_base_url}")

# --- MCP Toolset Configuration for Cocktail Server ---
async def get_cocktail_toolset():
    """Creates and returns the MCPToolset for the cocktail server."""
    mcp_cocktail_host = os.getenv("MCP_COCKTAIL_SERVICE_HOST", "mcp-cocktail-service")
    mcp_cocktail_port = int(os.getenv("MCP_COCKTAIL_SERVICE_PORT", 8080))
    mcp_cocktail_sse_path = os.getenv("MCP_COCKTAIL_SSE_PATH", "/sse")
    full_sse_url = f"http://{mcp_cocktail_host}:{mcp_cocktail_port}{mcp_cocktail_sse_path}"

    logger.info(f"Configuring MCPToolset with SseServerParams URL: {full_sse_url}")
    connection_params = SseServerParams(url=full_sse_url)

    logger.info(f"Attempting to get tools using MCPToolset.from_server with URL: {full_sse_url}")
    tools_list, exit_stack = await MCPToolset.from_server(
        connection_params=connection_params
    )
    logger.info(f"MCPToolset.from_server returned {len(tools_list)} tools.")
    return tools_list, exit_stack # exit_stack needs to be managed for cleanup

# --- Root Agent Creation Function ---
async def create_agent():
    """Creates and returns the root agent with MCP tools."""
    try:
        tools_list, exit_stack = await get_cocktail_toolset()
        logger.info(f"Successfully obtained {len(tools_list)} tools for root_agent.")
        
        agent = LlmAgent(
            name="cocktail_chat_agent",
            model=LiteLlm(
                model="hosted_vllm/meta-llama/Llama-3.1-8B-Instruct",
                api_base=api_base_url
            ),
            instruction="""You are a specialist AI assistant for cocktails.
                
Use your available tools to answer questions about cocktails.
Format your answers clearly using Markdown.""",
            tools=tools_list,
        )
        
        logger.info(f"ADK Agent '{agent.name}' created with {len(tools_list)} tools.")
        return agent, exit_stack
    except Exception as e:
        logger.error(f"Failed to create agent with MCP toolset: {e}", exc_info=True)
        # Fallback to a basic agent without tools
        agent = LlmAgent(
            name="cocktail_chat_agent",
            model=LiteLlm(
                model="hosted_vllm/meta-llama/Llama-3.1-8B-Instruct",
                api_base=api_base_url
            ),
            instruction="""You are a specialist AI assistant for cocktails.
                
Use your knowledge to answer questions about cocktails. 
Note: Tools are currently unavailable.
Format your answers clearly using Markdown.""",
            tools=[],
        )
        logger.info("Created fallback agent without tools due to error.")
        return agent, None

# This async function creates the agent when needed
# Using the pattern shown in the documentation
root_agent = create_agent()