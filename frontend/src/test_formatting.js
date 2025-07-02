// Test file to verify number formatting functions

// Copy the formatting functions from App.js for testing
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

// Test cases
console.log('=== Testing formatNumber ===');
console.log('1234 ->', formatNumber(1234)); // Should be "1,234"
console.log('1234.56 ->', formatNumber(1234.56)); // Should be "1,234.56"
console.log('12345678 ->', formatNumber(12345678)); // Should be "12,345,678"
console.log('12345678.123 ->', formatNumber(12345678.123)); // Should be "12,345,678.12"
console.log('123.456 ->', formatNumber(123.456)); // Should be "123.46"
console.log('123 ->', formatNumber(123)); // Should be "123"
console.log('12.3 ->', formatNumber(12.3)); // Should be "12.3"
console.log('"N/A" ->', formatNumber("N/A")); // Should be "N/A"

console.log('\n=== Testing formatPercentage ===');
console.log('0.1234 ->', formatPercentage(0.1234)); // Should be "12.34%"
console.log('0.5 ->', formatPercentage(0.5)); // Should be "50.00%"
console.log('45.67 ->', formatPercentage(45.67)); // Should be "45.67%"
console.log('"45.67%" ->', formatPercentage("45.67%")); // Should be "45.67%"

console.log('\n=== Testing formatDifference ===');
console.log('1234 ->', formatDifference(1234)); // Should be "+1,234"
console.log('-1234 ->', formatDifference(-1234)); // Should be "-1,234"
console.log('1234.56 ->', formatDifference(1234.56)); // Should be "+1,234.56"
console.log('-123.45 ->', formatDifference(-123.45)); // Should be "-123.45"
console.log('15.5, "accuracy" ->', formatDifference(15.5, "accuracy")); // Should be "+15.50%"
console.log('-5.2, "weapon accuracy" ->', formatDifference(-5.2, "weapon accuracy")); // Should be "-5.20%"
