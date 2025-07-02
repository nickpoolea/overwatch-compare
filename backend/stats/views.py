from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .overwatch_service import get_player_stats, compare_hero_stats, enhanced_compare_hero_stats, Hero
import json

@api_view(['GET'])
def get_heroes(request):
    """Return list of all available heroes."""
    heroes = [{"value": hero.value, "label": hero.value.replace('-', ' ').title()} for hero in Hero]
    return Response(heroes)

@api_view(['POST'])
def compare_players(request):
    """Compare two players' stats for a specific hero."""
    try:
        data = request.data
        player1_tag = data.get('player1')
        player2_tag = data.get('player2')
        hero_name = data.get('hero')
        gamemode = data.get('gamemode', 'quickplay')
        platform = data.get('platform', 'pc')
        
        if not all([player1_tag, player2_tag, hero_name]):
            return Response(
                {"error": "Missing required fields: player1, player2, hero"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate hero
        valid_heroes = [hero.value for hero in Hero]
        if hero_name not in valid_heroes:
            return Response(
                {"error": f"Invalid hero: {hero_name}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Fetch stats for both players
        player1_stats = get_player_stats(player1_tag, gamemode, platform)
        player2_stats = get_player_stats(player2_tag, gamemode, platform)
        
        if not player1_stats:
            return Response(
                {"error": f"Unable to fetch stats for player: {player1_tag}"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not player2_stats:
            return Response(
                {"error": f"Unable to fetch stats for player: {player2_tag}"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Compare stats with enhanced analysis
        comparison_result = enhanced_compare_hero_stats(
            player1_stats, player2_stats, hero_name, player1_tag, player2_tag
        )
        
        if "error" in comparison_result:
            return Response(comparison_result, status=status.HTTP_404_NOT_FOUND)
        
        return Response(comparison_result)
        
    except Exception as e:
        return Response(
            {"error": f"Internal server error: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def get_enhanced_summary(request):
    """Get only the enhanced analysis summary without detailed stat breakdown."""
    try:
        data = request.data
        player1_tag = data.get('player1')
        player2_tag = data.get('player2')
        hero_name = data.get('hero')
        gamemode = data.get('gamemode', 'quickplay')
        platform = data.get('platform', 'pc')
        
        if not all([player1_tag, player2_tag, hero_name]):
            return Response(
                {"error": "Missing required fields: player1, player2, hero"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate hero
        valid_heroes = [hero.value for hero in Hero]
        if hero_name not in valid_heroes:
            return Response(
                {"error": f"Invalid hero: {hero_name}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Fetch stats for both players
        player1_stats = get_player_stats(player1_tag, gamemode, platform)
        player2_stats = get_player_stats(player2_tag, gamemode, platform)
        
        if not player1_stats or not player2_stats:
            return Response(
                {"error": "Unable to fetch stats for one or both players"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get enhanced comparison
        comparison_result = enhanced_compare_hero_stats(
            player1_stats, player2_stats, hero_name, player1_tag, player2_tag
        )
        
        if "error" in comparison_result:
            return Response(comparison_result, status=status.HTTP_404_NOT_FOUND)
        
        # Return only the enhanced analysis part
        summary_only = {
            "hero": comparison_result["hero"],
            "player1": comparison_result["player1"],
            "player2": comparison_result["player2"],
            "enhanced_analysis": comparison_result.get("enhanced_analysis", {}),
            "quick_summary": {
                "total_categories": len(comparison_result.get("categories", [])),
                "category_winners": {
                    "player1": sum(1 for cat in comparison_result.get("categories", []) 
                                 if cat.get("summary", {}).get("player1_wins", 0) > cat.get("summary", {}).get("player2_wins", 0)),
                    "player2": sum(1 for cat in comparison_result.get("categories", []) 
                                 if cat.get("summary", {}).get("player2_wins", 0) > cat.get("summary", {}).get("player1_wins", 0))
                }
            }
        }
        
        return Response(summary_only)
        
    except Exception as e:
        return Response(
            {"error": f"Internal server error: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
