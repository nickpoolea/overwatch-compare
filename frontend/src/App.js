import React, { useState, useEffect } from 'react';
import './App.css';

const API_BASE_URL = 'http://localhost:8000/api';

// Utility functions for number formatting
const formatNumber = (value) => {
  if (value === null || value === undefined || value === "N/A") {
    return "N/A";
  }
  
  // Handle time strings (already formatted)
  if (typeof value === 'string' && (value.includes('h') || value.includes('m') || value.includes(':'))) {
    return value;
  }
  
  // Convert to number if it's a string
  const numValue = typeof value === 'string' ? parseFloat(value) : value;
  
  if (isNaN(numValue)) {
    return value; // Return original if not a number
  }
  
  // Check if it's already a percentage string
  if (typeof value === 'string' && value.includes('%')) {
    return value;
  }
  
  // Format numbers with appropriate decimal places and comma separators
  if (Math.abs(numValue) >= 1000) {
    // Large numbers: use comma separators, no decimals for whole numbers
    if (numValue % 1 === 0) {
      return numValue.toLocaleString('en-US');
    } else {
      return numValue.toLocaleString('en-US', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
      });
    }
  } else if (numValue % 1 !== 0) {
    // Small numbers with decimals: limit to 2 decimal places
    return numValue.toLocaleString('en-US', {
      minimumFractionDigits: 0,
      maximumFractionDigits: 2
    });
  } else {
    // Whole numbers less than 1000: no formatting needed
    return numValue.toString();
  }
};

const formatPercentage = (value) => {
  if (value === null || value === undefined || value === "N/A") {
    return "N/A";
  }
  
  // If already formatted as percentage string
  if (typeof value === 'string' && value.includes('%')) {
    return value;
  }
  
  const numValue = typeof value === 'string' ? parseFloat(value) : value;
  
  if (isNaN(numValue)) {
    return value;
  }
  
  // If value is already a percentage (> 1), format as is
  if (numValue > 1) {
    return `${numValue.toFixed(2)}%`;
  } else {
    // Convert decimal to percentage
    return `${(numValue * 100).toFixed(2)}%`;
  }
};

const formatDifference = (value, statLabel) => {
  if (value === null || value === undefined || value === "N/A" || value === "Ties") {
    return value;
  }
  
  // Handle time format differences (already formatted)
  if (typeof value === 'string' && (value.includes('h') || value.includes('m'))) {
    return value;
  }
  
  // Handle percentage strings
  if (typeof value === 'string' && value.includes('%')) {
    return value;
  }
  
  const numValue = typeof value === 'string' ? parseFloat(value.replace('+', '')) : value;
  
  if (isNaN(numValue)) {
    return value;
  }
  
  const isNegative = numValue < 0;
  const absValue = Math.abs(numValue);
  const sign = isNegative ? '-' : '+';
  
  // Check if this should be a percentage based on stat label
  if (statLabel && (statLabel.toLowerCase().includes('accuracy') || statLabel.toLowerCase().includes('percentage'))) {
    return `${sign}${absValue.toFixed(2)}%`;
  }
  
  // Format differences with commas and appropriate decimal places
  if (absValue >= 1000) {
    if (absValue % 1 === 0) {
      return `${sign}${absValue.toLocaleString('en-US')}`;
    } else {
      return `${sign}${absValue.toLocaleString('en-US', { maximumFractionDigits: 2 })}`;
    }
  } else if (absValue % 1 !== 0) {
    return `${sign}${absValue.toFixed(2)}`;
  } else {
    return `${sign}${absValue}`;
  }
};

const formatScore = (value) => {
  if (value === null || value === undefined || isNaN(value)) {
    return "N/A";
  }
  
  return (value * 100).toFixed(1);
};

const isPercentageStat = (statKey, statLabel) => {
  const percentageKeys = ['accuracy', 'percentage', 'hit_percentage', 'critical_hit_accuracy', 'weapon_accuracy', 'scoped_accuracy'];
  const key = statKey ? statKey.toLowerCase() : '';
  const label = statLabel ? statLabel.toLowerCase() : '';
  
  return percentageKeys.some(keyword => key.includes(keyword) || label.includes(keyword));
};

