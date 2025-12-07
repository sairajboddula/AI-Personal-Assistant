"""
Amazon MCP Server
Official Model Context Protocol implementation for Amazon e-commerce service
"""

import asyncio
import json
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.mcp_servers.core.config import settings

server = Server("amazon-server")

# Mock product data
MOCK_PRODUCTS = [
    {"id": "B001", "name": "Kindle Paperwhite", "category": "Electronics", "price": 129.99, "rating": 4.6, "in_stock": True},
    {"id": "B002", "name": "Echo Dot", "category": "Smart Home", "price": 49.99, "rating": 4.7, "in_stock": True},
    {"id": "B003", "name": "Fire TV Stick", "category": "Electronics", "price": 39.99, "rating": 4.5, "in_stock": True},
    {"id": "B004", "name": "AmazonBasics USB Cable", "category": "Accessories", "price": 7.99, "rating": 4.4, "in_stock": True},
]


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools for Amazon"""
    return [
        Tool(
            name="search_product",
            description="Search for products on Amazon by name or category",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Product name or category to search for"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="place_order",
            description="Place an order for a product on Amazon",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_id": {
                        "type": "string",
                        "description": "Product ID to order"
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "Quantity to order",
                        "minimum": 1,
                        "maximum": 10
                    }
                },
                "required": ["item_id"]
            }
        ),
        Tool(
            name="get_product_details",
            description="Get detailed information about a specific product",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "Amazon product ID"
                    }
                },
                "required": ["product_id"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""
    
    if name == "search_product":
        return await search_product(arguments.get("query", ""))
    elif name == "place_order":
        return await place_order(
            arguments.get("item_id", ""),
            arguments.get("quantity", 1)
        )
    elif name == "get_product_details":
        return await get_product_details(arguments.get("product_id", ""))
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def search_product(query: str) -> list[TextContent]:
    """Search for products"""
    query_lower = query.lower()
    
    if settings.AMAZON_MOCK_MODE:
        results = [
            product for product in MOCK_PRODUCTS
            if query_lower in product["name"].lower() or query_lower in product["category"].lower()
        ]
        
        if not results:
            results = MOCK_PRODUCTS
        
        response = {
            "success": True,
            "results": results,
            "count": len(results),
            "mode": "mock"
        }
    else:
        response = {
            "success": False,
            "error": "Real Amazon API not yet implemented",
            "mode": "real"
        }
    
    return [TextContent(type="text", text=json.dumps(response, indent=2))]


async def place_order(item_id: str, quantity: int = 1) -> list[TextContent]:
    """Place an order"""
    
    if settings.AMAZON_MOCK_MODE:
        product = next((p for p in MOCK_PRODUCTS if p["id"] == item_id), None)
        
        if not product:
            response = {"success": False, "error": f"Product {item_id} not found"}
        elif not product["in_stock"]:
            response = {"success": False, "error": "Product out of stock"}
        else:
            import random
            order_id = f"AMZ-{random.randint(100000, 999999)}"
            total_price = product["price"] * quantity
            
            response = {
                "success": True,
                "order_id": order_id,
                "status": "processing",
                "product": product["name"],
                "quantity": quantity,
                "total_price": total_price,
                "estimated_delivery": "2-3 business days",
                "mode": "mock"
            }
    else:
        response = {"success": False, "error": "Real Amazon API not yet implemented", "mode": "real"}
    
    return [TextContent(type="text", text=json.dumps(response, indent=2))]


async def get_product_details(product_id: str) -> list[TextContent]:
    """Get product details"""
    
    if settings.AMAZON_MOCK_MODE:
        product = next((p for p in MOCK_PRODUCTS if p["id"] == product_id), None)
        
        if product:
            response = {
                "success": True,
                "product": product,
                "mode": "mock"
            }
        else:
            response = {"success": False, "error": f"Product {product_id} not found", "mode": "mock"}
    else:
        response = {"success": False, "error": "Real Amazon API not yet implemented", "mode": "real"}
    
    return [TextContent(type="text", text=json.dumps(response, indent=2))]


async def main():
    """Run the Amazon MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
