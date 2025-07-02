"""
Test script for the enhanced analysis functionality
"""

import sys
import os
import django
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'overwatch_api.settings')
django.setup()

from stats.overwatch_service import enhanced_compare_hero_stats, get_player_stats

def test_enhanced_analysis():
    """Test the enhanced analysis with sample data."""
    print("🧪 Testing Enhanced Analysis...")
    
    # Test with some sample BattleTags
    player1 = "BaconChee#1321"
    player2 = "TestPlayer#1234"  # This might not exist, but let's see
    hero = "mercy"
    
    print(f"Fetching stats for {player1}...")
    stats1 = get_player_stats(player1)
    
    if stats1:
        print("✅ Player 1 stats fetched successfully")
        print(f"Available heroes: {list(stats1.keys())[:5]}...")  # Show first 5 heroes
        
        if hero in stats1:
            print(f"✅ {hero} stats found for {player1}")
            
            # For testing, let's compare against the same player (will show ties)
            print(f"\n🔄 Testing enhanced comparison (self vs self for demonstration)...")
            result = enhanced_compare_hero_stats(stats1, stats1, hero, player1, f"{player1}_copy")
            
            if "enhanced_analysis" in result:
                print("✅ Enhanced analysis generated successfully!")
                print("\n📊 Enhanced Analysis Results:")
                print(f"Performance Scores: {result['enhanced_analysis']['performance_scores']}")
                print(f"Role Effectiveness: {result['enhanced_analysis']['role_effectiveness']}")
                print(f"Statistical Summary: {result['enhanced_analysis']['statistical_summary']}")
                print(f"Insights: {result['enhanced_analysis']['insights']['overall_verdict']}")
            else:
                print("❌ Enhanced analysis not found in result")
        else:
            print(f"❌ Hero '{hero}' not found in player stats")
    else:
        print("❌ Failed to fetch player stats")

if __name__ == "__main__":
    test_enhanced_analysis()
