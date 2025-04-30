import logging
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import os
from typing import Dict, Any
import httpx

env_path = os.path.join(os.getcwd(), ".env")
load_dotenv(env_path)
from mcp_odds_api.mcp_config import config

ODDS_API_KEY = config.api_key
if not ODDS_API_KEY:
    raise ValueError("ODDS_API_KEY environment variable not set")

odds_api_regions = config.regions

MCP_SERVER_NAME = "mcp-odds-api"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(MCP_SERVER_NAME)

deps = ["starlette", "python-dotenv", "uvicorn", "httpx"]
mcp = FastMCP(MCP_SERVER_NAME, dependencies=deps)


import httpx
import logging
from typing import Dict, Any, List, Optional
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

class OddsAPIClient:
    """Client for The Odds API with async HTTP requests."""
    
    BASE_URL = "https://api.the-odds-api.com/v4"
    
    def __init__(self, api_key: str):
        """Initialize the client with your API key.
        
        Args:
            api_key: Your API key from The Odds API
        """
        self.api_key = api_key
    
    async def make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any] | None:
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
        params["apiKey"] = self.api_key
        
        # Build the full URL
        url = f"{self.BASE_URL}/{endpoint}"
        
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
        

    async def get_sports(self, include_all: bool = False, filter_group: str = None) -> List[Dict[str, Any]] | None:
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
        
        response = await self.make_request("sports", params)
        
        # Filter by group if specified
        if response and filter_group:
            return [sport for sport in response if sport.get('group') == filter_group]
        
        return response

    async def get_odds(
        self,
        sport: str,
        markets: Optional[List[str]] = None,
        date_format: str = "iso",
        odds_format: str = "decimal",
        event_ids: Optional[List[str]] = None,
        bookmakers: Optional[List[str]] = None,
        commence_time_from: Optional[str] = None,
        commence_time_to: Optional[str] = None,
        include_links: bool = False,
        include_sids: bool = False
    ) -> List[Dict[str, Any]] | None:
        """Get odds for a sport.
        
        Args:
            sport: Sport key from the /sports endpoint
            markets: List of markets (h2h, spreads, totals, outrights)
            date_format: Format for dates (iso, unix)
            odds_format: Format for odds (decimal, american)
            event_ids: Optional list of event IDs to filter by
            bookmakers: Optional list of bookmakers to include
            commence_time_from: Filter events starting on/after (ISO format)
            commence_time_to: Filter events starting on/before (ISO format)
            include_links: Include bookmaker links if available
            include_sids: Include source IDs if available
            
        Returns:
            List of odds data or None if the request failed
        """
        params = {
            "regions": ",".join(odds_api_regions),
            "dateFormat": date_format,
            "oddsFormat": odds_format
        }
        
        if markets:
            params["markets"] = ",".join(markets)
        
        if event_ids:
            params["eventIds"] = ",".join(event_ids)
            
        if bookmakers:
            params["bookmakers"] = ",".join(bookmakers)
            
        if commence_time_from:
            params["commenceTimeFrom"] = commence_time_from
            
        if commence_time_to:
            params["commenceTimeTo"] = commence_time_to
            
        if include_links:
            params["includeLinks"] = "true"
            
        if include_sids:
            params["includeSids"] = "true"
        
        endpoint = f"sports/{sport}/odds"
        response = await self.make_request(endpoint, params)
        return response
    
    async def get_event_odds_(
        self,
        sport: str,
        event_id: str,
        markets: Optional[List[str]] = None,
        date_format: str = "iso",
        odds_format: str = "decimal"
    ) -> Dict[str, Any] | None:
        """Get odds for a specific event.
        
        Args:
            sport: Sport key from the /sports endpoint
            event_id: Event ID
            regions: List of regions (us, us2, uk, au, eu)
            markets: List of markets (can include any available market)
            date_format: Format for dates (iso, unix)
            odds_format: Format for odds (decimal, american)
            
        Returns:
            Event odds data or None if the request failed
        """
        params = {
            "regions": ",".join(odds_api_regions),
            "dateFormat": date_format,
            "oddsFormat": odds_format
        }
        
        if markets:
            params["markets"] = ",".join(markets)
        
        endpoint = f"sports/{sport}/events/{event_id}/odds"
        response = await self.make_request(endpoint, params)
        return response

    async def get_event_odds(
        self,
        sport: str,
        event_id: str,
        markets: Optional[List[str]] = None,
        date_format: str = "iso",
        odds_format: str = "decimal",
        bookmakers: Optional[List[str]] = None,
        commence_time_from: Optional[str] = None,
        commence_time_to: Optional[str] = None,
        include_links: bool = False,
        include_sids: bool = False
    ) -> Dict[str, Any] | None:
        """Get odds for a specific event.
        
        Args:
            sport: Sport key from the /sports endpoint
            event_id: Event ID
            markets: List of markets (can include any available market)
            date_format: Format for dates (iso, unix)
            odds_format: Format for odds (decimal, american)
            bookmakers: Optional list of bookmakers to include
            commence_time_from: Filter events starting on/after (ISO format)
            commence_time_to: Filter events starting on/before (ISO format)
            include_links: Include bookmaker links if available
            include_sids: Include source IDs if available
            
        Returns:
            Event odds data or None if the request failed
        """
        params = {
            "regions": ",".join(odds_api_regions),
            "dateFormat": date_format,
            "oddsFormat": odds_format
        }
        
        if markets:
            params["markets"] = ",".join(markets)
            
        if bookmakers:
            params["bookmakers"] = ",".join(bookmakers)
            
        if commence_time_from:
            params["commenceTimeFrom"] = commence_time_from
            
        if commence_time_to:
            params["commenceTimeTo"] = commence_time_to
            
        if include_links:
            params["includeLinks"] = "true"
            
        if include_sids:
            params["includeSids"] = "true"
        
        endpoint = f"sports/{sport}/events/{event_id}/odds"
        response = await self.make_request(endpoint, params)
        return response
    
    async def get_participants(self, sport: str) -> List[Dict[str, Any]] | None:
        """Get participants for a sport.
        
        Args:
            sport: Sport key from the /sports endpoint
            
        Returns:
            List of participants or None if the request failed
        """
        endpoint = f"sports/{sport}/participants"
        response = await self.make_request(endpoint)
        return response

    async def get_events(
        self,
        sport: str,
        date_format: str = "iso",
        event_ids: Optional[List[str]] = None,
        commence_time_from: Optional[str] = None,
        commence_time_to: Optional[str] = None
    ) -> List[Dict[str, Any]] | None:
        """Get events for a sport.
        
        Args:
            sport: Sport key from the /sports endpoint
            date_format: Format for dates (iso, unix)
            event_ids: Optional list of event IDs to filter by
            commence_time_from: Filter events starting on/after (ISO format)
            commence_time_to: Filter events starting on/before (ISO format)
            
        Returns:
            List of events or None if the request failed
        """
        params = {
            "dateFormat": date_format
        }
        
        if event_ids:
            params["eventIds"] = ",".join(event_ids)
            
        if commence_time_from:
            params["commenceTimeFrom"] = commence_time_from
            
        if commence_time_to:
            params["commenceTimeTo"] = commence_time_to
        
        endpoint = f"sports/{sport}/events"
        response = await self.make_request(endpoint, params)
        return response
    
