import React, { useState, useEffect, useRef } from 'react';
import '../App.css';
import { formatNumber, formatPercentage, formatDifference, formatScore, isPercentageStat } from '../utils/formatting';
import { fetchHeroes, comparePlayers } from '../services/api';

function ComparePage() {
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
  const resultsRef = useRef(null);

  useEffect(() => {
    fetchHeroes()
      .then(setHeroes)
      .catch(() => setError('Failed to fetch heroes'));
  }, []);

  useEffect(() => {
    if (comparison && resultsRef.current) {
      resultsRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }, [comparison]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setComparison(null);
    try {
      const data = await comparePlayers(formData);
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
                const isPercentage = isPercentageStat(stat.key, stat.label);
                const player1Value = isPercentage 
                  ? formatPercentage(stat.player1_value) 
                  : formatNumber(stat.player1_value);
                const player2Value = isPercentage 
                  ? formatPercentage(stat.player2_value) 
                  : formatNumber(stat.player2_value);
                const differenceValue = formatDifference(stat.difference, stat.label);
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
                  <span className="player-name">Wins - {category.summary.player1_wins}</span>
                </div>
                <div className="score-item">
                  <span className="player-name">Wins - {category.summary.player2_wins}</span>
                </div>
                <div className="score-item">
                  <span className="player-name">Ties: {category.summary.ties}</span>
                </div>
                <div className="score-item">
                  <span className="player-name">Avg Difference:</span>
                  <span className={`stat-badge ${category.summary.average_difference > 0 ? 'positive' : category.summary.average_difference < 0 ? 'negative' : 'neutral'}`}>{formatDifference(category.summary.average_difference)}</span>
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
                <option key={hero.value} value={hero.value}>{hero.label}</option>
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
            <button type="submit" className="google-btn primary" disabled={loading}>
              {loading ? (<><span className="loading-spinner"></span>Comparing...</>) : 'Compare Players'}
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

export default ComparePage;
