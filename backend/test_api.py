#!/usr/bin/env python
"""
Simple test script to verify the Overwatch comparison backend is working.
"""

import requests
import json

def test_backend():
    base_url = "http://localhost:8000/api"
    
    print("Testing Overwatch Comparison API...")
    
    # Test 1: Get heroes list
    print("\n1. Testing GET /heroes/")
    try:
        response = requests.get(f"{base_url}/heroes/")
        if response.status_code == 200:
            heroes = response.json()
            print(f"✓ Successfully fetched {len(heroes)} heroes")
            print(f"Sample heroes: {[h['label'] for h in heroes[:5]]}")
        else:
            print(f"✗ Failed to fetch heroes: {response.status_code}")
    except requests.ConnectionError:
        print("✗ Cannot connect to backend. Make sure Django server is running on port 8000")
        return
    
    # Test 2: Compare players
    print("\n2. Testing POST /compare/")
    test_data = {
        "player1": "BaconChee#1321",
        "player2": "TestPlayer#1234",
        "hero": "ana",
        "gamemode": "quickplay",
        "platform": "pc"
    }
    
    try:
        response = requests.post(
            f"{base_url}/compare/",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Successfully compared players")
            print(f"Hero: {result['hero']}")
            print(f"Categories found: {len(result['categories'])}")
        else:
            print(f"✗ Comparison failed: {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"✗ Error during comparison: {e}")

if __name__ == "__main__":
    test_backend()
