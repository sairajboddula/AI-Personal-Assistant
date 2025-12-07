from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from backend.ai_engine.app.services.nlu_service import nlu_service
from backend.ai_engine.app.services import mcp_client
import asyncio
import json

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/message")
async def chat(request: ChatRequest):
    """Non-streaming endpoint (legacy support)"""
    intent_data = nlu_service.process_text(request.message)
    
    if intent_data["intent"] == "order_food":
        # Search for food first
        search_result = await mcp_client.search_food(intent_data.get("item", "pizza"))
        
        if search_result.get("success") and search_result.get("results"):
            # Place order for first result
            first_item = search_result["results"][0]
            order_result = await mcp_client.place_food_order(
                first_item["id"],
                intent_data.get("quantity", 1)
            )
            
            if order_result.get("success"):
                return {
                    "response": f"I have placed an order for {order_result['item']} from {order_result['restaurant']}. "
                               f"Order ID: {order_result['order_id']}. Estimated delivery: {order_result['estimated_delivery']}."
                }
            else:
                return {"response": f"Sorry, I couldn't place the order. {order_result.get('error', 'Unknown error')}"}
        else:
            return {"response": f"Sorry, I couldn't find {intent_data.get('item', 'that item')}."}
    
    elif intent_data["intent"] == "order_product":
        # Search for product
        search_result = await mcp_client.search_product(intent_data.get("item", "kindle"))
        
        if search_result.get("success") and search_result.get("results"):
            first_product = search_result["results"][0]
            order_result = await mcp_client.place_product_order(
                first_product["id"],
                intent_data.get("quantity", 1)
            )
            
            if order_result.get("success"):
                return {
                    "response": f"I have placed an order for {order_result['product']}. "
                               f"Order ID: {order_result['order_id']}. Estimated delivery: {order_result['estimated_delivery']}."
                }
            else:
                return {"response": f"Sorry, I couldn't place the order. {order_result.get('error', 'Unknown error')}"}
        else:
            return {"response": f"Sorry, I couldn't find {intent_data.get('item', 'that product')}."}
    
    elif intent_data["intent"] == "check_balance":
        # Get account balance
        account_id = intent_data.get("account_id", "123456")  # Default account
        balance_result = await mcp_client.get_balance(account_id)
        
        if balance_result.get("success"):
            account = balance_result["account"]
            return {
                "response": f"Your {account['account_type']} account balance is ${account['balance']:.2f} {account['currency']}."
            }
        else:
            return {"response": f"Sorry, I couldn't retrieve your balance. {balance_result.get('error', 'Unknown error')}"}
    
    return {"response": "I didn't understand that. Try saying 'Order pizza', 'Buy a Kindle', or 'Check my balance'."}

@router.post("/stream")
async def chat_stream(request: ChatRequest):
    """Streaming endpoint for smooth, Gemini-like responses"""
    
    async def generate_response():
        # Process the message
        intent_data = nlu_service.process_text(request.message)
        response_text = ""
        
        # Handle different intents using MCP
        if intent_data["intent"] == "order_food":
            search_result = await mcp_client.search_food(intent_data.get("item", "pizza"))
            
            if search_result.get("success") and search_result.get("results"):
                first_item = search_result["results"][0]
                order_result = await mcp_client.place_food_order(
                    first_item["id"],
                    intent_data.get("quantity", 1)
                )
                
                if order_result.get("success"):
                    response_text = (
                        f"I have placed an order for {order_result['item']} from {order_result['restaurant']}. "
                        f"Order ID: {order_result['order_id']}. Estimated delivery: {order_result['estimated_delivery']}."
                    )
                else:
                    response_text = f"Sorry, I couldn't place the order. {order_result.get('error', 'Unknown error')}"
            else:
                response_text = f"Sorry, I couldn't find {intent_data.get('item', 'that item')}."
        
        elif intent_data["intent"] == "order_product":
            search_result = await mcp_client.search_product(intent_data.get("item", "kindle"))
            
            if search_result.get("success") and search_result.get("results"):
                first_product = search_result["results"][0]
                order_result = await mcp_client.place_product_order(
                    first_product["id"],
                    intent_data.get("quantity", 1)
                )
                
                if order_result.get("success"):
                    response_text = (
                        f"I have placed an order for {order_result['product']}. "
                        f"Order ID: {order_result['order_id']}. Estimated delivery: {order_result['estimated_delivery']}."
                    )
                else:
                    response_text = f"Sorry, I couldn't place the order. {order_result.get('error', 'Unknown error')}"
            else:
                response_text = f"Sorry, I couldn't find {intent_data.get('item', 'that product')}."
        
        elif intent_data["intent"] == "check_balance":
            account_id = intent_data.get("account_id", "123456")
            balance_result = await mcp_client.get_balance(account_id)
            
            if balance_result.get("success"):
                account = balance_result["account"]
                response_text = f"Your {account['account_type']} account balance is ${account['balance']:.2f} {account['currency']}."
            else:
                response_text = f"Sorry, I couldn't retrieve your balance. {balance_result.get('error', 'Unknown error')}"
        
        else:
            response_text = "I didn't understand that. Try saying 'Order pizza', 'Buy a Kindle', or 'Check my balance'."
        
        # Stream the response character-by-character (Gemini-style)
        for char in response_text:
            yield f"data: {json.dumps({'type': 'token', 'content': char})}\n\n"
            await asyncio.sleep(0.02)  # 20ms delay for smooth typing effect
        
        # Send completion signal
        yield f"data: {json.dumps({'type': 'done'})}\n\n"
    
    return StreamingResponse(
        generate_response(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
