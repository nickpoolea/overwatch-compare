// Utility functions for number formatting and stats

export const formatNumber = (value) => {
  if (value === null || value === undefined || value === "N/A") {
    return "N/A";
  }
  if (typeof value === 'string' && (value.includes('h') || value.includes('m') || value.includes(':'))) {
    return value;
  }
  const numValue = typeof value === 'string' ? parseFloat(value) : value;
  if (isNaN(numValue)) {
    return value;
  }
  if (typeof value === 'string' && value.includes('%')) {
    return value;
  }
  if (Math.abs(numValue) >= 1000) {
    if (numValue % 1 === 0) {
      return numValue.toLocaleString('en-US');
    } else {
      return numValue.toLocaleString('en-US', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
      });
    }
  } else if (numValue % 1 !== 0) {
    return numValue.toLocaleString('en-US', {
      minimumFractionDigits: 0,
      maximumFractionDigits: 2
    });
  } else {
    return numValue.toString();
  }
};

export const formatPercentage = (value) => {
  if (value === null || value === undefined || value === "N/A") {
    return "N/A";
  }
  if (typeof value === 'string' && value.includes('%')) {
    return value;
  }
  const numValue = typeof value === 'string' ? parseFloat(value) : value;
  if (isNaN(numValue)) {
    return value;
  }
  if (numValue > 1) {
    return `${numValue.toFixed(2)}%`;
  } else {
    return `${(numValue * 100).toFixed(2)}%`;
  }
};

export const formatDifference = (value, statLabel) => {
  if (value === null || value === undefined || value === "N/A" || value === "Ties") {
    return value;
  }
  if (typeof value === 'string' && (value.includes('h') || value.includes('m'))) {
    return value;
  }
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
  if (statLabel && (statLabel.toLowerCase().includes('accuracy') || statLabel.toLowerCase().includes('percentage'))) {
    return `${sign}${absValue.toFixed(2)}%`;
  }
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

export const formatScore = (value) => {
  if (value === null || value === undefined || isNaN(value)) {
    return "N/A";
  }
  return (value * 100).toFixed(1);
};

export const isPercentageStat = (statKey, statLabel) => {
  const percentageKeys = ['accuracy', 'percentage', 'hit_percentage', 'critical_hit_accuracy', 'weapon_accuracy', 'scoped_accuracy'];
  const key = statKey ? statKey.toLowerCase() : '';
  const label = statLabel ? statLabel.toLowerCase() : '';
  return percentageKeys.some(keyword => key.includes(keyword) || label.includes(keyword));
};
