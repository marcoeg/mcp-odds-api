"""Environment configuration for the MCP odds-api server.

This module handles all environment variable configuration with sensible defaults
and type conversion.
"""

from dataclasses import dataclass
import os

@dataclass
class OddsAPIConfig:
    """Configuration for odss-api connection settings.

    This class handles all environment variable configuration related to
    the odds-api connection. 

    Required environment variables:
        "ODDS_API_KEY": The user odds-api api key
    """

    def __init__(self):
        """Initialize the configuration from environment variables."""
        self._validate_required_vars()

    @property
    def api_key(self) -> str:
        """Get the odds-api api key"""
        return os.environ["ODDS_API_KEY"]

    @property
    def regions(self) -> int:
        """Get the array of regions .

        Default: "us".
        """
        return os.environ.get("ODDS_API_REGIONS", "us").split(",")

    def _validate_required_vars(self) -> None:
        """Validate that all required environment variables are set.

        Raises:
            ValueError: If any required environment variable is missing.
        """
        missing_vars = []
        for var in ["ODDS_API_KEY"]:
            if var not in os.environ:
                missing_vars.append(var)

        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )

# Global instance for easy access
config = OddsAPIConfig()
