import React, { useState, useEffect, useRef } from 'react';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

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

  // Ref for the results container to enable auto-scrolling
  const resultsRef = useRef(null);

  // Auto-scroll to results when comparison data is available
  useEffect(() => {
    if (comparison && resultsRef.current) {
      resultsRef.current.scrollIntoView({ 
        behavior: 'smooth',
        block: 'start'
      });
    }
  }, [comparison]);

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
      <div key={category.name} className="result-card">
        <div className="result-card-header">
          <h3 className="result-card-title">{category.name}</h3>
        </div>
        <div className="result-card-body">
          <table className="data-table">
            <thead>
              <tr>
                <th>Stat</th>
                <th>{comparison.player1}</th>
                <th>{comparison.player2}</th>
                <th>Difference</th>
              </tr>
            </thead>
            <tbody>
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
                
                // Determine badge type
                let badgeClass = 'neutral';
                if (stat.difference > 0) badgeClass = 'positive';
                else if (stat.difference < 0) badgeClass = 'negative';
                
                return (
                  <tr key={index}>
                    <td><strong>{stat.label}</strong></td>
                    <td>{player1Value}</td>
                    <td>{player2Value}</td>
                    <td>
                      <span className={`stat-badge ${badgeClass}`}>
                        {differenceValue}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
          
          {category.summary && Object.keys(category.summary).length > 0 && (
            <div className="alert alert-info" style={{marginTop: '20px'}}>
              <div className="analysis-title">Category Summary</div>
              <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '12px', marginTop: '12px'}}>
                <div className="score-item">
                  <span className="player-name">Wins - {comparison.player1}:</span>
                  <span className="score-value">{category.summary.player1_wins}</span>
                </div>
                <div className="score-item">
                  <span className="player-name">Wins - {comparison.player2}:</span>
                  <span className="score-value">{category.summary.player2_wins}</span>
                </div>
                <div className="score-item">
                  <span className="player-name">Ties:</span>
                  <span className="score-value">{category.summary.ties}</span>
                </div>
                <div className="score-item">
                  <span className="player-name">Avg Difference:</span>
                  <span className={`stat-badge ${category.summary.average_difference > 0 ? 'positive' : category.summary.average_difference < 0 ? 'negative' : 'neutral'}`}>
                    {formatDifference(category.summary.average_difference)}
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="App">
      <header className="google-header">
        <h1>Overwatch Player Comparison</h1>
      </header>

      <div className="main-container">
        <form onSubmit={handleSubmit} className="search-form">
          <div className="form-group">
            <label className="form-label">Player 1 BattleTag</label>
            <input
              type="text"
              name="player1"
              value={formData.player1}
              onChange={handleInputChange}
              placeholder="e.g., BaconChee#1321"
              className="form-input"
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Player 2 BattleTag</label>
            <input
              type="text"
              name="player2"
              value={formData.player2}
              onChange={handleInputChange}
              placeholder="e.g., Player2#1234"
              className="form-input"
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Hero</label>
            <select
              name="hero"
              value={formData.hero}
              onChange={handleInputChange}
              className="form-select"
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
              <label className="form-label">Game Mode</label>
              <select
                name="gamemode"
                value={formData.gamemode}
                onChange={handleInputChange}
                className="form-select"
              >
                <option value="quickplay">Quickplay</option>
                <option value="competitive">Competitive</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Platform</label>
              <select
                name="platform"
                value={formData.platform}
                onChange={handleInputChange}
                className="form-select"
              >
                <option value="pc">PC</option>
                <option value="console">Console</option>
              </select>
            </div>
          </div>

          <div className="search-buttons">
            <button 
              type="submit" 
              className="google-btn primary"
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="loading-spinner"></span>
                  Comparing...
                </>
              ) : (
                'Compare Players'
              )}
            </button>
          </div>
        </form>

        {error && (
          <div className="alert alert-danger">
            <strong>Error:</strong> {error}
          </div>
        )}
      </div>

      {comparison && (
        <div className="results-container" ref={resultsRef}>
          <div className="alert alert-success">
            <strong>{comparison.hero.toUpperCase()} Comparison:</strong> {comparison.player1} vs {comparison.player2}
          </div>
          
          {/* Enhanced Analysis Summary */}
          {comparison.enhanced_analysis && (
            <div className="result-card">
              <div className="result-card-header">
                <h2 className="result-card-title">Performance Analysis</h2>
              </div>
              <div className="result-card-body">
                <div className="analysis-grid">
                  <div className="analysis-item">
                    <div className="analysis-title">Overall Performance Scores</div>
                    <div className="score-item">
                      <span className="player-name">{comparison.player1}:</span>
                      <span className="score-value">{formatScore(comparison.enhanced_analysis.performance_scores.player1_weighted_score)}%</span>
                    </div>
                    <div className="score-item">
                      <span className="player-name">{comparison.player2}:</span>
                      <span className="score-value">{formatScore(comparison.enhanced_analysis.performance_scores.player2_weighted_score)}%</span>
                    </div>
                    <div className="score-item">
                      <span className="player-name">Difference:</span>
                      <span className="score-value">{formatDifference(comparison.enhanced_analysis.performance_scores.score_difference * 100)}%</span>
                    </div>
                  </div>
                  
                  <div className="analysis-item">
                    <div className="analysis-title">
                      Role Effectiveness ({comparison.enhanced_analysis.role_effectiveness.hero_role})
                    </div>
                    <div className="score-item">
                      <span className="player-name">{comparison.player1}:</span>
                      <span className="score-value">{formatScore(comparison.enhanced_analysis.role_effectiveness.player1_effectiveness)}%</span>
                    </div>
                    <div className="score-item">
                      <span className="player-name">{comparison.player2}:</span>
                      <span className="score-value">{formatScore(comparison.enhanced_analysis.role_effectiveness.player2_effectiveness)}%</span>
                    </div>
                  </div>
                  
                  {comparison.enhanced_analysis.insights && (
                    <div className="analysis-item">
                      <div className="analysis-title">Key Insights</div>
                      <div className="insights-content">
                        <div className="verdict">
                          {comparison.enhanced_analysis.insights.overall_verdict}
                        </div>
                        
                        {comparison.enhanced_analysis.insights.key_strengths.player1.length > 0 && (
                          <div style={{marginBottom: '12px'}}>
                            <div style={{fontWeight: '500', marginBottom: '6px'}}>
                              {comparison.player1} excels in:
                            </div>
                            <div className="strength-tags">
                              {comparison.enhanced_analysis.insights.key_strengths.player1.map((strength, idx) => (
                                <span key={idx} className="strength-tag">{strength}</span>
                              ))}
                            </div>
                          </div>
                        )}
                        
                        {comparison.enhanced_analysis.insights.key_strengths.player2.length > 0 && (
                          <div>
                            <div style={{fontWeight: '500', marginBottom: '6px'}}>
                              {comparison.player2} excels in:
                            </div>
                            <div className="strength-tags">
                              {comparison.enhanced_analysis.insights.key_strengths.player2.map((strength, idx) => (
                                <span key={idx} className="strength-tag">{strength}</span>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
          
          {/* Detailed Stats */}
          <div className="result-card">
            <div className="result-card-header">
              <h2 className="result-card-title">Detailed Statistics</h2>
            </div>
            <div className="result-card-body">
              {comparison.categories.map(renderCategoryStats)}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
