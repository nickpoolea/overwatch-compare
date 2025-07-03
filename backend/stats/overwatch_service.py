import requests
import json
import statistics
from enum import Enum

from .enhanced_analysis import EnhancedOverwatchService, STAT_DEFINITIONS
from .utils import format_battletag, format_stat_value, calculate_difference

# Enum with all heroes
class Hero(Enum):
    ANA = "ana"
    ASHE = "ashe"
    BAPTISTE = "baptiste"
    BASTION = "bastion"
    BRIGITTE = "brigitte"
    CASSIDY = "cassidy"
    DVA = "dva"
    ECHO = "echo"
    FREJA = "freja"
    GENJI = "genji"
    HANZO = "hanzo"
    ILLARI = "illari"
    JUNKER_QUEEN = "junker-queen"
    JUNKRAT = "junkrat"
    JUNO = "juno"
    KIRIKO = "kiriko"
    LIFEWEAVER = "lifeweaver"
    LUCIO = "lucio"
    MAUGA = "mauga"
    MEI = "mei"
    MERCY = "mercy"
    MOIRA = "moira"
    ORISA = "orisa"
    PHARAH = "pharah"
    RAMATTRA = "ramattra"
    REAPER = "reaper"
    REINHARDT = "reinhardt"
    ROADHOG = "roadhog"
    SIGMA = "sigma"
    SOJOURN = "sojourn"
    SOLDIER_76 = "soldier-76"
    SOMBRA = "sombra"
    SYMMETRA = "symmetra"
    TORBJORN = "torbjorn"
    TRACER = "tracer"
    VENTURE = "venture"
    WIDOWMAKER = "widowmaker"
    WINSTON = "winston"
    WRECKING_BALL = "wrecking-ball"
    ZARYA = "zarya"
    ZENYATTA = "zenyatta"

def get_player_stats(battletag, gamemode='quickplay', platform='pc'):
    """Fetch and return the player stats from OverFast API with gamemode and platform parameters."""
    formatted_tag = format_battletag(battletag)
    url = f"https://overfast-api.tekrop.fr/players/{formatted_tag}/stats?gamemode={gamemode}&platform={platform}"
    try:
        response = requests.get(url, timeout=30)
        if response.status_code != 200:
            return None
        return response.json()
    except requests.RequestException:
        return None

def compare_hero_stats(stats1, stats2, hero_name, player1_tag, player2_tag):
    """Compare stats for a single hero between two players and return structured data."""
    if not stats1 or hero_name not in stats1:
        return {"error": f"No stats data available for {player1_tag} on hero: {hero_name}"}
    
    if not stats2 or hero_name not in stats2:
        return {"error": f"No stats data available for {player2_tag} on hero: {hero_name}"}
    
    hero_categories1 = stats1[hero_name]
    hero_categories2 = stats2[hero_name]
    
    # Create dictionaries organized by category
    player1_by_category = {}
    player2_by_category = {}
    
    # Parse player 1 stats by category
    for category in hero_categories1:
        if isinstance(category, dict) and 'category' in category and 'stats' in category:
            category_name = category.get('label', category.get('category', 'Unknown'))
            player1_by_category[category_name] = {}
            for stat in category['stats']:
                key = stat.get('key', '')
                player1_by_category[category_name][key] = stat
    
    # Parse player 2 stats by category
    for category in hero_categories2:
        if isinstance(category, dict) and 'category' in category and 'stats' in category:
            category_name = category.get('label', category.get('category', 'Unknown'))
            player2_by_category[category_name] = {}
            for stat in category['stats']:
                key = stat.get('key', '')
                player2_by_category[category_name][key] = stat
    
    # Get all unique categories
    all_categories = set(player1_by_category.keys()) | set(player2_by_category.keys())
    
    result = {
        "hero": hero_name,
        "player1": player1_tag,
        "player2": player2_tag,
        "categories": []
    }
    
    # Process each category
    for category_name in sorted(all_categories):
        player1_category = player1_by_category.get(category_name, {})
        player2_category = player2_by_category.get(category_name, {})
        all_stat_keys = set(player1_category.keys()) | set(player2_category.keys())
        
        category_data = {
            "name": category_name,
            "stats": [],
            "summary": {}
        }
        
        numeric_stats_p1 = []
        numeric_stats_p2 = []
        
        # Process each stat in the category
        for stat_key in sorted(all_stat_keys):
            player1_stat = player1_category.get(stat_key, {})
            player2_stat = player2_category.get(stat_key, {})
            
            label = player1_stat.get('label', player2_stat.get('label', stat_key))
            value1 = player1_stat.get('value', None)
            value2 = player2_stat.get('value', None)
            
            # Format values
            formatted_value1 = format_stat_value(stat_key, value1)
            formatted_value2 = format_stat_value(stat_key, value2)
            
            # Calculate difference
            difference = calculate_difference(stat_key, value1, value2)
            
            category_data["stats"].append({
                "key": stat_key,
                "label": label,
                "player1_value": value1,
                "player2_value": value2,
                "player1_formatted": formatted_value1,
                "player2_formatted": formatted_value2,
                "difference": difference
            })
            
            # Collect numeric values for summary
            if isinstance(value1, (int, float)) and isinstance(value2, (int, float)):
                numeric_stats_p1.append(value1)
                numeric_stats_p2.append(value2)
        
        # Calculate category summary
        if numeric_stats_p1 and numeric_stats_p2:
            wins_p1 = sum(1 for v1, v2 in zip(numeric_stats_p1, numeric_stats_p2) if v1 > v2)
            wins_p2 = sum(1 for v1, v2 in zip(numeric_stats_p1, numeric_stats_p2) if v2 > v1)
            ties = len(numeric_stats_p1) - wins_p1 - wins_p2
            
            avg1 = sum(numeric_stats_p1) / len(numeric_stats_p1)
            avg2 = sum(numeric_stats_p2) / len(numeric_stats_p2)
            
            category_data["summary"] = {
                "player1_wins": wins_p1,
                "player2_wins": wins_p2,
                "ties": ties,
                "player1_average": round(avg1, 2),
                "player2_average": round(avg2, 2),
                "average_difference": round(avg1 - avg2, 2)
            }
        
        result["categories"].append(category_data)
    
    return result



