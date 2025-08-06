from agents import Agent, Runner
from agents.mcp import create_static_tool_filter, MCPServerStdio
import asyncio

from agents import Agent

# Initialize MCP Playwright server
playwright_server = MCPServerStdio(
    params={
        "command": "npx",
        "args": ["@playwright/mcp", "--save-trace", "--output-dir", "./reports"],
    },
    tool_filter=create_static_tool_filter(
        allowed_tool_names=[
            "browser_navigate",
            "browser_click",
            "browser_type",
            "browser_press_key",
            "browser_hover",
            "browser_handle_dialog",
            "browser_file_upload",
            "browser_console_messages",
            "browser_network_requests",
            "browser_evaluate",
            "browser_drag",
            "browser_close",
            "browser_install",
            "browser_resize",
            "browser_wait_for_selector",
            "browser_wait_for_event",
            "browser_navigate_back",
            "browser_navigate_forward"
        ]
    )
)

async def main():
    await playwright_server.connect()

    agent = Agent(
        name="Browser automation agent",
        instructions="You are an automation agent using Playwright MCP tools. Execute all steps in the prompt and generate a final report and close the browser.",
        mcp_servers=[playwright_server],
        model="gpt-4.1",

    )

    prompt = """
        1. Navigate to https://todomvc.com/examples/react/dist/
        2. Wait for the page to load and the input field for new todos to appear.
        3. Add the following item 'Learn Playwright', hit enter and verify it is added.
        4. Add the following item 'Learn MCP', hit enter and verify it is added.
        5. Delete the second item ("Learn MCP") by hovering and clicking the delete button next to it.
        6. Mark last item ("Learn Playwright") as completed by clicking the checkbox next to it.
        7. Report success if all items are present.
    """

    result = await Runner.run(agent, prompt)
    print(result.final_output)

asyncio.run(main())
