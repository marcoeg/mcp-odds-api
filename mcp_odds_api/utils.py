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