def enhanced_compare_hero_stats(stats1, stats2, hero_name, player1_tag, player2_tag):
    """Enhanced comparison with statistical analysis and weighted scoring."""
    if not stats1 or hero_name not in stats1:
        return {"error": f"No stats data available for {player1_tag} on hero: {hero_name}"}
    
    if not stats2 or hero_name not in stats2:
        return {"error": f"No stats data available for {player2_tag} on hero: {hero_name}"}
    
    # Use existing comparison logic
    basic_comparison = compare_hero_stats(stats1, stats2, hero_name, player1_tag, player2_tag)
    
    if "error" in basic_comparison:
        return basic_comparison
    
    # Extract flat stat dictionaries for enhanced analysis
    player1_flat_stats = {}
    player2_flat_stats = {}
    
    hero_categories1 = stats1[hero_name]
    hero_categories2 = stats2[hero_name]
    
    # Flatten stats for analysis
    for category in hero_categories1:
        if isinstance(category, dict) and 'stats' in category:
            for stat in category['stats']:
                key = stat.get('key', '')
                value = stat.get('value')
                if isinstance(value, (int, float)):
                    player1_flat_stats[key] = value
    
    for category in hero_categories2:
        if isinstance(category, dict) and 'stats' in category:
            for stat in category['stats']:
                key = stat.get('key', '')
                value = stat.get('value')
                if isinstance(value, (int, float)):
                    player2_flat_stats[key] = value
    
    # Enhanced analysis
    enhanced_service = EnhancedOverwatchService()
    
    # Calculate weighted performance scores
    p1_score = enhanced_service.calculate_weighted_score(player1_flat_stats, STAT_DEFINITIONS)
    p2_score = enhanced_service.calculate_weighted_score(player2_flat_stats, STAT_DEFINITIONS)
    
    # Generate performance analysis
    performance_analysis = enhanced_service.analyze_performance_pattern(
        player1_flat_stats, player2_flat_stats
    )
    
    # Generate insights
    insights = enhanced_service.generate_insights(basic_comparison)
    
    # Determine hero role for role-specific analysis
    hero_roles = {
        'ana': 'support', 'baptiste': 'support', 'brigitte': 'support', 'kiriko': 'support',
        'lucio': 'support', 'mercy': 'support', 'moira': 'support', 'zenyatta': 'support',
        'illari': 'support', 'lifeweaver': 'support', 'juno': 'support',
        
        'dva': 'tank', 'junker-queen': 'tank', 'orisa': 'tank', 'ramattra': 'tank',
        'reinhardt': 'tank', 'roadhog': 'tank', 'sigma': 'tank', 'winston': 'tank',
        'wrecking-ball': 'tank', 'zarya': 'tank', 'mauga': 'tank',
        
        'ashe': 'damage', 'bastion': 'damage', 'cassidy': 'damage', 'echo': 'damage',
        'genji': 'damage', 'hanzo': 'damage', 'junkrat': 'damage', 'mei': 'damage',
        'pharah': 'damage', 'reaper': 'damage', 'sojourn': 'damage', 'soldier-76': 'damage',
        'sombra': 'damage', 'symmetra': 'damage', 'torbjorn': 'damage', 'tracer': 'damage',
        'venture': 'damage', 'widowmaker': 'damage', 'freja': 'damage'
    }
    
    hero_role = hero_roles.get(hero_name, 'damage')
    p1_role_effectiveness = enhanced_service.calculate_role_effectiveness(player1_flat_stats, hero_role)
    p2_role_effectiveness = enhanced_service.calculate_role_effectiveness(player2_flat_stats, hero_role)
    
    # Add enhanced data to the basic comparison
    basic_comparison['enhanced_analysis'] = {
        'performance_scores': {
            'player1_weighted_score': round(p1_score, 3),
            'player2_weighted_score': round(p2_score, 3),
            'score_difference': round(p1_score - p2_score, 3)
        },
        'role_effectiveness': {
            'player1_effectiveness': round(p1_role_effectiveness, 3),
            'player2_effectiveness': round(p2_role_effectiveness, 3),
            'hero_role': hero_role
        },
        'performance_analysis': performance_analysis,
        'insights': insights,
        'statistical_summary': {
            'total_stats_compared': len(set(player1_flat_stats.keys()) | set(player2_flat_stats.keys())),
            'common_stats': len(set(player1_flat_stats.keys()) & set(player2_flat_stats.keys())),
            'confidence_level': 'high' if len(player1_flat_stats) > 10 else 'medium' if len(player1_flat_stats) > 5 else 'low'
        }
    }
    
    return basic_comparison
