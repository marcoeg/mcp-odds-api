# mcp-odds-api
A mimimalist Model Context Protocol MCP server to interact with the OddsAPI.

## Features
- Uses environmental variables to limit the queries to some regions and a single sport.

>It supports both SSE and STDIO transports. 

## Tools
The server implements the following tools to interact with the OddsAPI:

- `get_events`:
   - Get in-play and forthcoming events (matches). 

- `get_odds`:
   - Get odds for all forthcoming events (matches) for selected betting markets.
- `get_event_odds`:
   - Get odds for a specific event (match) for selected betting markets.

## Configuration

1. Create _or edit the Claude Desktop configuration file located at:
   - On macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

2. Add the following:

```json
{
  "mcpServers": {
    "mcp-bauplan": {
      "command": "/path/to/uvx",
      "args": ["mcp-odds-api"],
      "env": {
        "ODDS_API_KEY": "<your-api-odds-key>",
        "ODDS_API_REGIONS": "<region1>", "<region2>",
        "ODDS_API_SPORT": "<selected-sport-key>",
      }
    }
  }
}
```
3. Replace `/path/to/uvx` with the absolute path to the `uvx` executable. Find the path with `which uvx` command in a terminal. This ensures that the correct version of `uvx` is used when starting the server.

4. Restart Claude Desktop to apply the changes.

## Run the stand-alone SSE server
Create a .env file from .env.example and then execute the following command:
```bash
$ uvx --env-file /path/to/.env mcp-odds-api --transport sse --port 9090
```
>Note the use of `nvx` and not `uvx` will fetch `mcp-bauplan` from the default registry https://pypi.org.

## Development

### Setup

1. **Prerequisites**:
   - Python 3.10 or higher.
   - A OddsAPI key ([request here](https://the-odds-api.com/account/)).
   - `uv` package manager ([installation](https://docs.astral.sh/uv/)).

2. **Clone the Repository**:
```bash
git clone https://github.com/marcoeg/mcp-odds-api
cd mcp-nvd
```

3. **Set Environment Variables**:
   - Create a `.env` file in the project root:
     ```
    ODDS_API_KEY="<your-api-odds-key>"
    ODDS_API_REGIONS="<region1>", "<region2>"
    ODDS_API_SPORT="<selected-sport-key>"
     ```

4. **Install Dependencies**:
```bash
uv sync
uv pip install -e .
```

### Start the server with SSE transport
```bash
$ uv run mcp-odds-api --transport sse --port 9090
python-dotenv could not parse statement starting at line 2
2025-04-30 19:35:34 - dotenv.main - WARNING - python-dotenv could not parse statement starting at line 2
INFO:     Started server process [68314]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:9090 (Press CTRL+C to quit)
```

### Run the Inspector:
```bash
$ CLIENT_PORT=8077 TARGET_PORT=9090 \
npx @modelcontextprotocol/inspector run

Starting MCP inspector...
⚙️ Proxy server listening on port 6277
🔍 MCP Inspector is up and running at http://127.0.0.1:8077 🚀
```

Then open the browser to the URL indicated by the MCP Inspector. Select SSE Transport Type.
