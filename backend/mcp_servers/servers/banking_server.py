"""
Banking MCP Server
Official Model Context Protocol implementation for Banking services
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

server = Server("banking-server")

# Mock account data
MOCK_ACCOUNTS = {
    "123456": {
        "account_id": "123456",
        "account_type": "Checking",
        "balance": 5000.00,
        "currency": "USD",
        "status": "active"
    },
    "789012": {
        "account_id": "789012",
        "account_type": "Savings",
        "balance": 15000.00,
        "currency": "USD",
        "status": "active"
    }
}


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools for Banking"""
    return [
        Tool(
            name="get_balance",
            description="Get account balance for a bank account",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {
                        "type": "string",
                        "description": "Bank account ID"
                    }
                },
                "required": ["account_id"]
            }
        ),
        Tool(
            name="process_payment",
            description="Process a payment from the account",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {
                        "type": "string",
                        "description": "Source account ID"
                    },
                    "amount": {
                        "type": "number",
                        "description": "Payment amount",
                        "minimum": 0.01
                    },
                    "merchant": {
                        "type": "string",
                        "description": "Merchant/recipient name"
                    }
                },
                "required": ["account_id", "amount", "merchant"]
            }
        ),
        Tool(
            name="get_transaction_history",
            description="Get recent transaction history for an account",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {
                        "type": "string",
                        "description": "Bank account ID"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of transactions to retrieve",
                        "minimum": 1,
                        "maximum": 50,
                        "default": 10
                    }
                },
                "required": ["account_id"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""
    
    if name == "get_balance":
        return await get_balance(arguments.get("account_id", ""))
    elif name == "process_payment":
        return await process_payment(
            arguments.get("account_id", ""),
            arguments.get("amount", 0),
            arguments.get("merchant", "")
        )
    elif name == "get_transaction_history":
        return await get_transaction_history(
            arguments.get("account_id", ""),
            arguments.get("limit", 10)
        )
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def get_balance(account_id: str) -> list[TextContent]:
    """Get account balance"""
    
    if settings.BANK_MOCK_MODE:
        account = MOCK_ACCOUNTS.get(account_id)
        
        if account:
            response = {
                "success": True,
                "account": account,
                "mode": "mock"
            }
        else:
            response = {
                "success": False,
                "error": f"Account {account_id} not found",
                "mode": "mock"
            }
    else:
        response = {
            "success": False,
            "error": "Real Banking API not yet implemented",
            "mode": "real"
        }
    
    return [TextContent(type="text", text=json.dumps(response, indent=2))]


async def process_payment(account_id: str, amount: float, merchant: str) -> list[TextContent]:
    """Process a payment"""
    
    if settings.BANK_MOCK_MODE:
        account = MOCK_ACCOUNTS.get(account_id)
        
        if not account:
            response = {"success": False, "error": f"Account {account_id} not found"}
        elif account["balance"] < amount:
            response = {"success": False, "error": "Insufficient funds"}
        else:
            import random
            transaction_id = f"TXN-{random.randint(100000, 999999)}"
            new_balance = account["balance"] - amount
            
            # Update mock balance (in real implementation, this would be in database)
            MOCK_ACCOUNTS[account_id]["balance"] = new_balance
            
            response = {
                "success": True,
                "transaction_id": transaction_id,
                "status": "completed",
                "amount": amount,
                "merchant": merchant,
                "new_balance": new_balance,
                "timestamp": "2025-12-07T17:10:00Z",
                "mode": "mock"
            }
    else:
        response = {"success": False, "error": "Real Banking API not yet implemented", "mode": "real"}
    
    return [TextContent(type="text", text=json.dumps(response, indent=2))]


async def get_transaction_history(account_id: str, limit: int = 10) -> list[TextContent]:
    """Get transaction history"""
    
    if settings.BANK_MOCK_MODE:
        account = MOCK_ACCOUNTS.get(account_id)
        
        if not account:
            response = {"success": False, "error": f"Account {account_id} not found"}
        else:
            # Mock transaction history
            transactions = [
                {"id": "TXN-001", "date": "2025-12-06", "description": "Grocery Store", "amount": -85.50, "balance": 5085.50},
                {"id": "TXN-002", "date": "2025-12-05", "description": "Salary Deposit", "amount": 3000.00, "balance": 5171.00},
                {"id": "TXN-003", "date": "2025-12-04", "description": "Electric Bill", "amount": -120.00, "balance": 2171.00},
                {"id": "TXN-004", "date": "2025-12-03", "description": "Restaurant", "amount": -45.00, "balance": 2291.00},
            ]
            
            response = {
                "success": True,
                "account_id": account_id,
                "transactions": transactions[:limit],
                "count": len(transactions[:limit]),
                "mode": "mock"
            }
    else:
        response = {"success": False, "error": "Real Banking API not yet implemented", "mode": "real"}
    
    return [TextContent(type="text", text=json.dumps(response, indent=2))]


async def main():
    """Run the Banking MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
