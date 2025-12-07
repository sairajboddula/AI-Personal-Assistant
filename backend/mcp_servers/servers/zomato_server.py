"""
Zomato MCP Server
Official Model Context Protocol implementation for Zomato food ordering service
"""

import asyncio
import json
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.mcp_servers.core.config import settings

# Create MCP server instance
server = Server("zomato-server")

# Mock data for testing
MOCK_FOOD_ITEMS = [
    {"id": "1", "name": "Cheese Pizza", "restaurant": "Pizza Hut", "price": 15.0, "rating": 4.5},
    {"id": "2", "name": "Chicken Biryani", "restaurant": "Paradise", "price": 12.0, "rating": 4.7},
    {"id": "3", "name": "Veg Burger", "restaurant": "McDonald's", "price": 8.0, "rating": 4.2},
    {"id": "4", "name": "Pasta Alfredo", "restaurant": "Olive Garden", "price": 14.0, "rating": 4.6},
]


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools for Zomato"""
    return [
        Tool(
            name="search_food",
            description="Search for food items on Zomato by name or cuisine type",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Food item or cuisine to search for (e.g., 'pizza', 'biryani', 'burger')"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="place_order",
            description="Place a food order on Zomato",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_id": {
                        "type": "string",
                        "description": "ID of the food item to order"
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "Number of items to order",
                        "minimum": 1,
                        "maximum": 10
                    }
                },
                "required": ["item_id", "quantity"]
            }
        ),
        Tool(
            name="get_restaurant_info",
            description="Get detailed information about a restaurant",
            inputSchema={
                "type": "object",
                "properties": {
                    "restaurant_name": {
                        "type": "string",
                        "description": "Name of the restaurant"
                    }
                },
                "required": ["restaurant_name"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls from MCP client"""
    
    if name == "search_food":
        return await search_food(arguments.get("query", ""))
    
    elif name == "place_order":
        return await place_order(
            arguments.get("item_id", ""),
            arguments.get("quantity", 1)
        )
    
    elif name == "get_restaurant_info":
        return await get_restaurant_info(arguments.get("restaurant_name", ""))
    
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]


async def search_food(query: str) -> list[TextContent]:
    """Search for food items"""
    query_lower = query.lower()
    
    if settings.ZOMATO_MOCK_MODE:
        # Mock mode - filter from mock data
        results = [
            item for item in MOCK_FOOD_ITEMS
            if query_lower in item["name"].lower() or query_lower in item["restaurant"].lower()
        ]
        
        if not results:
            results = MOCK_FOOD_ITEMS  # Return all if no match
        
        response = {
            "success": True,
            "results": results,
            "count": len(results),
            "mode": "mock"
        }
    else:
        # Real API mode - would make actual Zomato API call
        # TODO: Implement real Zomato API integration
        response = {
            "success": False,
            "error": "Real Zomato API not yet implemented",
            "mode": "real"
        }
    
    return [TextContent(
        type="text",
        text=json.dumps(response, indent=2)
    )]


async def place_order(item_id: str, quantity: int) -> list[TextContent]:
    """Place a food order"""
    
    if settings.ZOMATO_MOCK_MODE:
        # Mock mode - simulate order placement
        item = next((item for item in MOCK_FOOD_ITEMS if item["id"] == item_id), None)
        
        if not item:
            response = {
                "success": False,
                "error": f"Item with ID {item_id} not found"
            }
        else:
            import random
            order_id = f"ZOMATO-{random.randint(10000, 99999)}"
            total_price = item["price"] * quantity
            
            response = {
                "success": True,
                "order_id": order_id,
                "status": "confirmed",
                "item": item["name"],
                "restaurant": item["restaurant"],
                "quantity": quantity,
                "total_price": total_price,
                "estimated_delivery": "30-40 mins",
                "mode": "mock"
            }
    else:
        # Real API mode
        response = {
            "success": False,
            "error": "Real Zomato API not yet implemented",
            "mode": "real"
        }
    
    return [TextContent(
        type="text",
        text=json.dumps(response, indent=2)
    )]


async def get_restaurant_info(restaurant_name: str) -> list[TextContent]:
    """Get restaurant information"""
    
    if settings.ZOMATO_MOCK_MODE:
        # Mock mode
        restaurants = {
            "pizza hut": {
                "name": "Pizza Hut",
                "cuisine": "Italian, Pizza",
                "rating": 4.5,
                "delivery_time": "30-40 mins",
                "min_order": 10.0
            },
            "paradise": {
                "name": "Paradise",
                "cuisine": "Indian, Biryani",
                "rating": 4.7,
                "delivery_time": "40-50 mins",
                "min_order": 12.0
            },
            "mcdonald's": {
                "name": "McDonald's",
                "cuisine": "Fast Food, Burgers",
                "rating": 4.2,
                "delivery_time": "20-30 mins",
                "min_order": 5.0
            }
        }
        
        info = restaurants.get(restaurant_name.lower())
        if info:
            response = {
                "success": True,
                "restaurant": info,
                "mode": "mock"
            }
        else:
            response = {
                "success": False,
                "error": f"Restaurant '{restaurant_name}' not found",
                "mode": "mock"
            }
    else:
        response = {
            "success": False,
            "error": "Real Zomato API not yet implemented",
            "mode": "real"
        }
    
    return [TextContent(
        type="text",
        text=json.dumps(response, indent=2)
    )]


async def main():
    """Run the Zomato MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