# Example usage
async def main():
    from .utils import format_odds
    import json

    # Initialize the client
    client = OddsAPIClient(api_key=ODDS_API_KEY)
    
   
    # Get soccer sports
    soccer_sports = await client.get_sports(include_all=True, filter_group="Soccer")
    if soccer_sports:
        print(f"Found {len(soccer_sports)} soccer sports")
        for sport in soccer_sports:
            print(f"{sport['key']} - {sport['title']} - {sport['description']}")


    """
    # Get participants for a sport
    participants = await client.get_participants(sport="soccer_italy_serie_b")
    if participants:
        print(f"Found {len(participants)} participants")
        print(json.dumps(participants, indent=2))
    # Get odds for Italian Serie A soccer games
    odds = await client.get_odds(
        sport="soccer_italy_serie_a",
        markets=["h2h"],
        include_links=True
    )
    if odds:
        print(f"Found odds for {len(odds)} events")
        print(format_odds(odds))
    """
    
    # Get events for Italian Serie A and filter for Roma matches
    events = await client.get_events(
        sport="soccer_italy_serie_a",
        date_format="iso"
    )
    if events:
        # Filter for matches involving Roma (either home or away)
        roma_events = [event for event in events if "Roma" in event.get("home_team", "") or "Roma" in event.get("away_team", "")]
        #roma_events = [roma_events[0]]  # only to limit to one event for testing
        print(f"\nFound {len(roma_events)} events with Roma:")

        for event in roma_events:
            print(f"{event['away_team']} @ {event['home_team']} - {event['commence_time']}")
        
        # Get odds for each Roma event
        if roma_events:
            print("\nOdds for Roma matches:")
            for event in roma_events:
                event_id = event['id']
                event_odds = await client.get_event_odds(
                    include_links=True,
                    include_sids=True,
                    sport="soccer_italy_serie_a",
                    event_id=event_id,
                    markets=["h2h", "spreads", "totals","alternate_spreads","alternate_totals","btts",
                             "draw_no_bet","h2h_3_way","team_totals","alternate_team_totals","h2h_h1","h2h_h2",
                            "h2h_3_way_h1","h2h_3_way_h2","spreads_h1","spreads_h2","alternate_spreads_h1","totals_h1","totals_h2",
                            "alternate_totals_h1","alternate_team_totals_h1","alternate_team_totals_h2",
                             "player_goal_scorer_anytime","player_first_goal_scorer","player_last_goal_scorer","player_to_receive_card",
                             "player_to_receive_red_card","player_shots_on_target","player_shots","player_assists"],
                    date_format="iso",
                    odds_format="decimal"
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