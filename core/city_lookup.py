"""
City Coordinate Lookup Module
Provides accurate longitude for true solar time calculation
"""
import json
import os

_city_data = None


def _load_city_data():
    """Load city coordinates data (lazy load)."""
    global _city_data
    if _city_data is None:
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "city_coords.json")
        try:
            with open(data_path, "r", encoding="utf-8") as f:
                _city_data = json.load(f)
        except FileNotFoundError:
            _city_data = {}
    return _city_data


def lookup_city_longitude(country_code, city_name=None):
    """
    Look up longitude for a city.
    
    Args:
        country_code: ISO country code (CN, JP, VN, LK, MM)
        city_name: Optional city name. If None or not found, returns capital longitude.
    
    Returns:
        dict with 'longitude' and 'matched_city' keys
    """
    data = _load_city_data()
    country_config = data.get(country_code, {})
    
    if not country_config:
        return {
            "longitude": 116.4,  # Default to Beijing
            "matched_city": "默认",
            "is_capital": True
        }
    
    capital_lon = country_config.get("capital_longitude", 116.4)
    
    if not city_name:
        return {
            "longitude": capital_lon,
            "matched_city": "首都",
            "is_capital": True
        }
    
    cities = country_config.get("cities", {})
    city_name = city_name.strip()
    
    # Exact match
    if city_name in cities:
        return {
            "longitude": cities[city_name],
            "matched_city": city_name,
            "is_capital": False
        }
    
    # Case-insensitive match
    city_lower = city_name.lower()
    for name, lon in cities.items():
        if name.lower() == city_lower:
            return {
                "longitude": lon,
                "matched_city": name,
                "is_capital": False
            }
    
    # Partial match (contains)
    for name, lon in cities.items():
        if city_lower in name.lower() or name.lower() in city_lower:
            return {
                "longitude": lon,
                "matched_city": name,
                "is_capital": False
            }
    
    # Not found, fallback to capital
    return {
        "longitude": capital_lon,
        "matched_city": "首都 (未找到城市)",
        "is_capital": True
    }


def get_country_config(country_code):
    """Get full country configuration."""
    data = _load_city_data()
    return data.get(country_code, {})


def search_cities(country_code, query, limit=5):
    """
    Search cities by partial name.
    
    Returns list of (name, longitude) tuples.
    """
    data = _load_city_data()
    country_config = data.get(country_code, {})
    cities = country_config.get("cities", {})
    
    if not query:
        return list(cities.items())[:limit]
    
    query_lower = query.lower()
    results = []
    
    for name, lon in cities.items():
        if query_lower in name.lower():
            results.append((name, lon))
            if len(results) >= limit:
                break
    
    return results
