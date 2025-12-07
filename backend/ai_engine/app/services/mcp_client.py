"""
MCP Client Service - Simplified Version
Official Model Context Protocol client for connecting to MCP servers
"""

import asyncio
from typing import Dict, Any, Optional
import json
import httpx


class MCPClientService:
    """Simplified MCP Client using HTTP instead of stdio for easier integration"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000/api/v1"
    
    async def call_tool(self, server_name: str, tool_name: str, arguments: dict) -> Any:
        """
        Call a tool via HTTP (simplified approach)
        
        For now, we'll use direct function calls to the MCP server logic
        This is a temporary solution until we properly implement stdio transport
        """
        # Direct imports now work with proper backend package structure
        try:
            if server_name == 'zomato':
                from backend.mcp_servers.servers.zomato_server import search_food as zomato_search, place_order as zomato_order
                
                if tool_name == 'search_food':
                    result = await zomato_search(arguments.get('query', ''))
                elif tool_name == 'place_order':
                    result = await zomato_order(arguments.get('item_id', ''), arguments.get('quantity', 1))
                else:
                    return {"success": False, "error": f"Unknown tool: {tool_name}"}
                
                # Extract text from TextContent
                if result and len(result) > 0:
                    return json.loads(result[0].text)
                    
            elif server_name == 'amazon':
                from backend.mcp_servers.servers.amazon_server import search_product as amazon_search, place_order as amazon_order
                
                if tool_name == 'search_product':
                    result = await amazon_search(arguments.get('query', ''))
                elif tool_name == 'place_order':
                    result = await amazon_order(arguments.get('item_id', ''), arguments.get('quantity', 1))
                else:
                    return {"success": False, "error": f"Unknown tool: {tool_name}"}
                
                if result and len(result) > 0:
                    return json.loads(result[0].text)
                    
            elif server_name == 'banking':
                from backend.mcp_servers.servers.banking_server import get_balance as bank_balance, process_payment as bank_payment
                
                if tool_name == 'get_balance':
                    result = await bank_balance(arguments.get('account_id', ''))
                elif tool_name == 'process_payment':
                    result = await bank_payment(
                        arguments.get('account_id', ''),
                        arguments.get('amount', 0),
                        arguments.get('merchant', '')
                    )
                else:
                    return {"success": False, "error": f"Unknown tool: {tool_name}"}
                
                if result and len(result) > 0:
                    return json.loads(result[0].text)
            
            return {"success": False, "error": "Unknown server"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}


# Global MCP client instance
mcp_client = MCPClientService()


# Helper functions for specific integrations

async def search_food(query: str) -> dict:
    """Search for food on Zomato via MCP"""
    try:
        result = await mcp_client.call_tool('zomato', 'search_food', {'query': query})
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}


async def place_food_order(item_id: str, quantity: int) -> dict:
    """Place a food order on Zomato via MCP"""
    try:
        result = await mcp_client.call_tool('zomato', 'place_order', {
            'item_id': item_id,
            'quantity': quantity
        })
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}


async def search_product(query: str) -> dict:
    """Search for products on Amazon via MCP"""
    try:
        result = await mcp_client.call_tool('amazon', 'search_product', {'query': query})
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}


async def place_product_order(item_id: str, quantity: int = 1) -> dict:
    """Place a product order on Amazon via MCP"""
    try:
        result = await mcp_client.call_tool('amazon', 'place_order', {
            'item_id': item_id,
            'quantity': quantity
        })
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}


async def get_balance(account_id: str) -> dict:
    """Get bank account balance via MCP"""
    try:
        result = await mcp_client.call_tool('banking', 'get_balance', {'account_id': account_id})
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}


async def process_payment(account_id: str, amount: float, merchant: str) -> dict:
    """Process a payment via MCP"""
    try:
        result = await mcp_client.call_tool('banking', 'process_payment', {
            'account_id': account_id,
            'amount': amount,
            'merchant': merchant
        })
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}
