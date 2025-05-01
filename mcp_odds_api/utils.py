def format_odds(odds_data, default_state="nj"):
    """Format odds data for readability with all available links.
    
    Args:
        odds_data: Odds data from the API
        default_state: State code to use when replacing {state} in URLs (default: "nj")
    """
    if not odds_data:
        return "No odds data available"
    
    formatted_output = []
    
    for event in odds_data:
        event_info = f"\n=== MATCH: {event['away_team']} @ {event['home_team']} ===\n"
        event_info += f"Time: {event['commence_time']}\n"
        
        # Bookmakers info
        for bookmaker in event['bookmakers']:
            event_info += f"\n  {bookmaker['title']}:"
            
            # Add bookmaker link if available and fix {state} placeholder
            if 'link' in bookmaker and bookmaker['link']:
                fixed_link = bookmaker['link'].replace("{state}", default_state)
                event_info += f" [SITE: {fixed_link}]"
            event_info += "\n"
            
            # Markets info
            for market in bookmaker['markets']:
                event_info += f"    {market['key'].upper()}\n"
                
                for outcome in market['outcomes']:
                    point_info = f" ({outcome.get('point', '')})" if 'point' in outcome else ""
                    event_info += f"      {outcome['name']}: {outcome['price']}{point_info}"
                    
                    # Add outcome link if available and fix {state} placeholder
                    if 'link' in outcome and outcome['link']:
                        fixed_link = outcome['link'].replace("{state}", default_state)
                        event_info += f" [BET: {fixed_link}]"
                    event_info += "\n"
        
        formatted_output.append(event_info)
    
    return "\n".join(formatted_output)

def format_odds_(odds_data):
    """Format odds data for readability with all available links."""
    if not odds_data:
        return "No odds data available"
    
    formatted_output = []
    
    for event in odds_data:
        event_info = f"\n=== MATCH: {event['away_team']} @ {event['home_team']} ===\n"
        event_info += f"Time: {event['commence_time']}\n"
        
        # Bookmakers info
        for bookmaker in event['bookmakers']:
            event_info += f"\n  {bookmaker['title']}:"
            
            # Add bookmaker link if available
            if 'link' in bookmaker and bookmaker['link']:
                event_info += f" [SITE: {bookmaker['link']}]"
            event_info += "\n"
            
            # Markets info
            for market in bookmaker['markets']:
                event_info += f"    {market['key'].upper()}\n"
                
                for outcome in market['outcomes']:
                    point_info = f" ({outcome.get('point', '')})" if 'point' in outcome else ""
                    event_info += f"      {outcome['name']}: {outcome['price']}{point_info}"
                    
                    # Add outcome link if available
                    if 'link' in outcome and outcome['link']:
                        event_info += f" [BET: {outcome['link']}]"
                    event_info += "\n"
        
        formatted_output.append(event_info)
    
    return "\n".join(formatted_output)

