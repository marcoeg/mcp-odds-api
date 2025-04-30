import logging
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import os
import httpx
from typing import Dict, Any, List, Optional
from urllib.parse import urlencode

env_path = os.path.join(os.getcwd(), ".env")
load_dotenv(env_path)
from mcp_odds_api.mcp_config import config

BASE_URL = "https://api.the-odds-api.com/v4"

ODDS_API_KEY = config.api_key
if not ODDS_API_KEY:
    raise ValueError("ODDS_API_KEY environment variable not set")

odds_api_regions = config.regions
odds_api_key = config.api_key
odds_api_sport = "soccer_italy_serie_a"

MCP_SERVER_NAME = "mcp-odds-api"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(MCP_SERVER_NAME)

deps = ["starlette", "python-dotenv", "uvicorn", "httpx"]
mcp = FastMCP(MCP_SERVER_NAME, dependencies=deps)

logger = logging.getLogger(__name__)

async def set_api_sport(league: str):
    """Set the current league.
    
    Args:
        league: the league code in the dictionary.

    Returns:
        True if the league is in the dictionary and the odds_api_sport has been changed
        Fals if the league is not in the dictionary
    """
    global odds_api_sport
    from utils import get_league_info

    if get_league_info(league):
        odds_api_sport = league
        return True
    else:
        return False 

async def make_request(endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any] | None:
    """Make a request to the API with proper error handling.
    
    Args:
        endpoint: API endpoint without leading slash
        params: Optional query parameters
        
    Returns:
        JSON response or None if the request failed
    """
    # Ensure params is a dictionary
    if params is None:
        params = {}
    
    # Always add the API key
    params["apiKey"] = odds_api_key
    
    # Build the full URL
    url = f"{BASE_URL}/{endpoint}"
    
    # Add query parameters
    if params:
        query_string = urlencode(params, doseq=False)
        url = f"{url}?{query_string}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            
            # Log remaining requests
            remaining = response.headers.get("x-requests-remaining")
            if remaining:
                logger.info(f"Remaining API requests: {remaining}")
            
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
            return None
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
    

async def get_sports(include_all: bool = False, filter_group: str = None) -> List[Dict[str, Any]] | None:
    """Get all available sports.
    
    Args:
        include_all: If True, include out-of-season sports
        filter_group: Optional group name to filter results (e.g., 'Soccer')
        
    Returns:
        List of sports or None if the request failed
    """
    params = {}
    if include_all:
        params["all"] = "true"
    
    response = await make_request("sports", params)
    
    # Filter by group if specified
    if response and filter_group:
        return [sport for sport in response if sport.get('group') == filter_group]
    
    return response

async def get_participants() -> List[Dict[str, Any]] | None:
    """Get participants for the selected sport.
    
    Args:
        
    Returns:
        List of participants or None if the request failed
    """
    endpoint = f"sports/{odds_api_sport}/participants"
    response = await make_request(endpoint)
    return response

@mcp.tool(name="get_odds", description="Get odds for all forthcoming events (matches) for selected betting markets.")
async def get_odds(
    markets: Optional[List[str]] = None,
) -> List[Dict[str, Any]] | None:
    """Get odds for a sport.
    
    Args:
        markets: List of markets (h2h, spreads, totals, outrights)
        bookmakers: Optional list of bookmakers to include
        
    Returns:
        List of odds data or None if the request failed
    """
    params = {
        "regions": ",".join(odds_api_regions),
        "dateFormat": "iso",
        "oddsFormat": "decimal",
        "includeLinks": True,
        "includeSids": True
    }
    
    if markets:
        params["markets"] = ",".join(markets)

        
    #if bookmakers:
    #    params["bookmakers"] = ",".join(bookmakers)
        
    #if commence_time_from:
    #    params["commenceTimeFrom"] = commence_time_from
    #    
    #if commence_time_to:
    #    params["commenceTimeTo"] = commence_time_to

    endpoint = f"sports/{odds_api_sport}/odds"
    response = await make_request(endpoint, params)
    return response

@mcp.tool(name="get_event_odds", description="Get odds for a specific event (match) for selected betting markets.")
async def get_event_odds(
    event_id: str,
    markets: Optional[List[str]] = None,
) -> Dict[str, Any] | None:
    """Get odds for a specific event.
    
    Args:
        event_id: Event ID
        markets: List of markets (can include any available market)
        bookmakers: Optional list of bookmakers to include
        
    Returns:
        Event odds data or None if the request failed
    """
    params = {
        "regions": ",".join(odds_api_regions),
        "dateFormat":  "iso",
        "oddsFormat": "decimal",
        "includeLinks": True,
        "includeSids": True
    }
    
    if markets:
        params["markets"] = ",".join(markets)
        
    #if bookmakers:
    #    params["bookmakers"] = ",".join(bookmakers)
        
    #if commence_time_from:
    #    params["commenceTimeFrom"] = commence_time_from
    #    
    #if commence_time_to:
    #    params["commenceTimeTo"] = commence_time_to
    
    endpoint = f"sports/{odds_api_sport}/events/{event_id}/odds"
    response = await make_request(endpoint, params)
    return response

