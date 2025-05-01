# mcp-odds-api
A mimimalist Model Context Protocol MCP server to interact with the OddsAPI.

## Features
- Uses environmental variables to limit the queries to some regions and a single sport.

>It supports both SSE and STDIO transports. 

## Tools
The server implements the following tools to interact with Bauplan data tables:
- `list_tables`:
   - Lists all the tables in the configured namespace
- `get_schema`:
   - Get the schema of a data tables
- `run_query`:
   - Run a SELECT query on the specified table 

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
      "args": ["mcp-bauplan"],
      "env": {
        "BAUPLAN_API_KEY": "your-api-key",
        "BAUPLAN_BRANCH": "your-branch",
        "BAUPLAN_NAMESPACE": "your-namespace",
        // Optional
        "BAUPLAN_TIMEOUT": "query-timeout-secs" // default 30 seconds
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
$ uvx --env-file /path/to/.env mcp-bauplan --transport sse --port 9090
```
>Note the use of `nvx` and not `uvx` will fetch `mcp-bauplan` from the default registry https://pypi.org.

## Development

### Setup

1. **Prerequisites**:
   - Python 3.10 or higher.
   - A Bauplan API key ([request here](https://www.bauplanlabs.com/#join)).
   - `uv` package manager ([installation](https://docs.astral.sh/uv/)).

2. **Clone the Repository**:
```bash
git clone https://github.com/marcoeg/mcp-bauplan
cd mcp-nvd
```

3. **Set Environment Variables**:
   - Create a `.env` file in the project root:
     ```
     BAUPLAN_API_KEY=your-api-key
     BAUPLAN_BRANCH=your-branch
     BAUPLAN_NAMESPACE=your-namespace
     ```

4. **Install Dependencies**:
```bash
uv sync
uv pip install -e .
```

### Run with the MCP Inspector
```bash
cd /path/to/the/repo
source .env

CLIENT_PORT=8077 SERVER_PORT=8078 npx @modelcontextprotocol/inspector \
     uv run mcp-bauplan
 ```
>Note: omit `CLIENT_PORT=8077 SERVER_PORT=8078` if the standard ports are not conflicting.

Then open the browser to the URL indicated by the MCP Inspector, typically `http://localhost:8077?proxyPort=8078`

> Switch freely between `stdio` and `sse` transport types in the inspector. To use `sse` you need to run the server as explained below.

### Testing with the SSE transport 

#### Run the Server:
```bash
cd /path/to/the/repo
source .env

uv run mcp-bauplan --transport sse --port 9090
```
- Runs with SSE transport on port `9090` by default.

Then open the browser to the URL indicated by the MCP Inspector. Select SSE Transport Type.

### Start the server with SSE transport
```
$ uv run mcp-odds-api --transport sse --port 9090
python-dotenv could not parse statement starting at line 2
2025-04-30 19:35:34 - dotenv.main - WARNING - python-dotenv could not parse statement starting at line 2
INFO:     Started server process [68314]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:9090 (Press CTRL+C to quit)
```

### Run the Inspector:
```
$ CLIENT_PORT=8077 TARGET_PORT=9090 \
npx @modelcontextprotocol/inspector run \
  --messages-path /messages \
  --cors

Starting MCP inspector...
⚙️ Proxy server listening on port 6277
🔍 MCP Inspector is up and running at http://127.0.0.1:8077 🚀
```