soccer_leagues = [
    {
        "league": "soccer_africa_cup_of_nations",
        "description": "Africa Cup of Nations - Africa Cup of Nations"
    },
    {
        "league": "soccer_argentina_primera_division",
        "description": "Primera División - Argentina - Argentine Primera División"
    },
    {
        "league": "soccer_australia_aleague",
        "description": "A-League - Aussie Soccer"
    },
    {
        "league": "soccer_austria_bundesliga",
        "description": "Austrian Football Bundesliga - Austrian Soccer"
    },
    {
        "league": "soccer_belgium_first_div",
        "description": "Belgium First Div - Belgian First Division A"
    },
    {
        "league": "soccer_brazil_campeonato",
        "description": "Brazil Série A - Brasileirão Série A"
    },
    {
        "league": "soccer_brazil_serie_b",
        "description": "Brazil Série B - Campeonato Brasileiro Série B"
    },
    {
        "league": "soccer_chile_campeonato",
        "description": "Primera División - Chile - Campeonato Chileno"
    },
    {
        "league": "soccer_china_superleague",
        "description": "Super League - China - Chinese Soccer"
    },
    {
        "league": "soccer_conmebol_copa_america",
        "description": "Copa América - CONMEBOL Copa América"
    },
    {
        "league": "soccer_conmebol_copa_libertadores",
        "description": "Copa Libertadores - CONMEBOL Copa Libertadores"
    },
    {
        "league": "soccer_conmebol_copa_sudamericana",
        "description": "Copa Sudamericana - CONMEBOL Copa Sudamericana"
    },
    {
        "league": "soccer_denmark_superliga",
        "description": "Denmark Superliga - Danish Soccer"
    },
    {
        "league": "soccer_efl_champ",
        "description": "Championship - EFL Championship"
    },
    {
        "league": "soccer_england_efl_cup",
        "description": "EFL Cup - League Cup"
    },
    {
        "league": "soccer_england_league1",
        "description": "League 1 - EFL League 1"
    },
    {
        "league": "soccer_england_league2",
        "description": "League 2 - EFL League 2"
    },
    {
        "league": "soccer_epl",
        "description": "EPL - English Premier League"
    },
    {
        "league": "soccer_fa_cup",
        "description": "FA Cup - Football Association Challenge Cup"
    },
    {
        "league": "soccer_fifa_world_cup",
        "description": "FIFA World Cup - FIFA World Cup 2022"
    },
    {
        "league": "soccer_fifa_world_cup_qualifiers_europe",
        "description": "FIFA World Cup Qualifiers - Europe - FIFA World Cup Qualifiers - UEFA"
    },
    {
        "league": "soccer_fifa_world_cup_qualifiers_south_america",
        "description": "FIFA World Cup Qualifiers - South America - FIFA World Cup Qualifiers - CONMEBOL"
    },
    {
        "league": "soccer_fifa_world_cup_winner",
        "description": "FIFA World Cup Winner - FIFA World Cup Winner 2026"
    },
    {
        "league": "soccer_fifa_world_cup_womens",
        "description": "FIFA Women's World Cup - FIFA Women's World Cup"
    },
    {
        "league": "soccer_finland_veikkausliiga",
        "description": "Veikkausliiga - Finland - Finnish Soccer"
    },
    {
        "league": "soccer_france_ligue_one",
        "description": "Ligue 1 - France - French Soccer"
    },
    {
        "league": "soccer_france_ligue_two",
        "description": "Ligue 2 - France - French Soccer"
    },
    {
        "league": "soccer_germany_bundesliga",
        "description": "Bundesliga - Germany - German Soccer"
    },
    {
        "league": "soccer_germany_bundesliga2",
        "description": "Bundesliga 2 - Germany - German Soccer"
    },
    {
        "league": "soccer_germany_liga3",
        "description": "3. Liga - Germany - German Soccer"
    },
    {
        "league": "soccer_greece_super_league",
        "description": "Super League - Greece - Greek Soccer"
    },
    {
        "league": "soccer_italy_serie_a",
        "description": "Serie A - Italy - Italian Soccer"
    },
    {
        "league": "soccer_italy_serie_b",
        "description": "Serie B - Italy - Italian Soccer"
    },
    {
        "league": "soccer_japan_j_league",
        "description": "J League - Japan Soccer League"
    },
    {
        "league": "soccer_korea_kleague1",
        "description": "K League 1 - Korean Soccer"
    },
    {
        "league": "soccer_league_of_ireland",
        "description": "League of Ireland - Airtricity League Premier Division"
    },
    {
        "league": "soccer_mexico_ligamx",
        "description": "Liga MX - Mexican Soccer"
    },
    {
        "league": "soccer_netherlands_eredivisie",
        "description": "Dutch Eredivisie - Dutch Soccer"
    },
    {
        "league": "soccer_norway_eliteserien",
        "description": "Eliteserien - Norway - Norwegian Soccer"
    },
    {
        "league": "soccer_poland_ekstraklasa",
        "description": "Ekstraklasa - Poland - Polish Soccer"
    },
    {
        "league": "soccer_portugal_primeira_liga",
        "description": "Primeira Liga - Portugal - Portugese Soccer"
    },
    {
        "league": "soccer_spain_la_liga",
        "description": "La Liga - Spain - Spanish Soccer"
    },
    {
        "league": "soccer_spain_segunda_division",
        "description": "La Liga 2 - Spain - Spanish Soccer"
    },
    {
        "league": "soccer_spl",
        "description": "Premiership - Scotland - Scottish Premiership"
    },
    {
        "league": "soccer_sweden_allsvenskan",
        "description": "Allsvenskan - Sweden - Swedish Soccer"
    },
    {
        "league": "soccer_sweden_superettan",
        "description": "Superettan - Sweden - Swedish Soccer"
    },
    {
        "league": "soccer_switzerland_superleague",
        "description": "Swiss Superleague - Swiss Soccer"
    },
    {
        "league": "soccer_turkey_super_league",
        "description": "Turkey Super League - Turkish Soccer"
    },
    {
        "league": "soccer_uefa_champs_league",
        "description": "UEFA Champions League - European Champions League"
    },
    {
        "league": "soccer_uefa_champs_league_qualification",
        "description": "UEFA Champions League Qualification - European Champions League Qualification"
    },
    {
        "league": "soccer_uefa_champs_league_women",
        "description": "UEFA Champions League Women - European Champions League Women"
    },
    {
        "league": "soccer_uefa_euro_qualification",
        "description": "UEFA Euro Qualification - European Championship Qualification"
    },
    {
        "league": "soccer_uefa_europa_conference_league",
        "description": "UEFA Europa Conference League - UEFA Europa Conference League"
    },
    {
        "league": "soccer_uefa_europa_league",
        "description": "UEFA Europa League - European Europa League"
    },
    {
        "league": "soccer_uefa_european_championship",
        "description": "UEFA Euro 2024 - UEFA European Championship"
    },
    {
        "league": "soccer_uefa_nations_league",
        "description": "UEFA Nations League - UEFA Nations League"
    },
    {
        "league": "soccer_usa_mls",
        "description": "MLS - Major League Soccer"
    }
]

def get_league_info(league_id: str, soccer_leagues: list) -> dict:
    """
    Retrieves league information from the soccer_leagues list based on the league ID.
    
    Args:
        league_id (str): The ID of the league to search for (e.g., 'soccer_usa_mls')
        soccer_leagues (list): List of dictionaries containing league information
        
    Returns:
        dict: The dictionary containing the league information or None if not found
    """
    for league in soccer_leagues:
        if league["league"] == league_id:
            return league
    return None

# Example usage:
# league_info = get_league_info("soccer_usa_mls", soccer_leagues)
# if league_info:
#     print(f"Found league: {league_info['description']}")
# else:
#     print("League not found")