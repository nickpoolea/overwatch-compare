// API service for Overwatch comparison app

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export async function fetchHeroes() {
  const response = await fetch(`${API_BASE_URL}/heroes/`);
  if (!response.ok) throw new Error('Failed to fetch heroes');
  return response.json();
}

export async function comparePlayers(formData) {
  const response = await fetch(`${API_BASE_URL}/compare/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData)
  });
  if (!response.ok) throw new Error('Failed to compare players');
  return response.json();
}
