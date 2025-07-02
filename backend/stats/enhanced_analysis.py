"""
Enhanced Overwatch Stats Summarization Service

This module provides more sophisticated data analysis and summarization
for Overwatch player comparisons with statistical insights and weighted metrics.
"""

import requests
import json
import statistics
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Union, Tuple

# Enhanced stat categorization with weights and types
@dataclass
class StatDefinition:
    key: str
    category: str
    weight: float  # Importance weight (0-1)
    stat_type: str  # 'higher_better', 'lower_better', 'neutral'
    format_type: str  # 'number', 'percentage', 'time', 'ratio'

# Stat definitions with weights and importance
STAT_DEFINITIONS = {
    # Combat Stats (High Weight)
    'eliminations': StatDefinition('eliminations', 'combat', 0.9, 'higher_better', 'number'),
    'deaths': StatDefinition('deaths', 'combat', 0.8, 'lower_better', 'number'),
    'damage_dealt': StatDefinition('damage_dealt', 'combat', 0.85, 'higher_better', 'number'),
    'healing_done': StatDefinition('healing_done', 'support', 0.9, 'higher_better', 'number'),
    'damage_blocked': StatDefinition('damage_blocked', 'tank', 0.8, 'higher_better', 'number'),
    
    # Accuracy Stats (Medium-High Weight)
    'weapon_accuracy': StatDefinition('weapon_accuracy', 'accuracy', 0.7, 'higher_better', 'percentage'),
    'critical_hit_accuracy': StatDefinition('critical_hit_accuracy', 'accuracy', 0.7, 'higher_better', 'percentage'),
    
    # Objective Stats (High Weight)
    'objective_kills': StatDefinition('objective_kills', 'objective', 0.8, 'higher_better', 'number'),
    'objective_time': StatDefinition('objective_time', 'objective', 0.7, 'higher_better', 'time'),
    
    # General Stats (Medium Weight)
    'games_won': StatDefinition('games_won', 'general', 0.6, 'higher_better', 'number'),
    'time_played': StatDefinition('time_played', 'general', 0.3, 'neutral', 'time'),
}