function App() {
  const [heroes, setHeroes] = useState([]);
  const [formData, setFormData] = useState({
    player1: 'BaconChee#1321',
    player2: 'wompkins#1289',
    hero: '',
    gamemode: 'quickplay',
    platform: 'pc'
  });
  const [comparison, setComparison] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchHeroes();
  }, []);

  const fetchHeroes = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/heroes/`);
      const data = await response.json();
      setHeroes(data);
    } catch (err) {
      setError('Failed to fetch heroes');
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setComparison(null);

    try {
      const response = await fetch(`${API_BASE_URL}/compare/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to compare players');
      }

      setComparison(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const renderCategoryStats = (category) => {
    return (
      <div key={category.name} className="category-section">
        <h3 className="category-title">{category.name}</h3>
        <div className="stats-table">
          <div className="stats-header">
            <div className="stat-name">Stat</div>
            <div className="player-value">{comparison.player1}</div>
            <div className="player-value">{comparison.player2}</div>
            <div className="difference">Difference</div>
          </div>
          {category.stats.map((stat, index) => {
            // Determine if this is a percentage stat
            const isPercentage = isPercentageStat(stat.key, stat.label);
            
            // Format the values appropriately
            const player1Value = isPercentage 
              ? formatPercentage(stat.player1_value) 
              : formatNumber(stat.player1_value);
            
            const player2Value = isPercentage 
              ? formatPercentage(stat.player2_value) 
              : formatNumber(stat.player2_value);
            
            const differenceValue = formatDifference(stat.difference, stat.label);
            
            return (
              <div key={index} className="stats-row">
                <div className="stat-name">{stat.label}</div>
                <div className="player-value">{player1Value}</div>
                <div className="player-value">{player2Value}</div>
                <div className="difference">{differenceValue}</div>
              </div>
            );
          })}
          {category.summary && Object.keys(category.summary).length > 0 && (
            <div className="category-summary">
              <div className="summary-row">
                <div className="stat-name">Category Summary:</div>
                <div className="player-value">Wins: {category.summary.player1_wins}</div>
                <div className="player-value">Wins: {category.summary.player2_wins}</div>
                <div className="difference">Ties: {category.summary.ties}</div>
              </div>
              <div className="summary-row">
                <div className="stat-name">Average:</div>
                <div className="player-value">{formatNumber(category.summary.player1_average)}</div>
                <div className="player-value">{formatNumber(category.summary.player2_average)}</div>
                <div className="difference">{formatDifference(category.summary.average_difference)}</div>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Overwatch Player Comparison</h1>
      </header>

      <main className="main-content">
        <form onSubmit={handleSubmit} className="comparison-form">
          <div className="form-group">
            <label htmlFor="player1">Player 1 BattleTag:</label>
            <input
              type="text"
              id="player1"
              name="player1"
              value={formData.player1}
              onChange={handleInputChange}
              placeholder="e.g., BaconChee#1321"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="player2">Player 2 BattleTag:</label>
            <input
              type="text"
              id="player2"
              name="player2"
              value={formData.player2}
              onChange={handleInputChange}
              placeholder="e.g., Player2#1234"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="hero">Hero:</label>
            <select
              id="hero"
              name="hero"
              value={formData.hero}
              onChange={handleInputChange}
              required
            >
              <option value="">Select a hero</option>
              {heroes.map(hero => (
                <option key={hero.value} value={hero.value}>
                  {hero.label}
                </option>
              ))}
            </select>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="gamemode">Game Mode:</label>
              <select
                id="gamemode"
                name="gamemode"
                value={formData.gamemode}
                onChange={handleInputChange}
              >
                <option value="quickplay">Quickplay</option>
                <option value="competitive">Competitive</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="platform">Platform:</label>
              <select
                id="platform"
                name="platform"
                value={formData.platform}
                onChange={handleInputChange}
              >
                <option value="pc">PC</option>
                <option value="console">Console</option>
              </select>
            </div>
          </div>

          <button type="submit" disabled={loading} className="submit-btn">
            {loading ? 'Comparing...' : 'Compare Players'}
          </button>
        </form>

        {error && (
          <div className="error-message">
            <p>{error}</p>
          </div>
        )}

        {comparison && (
          <div className="comparison-results">
            <h2>
              {comparison.hero.toUpperCase()} Comparison: {comparison.player1} vs {comparison.player2}
            </h2>
            
            {/* Enhanced Analysis Summary */}
            {comparison.enhanced_analysis && (
              <div className="enhanced-analysis">
                <h3 className="analysis-title">Performance Analysis</h3>
                <div className="analysis-grid">
                  <div className="analysis-card">
                    <h4>Overall Performance Scores</h4>
                    <div className="score-comparison">
                      <div className="score-item">
                        <span className="player-name">{comparison.player1}:</span>
                        <span className="score-value">{formatScore(comparison.enhanced_analysis.performance_scores.player1_weighted_score)}%</span>
                      </div>
                      <div className="score-item">
                        <span className="player-name">{comparison.player2}:</span>
                        <span className="score-value">{formatScore(comparison.enhanced_analysis.performance_scores.player2_weighted_score)}%</span>
                      </div>
                      <div className="score-difference">
                        <span>Difference: {formatDifference(comparison.enhanced_analysis.performance_scores.score_difference * 100)}%</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="analysis-card">
                    <h4>Role Effectiveness ({comparison.enhanced_analysis.role_effectiveness.hero_role})</h4>
                    <div className="effectiveness-comparison">
                      <div className="effectiveness-item">
                        <span className="player-name">{comparison.player1}:</span>
                        <span className="effectiveness-value">{formatScore(comparison.enhanced_analysis.role_effectiveness.player1_effectiveness)}%</span>
                      </div>
                      <div className="effectiveness-item">
                        <span className="player-name">{comparison.player2}:</span>
                        <span className="effectiveness-value">{formatScore(comparison.enhanced_analysis.role_effectiveness.player2_effectiveness)}%</span>
                      </div>
                    </div>
                  </div>
                  
                  {comparison.enhanced_analysis.insights && (
                    <div className="analysis-card insights-card">
                      <h4>Key Insights</h4>
                      <p className="overall-verdict">{comparison.enhanced_analysis.insights.overall_verdict}</p>
                      
                      {comparison.enhanced_analysis.insights.key_strengths.player1.length > 0 && (
                        <div className="strengths">
                          <strong>{comparison.player1} excels in:</strong>
                          <span className="strength-tags">
                            {comparison.enhanced_analysis.insights.key_strengths.player1.join(', ')}
                          </span>
                        </div>
                      )}
                      
                      {comparison.enhanced_analysis.insights.key_strengths.player2.length > 0 && (
                        <div className="strengths">
                          <strong>{comparison.player2} excels in:</strong>
                          <span className="strength-tags">
                            {comparison.enhanced_analysis.insights.key_strengths.player2.join(', ')}
                          </span>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            )}
            
            {/* Detailed Stats */}
            <div className="detailed-stats">
              <h3 className="stats-title">Detailed Statistics</h3>
              {comparison.categories.map(renderCategoryStats)}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