@mcp.tool(name="get_events", description="Get in-play and forthcoming events (matches). If a team is specified, returns only the events for the specified team.")
async def get_events(
    team: Optional[str] = None,
) -> List[Dict[str, Any]] | None:
    """Get in-play and pre-match events for the selected league. If a team is specified, returns only the events for the specified team. 
    
    Args:
        team: Optional. If present list only the events for the team.

    Returns:
        List of in-play and pre-match events or None if the request failed.
    
    Example response:
        [
            {
                'id': 'd10cd88092145c5cc79d6f45dbf65599', 
                'sport_key': 'soccer_italy_serie_a', 
                'sport_title': 'Serie A - Italy', 
                'commence_time': '2025-05-12T18:45:00Z', 
                'home_team': 'Atalanta BC', 
                'away_team': 'AS Roma'
            },
            {
                'id': 'd10cd88092145c5cc79d6f45dbf65599', 
                'sport_key': 'soccer_italy_serie_a', 
                'sport_title': 'Serie A - Italy', 
                'commence_time': '2025-05-12T18:45:00Z', 
                'home_team': 'Atalanta BC', 
                'away_team': 'AS Roma'
            }
        ]
    """
    params = {
        "dateFormat": "iso"
    }
    endpoint = f"sports/{odds_api_sport}/events"
    events = await make_request(endpoint, params)

    if team:
        if events:
            # Filter for matches involving Roma (either home or away)
            response = [event for event in events if team in event.get("home_team", "") or team in event.get("away_team", "")]
    else:
        response = events        

    return response

# Example usage
async def main():
    from .utils import format_odds
    import json
   
    # Get soccer sports
    #soccer_sports = await get_sports(include_all=True, filter_group="Soccer")
    #if soccer_sports:
    #    print(f"Found {len(soccer_sports)} soccer sports")
    #    for sport in soccer_sports:
    #        print(f"{sport['key']} - {sport['title']} - {sport['description']}")

    # Get participants for a sport
    #participants = await get_participants()
    #if participants:
    #    print(f"Found {len(participants)} participants")
    #    print(json.dumps(participants, indent=2))
        
    # Get odds for the selected sport. for instance Italian Serie A soccer games
    #odds = await get_odds(
    #    markets=["h2h"]
    #)
    #if odds:
    #    print(f"Found odds for {len(odds)} events")
    #    print(format_odds(odds))
    
    # Get events for Italian Serie A and filter for Roma matches
    events = await get_events(
        team="Roma"
    )
    if events:
        # Filter for matches involving Roma (either home or away)
        #roma_events = [event for event in events if "Roma" in event.get("home_team", "") or "Roma" in event.get("away_team", "")]
        roma_events = events
        print(f"\nFound {len(roma_events)} events with Roma:")

        for event in roma_events:
            print(f"{event['away_team']} @ {event['home_team']} - {event['commence_time']}")
        
        # Get odds for each Roma event
        if roma_events:
            print("\nOdds for Roma matches:")
            for event in roma_events:
                event_id = event['id']
                event_odds = await get_event_odds(
                    event_id=event_id,
                    markets=["h2h", "spreads", "totals","alternate_spreads","alternate_totals","btts",
                             "draw_no_bet","h2h_3_way","team_totals","alternate_team_totals","h2h_h1","h2h_h2",
                            "h2h_3_way_h1","h2h_3_way_h2","spreads_h1","spreads_h2","alternate_spreads_h1","totals_h1","totals_h2",
                            "alternate_totals_h1","alternate_team_totals_h1","alternate_team_totals_h2",
                             "player_goal_scorer_anytime","player_first_goal_scorer","player_last_goal_scorer","player_to_receive_card",
                             "player_to_receive_red_card","player_shots_on_target","player_shots","player_assists"]
                )               

                if event_odds:
                    print(f"\n{'='*60}")
                    # Check the structure of event_odds and adapt as needed
                    if isinstance(event_odds, dict) and 'bookmakers' in event_odds:
                        # Create a single-item list to match the format_odds expectation
                        formatted_odds = format_odds([event_odds], default_state="nj")
                        print(formatted_odds)
                    else:
                        # If it's already a list format compatible with format_odds
                        formatted_odds = format_odds(event_odds, default_state="nj")
                        print(formatted_odds)
                else:
                    print(f"No odds available for {event['away_team']} @ {event['home_team']}")
                    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())