class EnhancedOverwatchService:
    
    @staticmethod
    def calculate_weighted_score(stats: Dict, stat_definitions: Dict[str, StatDefinition]) -> float:
        """Calculate a weighted performance score based on stat importance."""
        total_score = 0
        total_weight = 0
        
        for stat_key, value in stats.items():
            if stat_key in stat_definitions and isinstance(value, (int, float)):
                stat_def = stat_definitions[stat_key]
                
                # Normalize value to 0-1 scale (simplified)
                normalized_value = min(value / 1000, 1.0)  # Adjust scaling as needed
                
                # Apply direction (higher_better vs lower_better)
                if stat_def.stat_type == 'lower_better':
                    score_component = (1 - normalized_value) * stat_def.weight
                elif stat_def.stat_type == 'higher_better':
                    score_component = normalized_value * stat_def.weight
                else:  # neutral
                    score_component = 0.5 * stat_def.weight
                
                total_score += score_component
                total_weight += stat_def.weight
        
        return total_score / total_weight if total_weight > 0 else 0

    @staticmethod
    def calculate_stat_percentiles(all_stats: List[float]) -> Dict:
        """Calculate statistical percentiles for a set of values."""
        if not all_stats:
            return {}
        
        return {
            'median': statistics.median(all_stats),
            'p25': statistics.quantiles(all_stats, n=4)[0] if len(all_stats) >= 4 else min(all_stats),
            'p75': statistics.quantiles(all_stats, n=4)[2] if len(all_stats) >= 4 else max(all_stats),
            'std_dev': statistics.stdev(all_stats) if len(all_stats) > 1 else 0,
            'range': max(all_stats) - min(all_stats)
        }

    @staticmethod
    def analyze_performance_pattern(stats1: Dict, stats2: Dict) -> Dict:
        """Analyze performance patterns and provide insights."""
        analysis = {
            'dominant_categories': [],
            'close_categories': [],
            'improvement_areas': [],
            'overall_assessment': ''
        }
        
        # Calculate category-wise dominance
        category_scores = {}
        for category in ['combat', 'accuracy', 'objective', 'support', 'tank']:
            p1_score = 0
            p2_score = 0
            stat_count = 0
            
            for stat_key, value1 in stats1.items():
                if stat_key in STAT_DEFINITIONS:
                    stat_def = STAT_DEFINITIONS[stat_key]
                    if stat_def.category == category and isinstance(value1, (int, float)):
                        value2 = stats2.get(stat_key, 0)
                        if isinstance(value2, (int, float)):
                            if stat_def.stat_type == 'higher_better':
                                if value1 > value2:
                                    p1_score += stat_def.weight
                                elif value2 > value1:
                                    p2_score += stat_def.weight
                            elif stat_def.stat_type == 'lower_better':
                                if value1 < value2:
                                    p1_score += stat_def.weight
                                elif value2 < value1:
                                    p2_score += stat_def.weight
                            stat_count += 1
            
            if stat_count > 0:
                category_scores[category] = {
                    'player1_score': p1_score,
                    'player2_score': p2_score,
                    'stat_count': stat_count
                }
        
        # Determine dominant and close categories
        for category, scores in category_scores.items():
            p1_score = scores['player1_score']
            p2_score = scores['player2_score']
            total_possible = scores['stat_count']
            
            if abs(p1_score - p2_score) / total_possible > 0.3:  # 30% difference threshold
                winner = 'player1' if p1_score > p2_score else 'player2'
                analysis['dominant_categories'].append({
                    'category': category,
                    'winner': winner,
                    'margin': abs(p1_score - p2_score) / total_possible
                })
            else:
                analysis['close_categories'].append({
                    'category': category,
                    'margin': abs(p1_score - p2_score) / total_possible
                })
        
        return analysis

    @staticmethod
    def generate_insights(comparison_data: Dict) -> Dict:
        """Generate actionable insights from the comparison."""
        insights = {
            'key_strengths': {'player1': [], 'player2': []},
            'improvement_opportunities': {'player1': [], 'player2': []},
            'overall_verdict': '',
            'recommendation': ''
        }
        
        # Analyze each category for insights
        for category in comparison_data.get('categories', []):
            category_name = category['name']
            summary = category.get('summary', {})
            
            p1_wins = summary.get('player1_wins', 0)
            p2_wins = summary.get('player2_wins', 0)
            
            # Determine strengths
            if p1_wins > p2_wins * 1.5:  # 50% more wins
                insights['key_strengths']['player1'].append(category_name)
            elif p2_wins > p1_wins * 1.5:
                insights['key_strengths']['player2'].append(category_name)
            
            # Identify improvement areas (where one player significantly lags)
            if p1_wins < p2_wins * 0.5:
                insights['improvement_opportunities']['player1'].append(category_name)
            elif p2_wins < p1_wins * 0.5:
                insights['improvement_opportunities']['player2'].append(category_name)
        
        # Generate overall verdict
        p1_categories_won = len(insights['key_strengths']['player1'])
        p2_categories_won = len(insights['key_strengths']['player2'])
        
        if p1_categories_won > p2_categories_won:
            insights['overall_verdict'] = f"{comparison_data['player1']} shows superior performance"
        elif p2_categories_won > p1_categories_won:
            insights['overall_verdict'] = f"{comparison_data['player2']} shows superior performance"
        else:
            insights['overall_verdict'] = "Both players show comparable performance"
        
        return insights

    @staticmethod
    def calculate_role_effectiveness(stats: Dict, hero_role: str) -> float:
        """Calculate effectiveness score based on hero role."""
        role_weights = {
            'tank': ['damage_blocked', 'damage_dealt', 'eliminations', 'objective_time'],
            'damage': ['eliminations', 'damage_dealt', 'weapon_accuracy', 'objective_kills'],
            'support': ['healing_done', 'eliminations', 'deaths', 'weapon_accuracy']
        }
        
        relevant_stats = role_weights.get(hero_role, [])
        if not relevant_stats:
            return 0
        
        effectiveness_score = 0
        stat_count = 0
        
        for stat_key in relevant_stats:
            if stat_key in stats and isinstance(stats[stat_key], (int, float)):
                # Simplified effectiveness calculation
                effectiveness_score += min(stats[stat_key] / 100, 1.0)  # Normalize
                stat_count += 1
        
        return effectiveness_score / stat_count if stat_count > 0 else 0
