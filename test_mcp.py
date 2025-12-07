"""
Test script for MCP implementation with new backend structure
"""

import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.ai_engine.app.services.mcp_client import search_food, place_food_order, search_product, get_balance

async def test_mcp():
    """Test MCP integration"""
    
    print("=" * 60)
    print("Testing Official MCP Implementation (New Structure)")
    print("=" * 60)
    
    # Test 1: Search for food (Zomato MCP Server)
    print("\n1. Testing Zomato MCP Server - search_food")
    print("-" * 60)
    result = await search_food("pizza")
    print(f"Result: {result}")
    
    if result.get("success"):
        print("✅ Zomato search_food works!")
        
        # Test 2: Place food order
        print("\n2. Testing Zomato MCP Server - place_order")
        print("-" * 60)
        if result.get("results"):
            first_item = result["results"][0]
            order_result = await place_food_order(first_item["id"], 1)
            print(f"Result: {order_result}")
            if order_result.get("success"):
                print("✅ Zomato place_order works!")
            else:
                print("❌ Zomato place_order failed")
    else:
        print("❌ Zomato search_food failed")
    
    # Test 3: Search for product (Amazon MCP Server)
    print("\n3. Testing Amazon MCP Server - search_product")
    print("-" * 60)
    result = await search_product("kindle")
    print(f"Result: {result}")
    if result.get("success"):
        print("✅ Amazon search_product works!")
    else:
        print("❌ Amazon search_product failed")
    
    # Test 4: Get balance (Banking MCP Server)
    print("\n4. Testing Banking MCP Server - get_balance")
    print("-" * 60)
    result = await get_balance("123456")
    print(f"Result: {result}")
    if result.get("success"):
        print("✅ Banking get_balance works!")
    else:
        print("❌ Banking get_balance failed")
    
    print("\n" + "=" * 60)
    print("MCP Testing Complete!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_mcp())
