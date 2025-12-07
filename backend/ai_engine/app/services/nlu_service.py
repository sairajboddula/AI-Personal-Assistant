from typing import Dict, Any
import re

class NLUService:
    def process_text(self, text: str) -> Dict[str, Any]:
        """Process user text and extract intent and parameters"""
        text_lower = text.lower()
        
        # Food ordering intents
        if "order" in text_lower and any(food in text_lower for food in ["pizza", "biryani", "burger", "pasta", "food"]):
            # Extract food item
            food_items = ["pizza", "biryani", "burger", "pasta", "chicken", "veg"]
            item = next((food for food in food_items if food in text_lower), "pizza")
            
            return {
                "intent": "order_food",
                "item": item,
                "quantity": self._extract_quantity(text_lower)
            }
        
        # Product ordering intents (Amazon)
        elif any(keyword in text_lower for keyword in ["buy", "purchase", "get me"]) or \
             any(product in text_lower for product in ["kindle", "echo", "fire tv", "usb"]):
            # Extract product
            products = ["kindle", "echo", "fire tv", "usb"]
            item = next((prod for prod in products if prod in text_lower), "kindle")
            
            return {
                "intent": "order_product",
                "item": item,
                "quantity": self._extract_quantity(text_lower)
            }
        
        # Banking intents
        elif any(keyword in text_lower for keyword in ["balance", "account", "money"]):
            return {
                "intent": "check_balance",
                "account_id": "123456"  # Default account
            }
        
        elif "pay" in text_lower or "payment" in text_lower or "transfer" in text_lower:
            return {
                "intent": "process_payment",
                "account_id": "123456",
                "amount": self._extract_amount(text_lower),
                "merchant": "Unknown"
            }
        
        return {"intent": "unknown"}
    
    def _extract_quantity(self, text: str) -> int:
        """Extract quantity from text"""
        # Look for numbers
        numbers = re.findall(r'\d+', text)
        if numbers:
            return int(numbers[0])
        
        # Look for words
        word_to_num = {
            "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
        }
        for word, num in word_to_num.items():
            if word in text:
                return num
        
        return 1  # Default
    
    def _extract_amount(self, text: str) -> float:
        """Extract monetary amount from text"""
        # Look for dollar amounts
        amounts = re.findall(r'\$?(\d+\.?\d*)', text)
        if amounts:
            return float(amounts[0])
        return 0.0

nlu_service = NLUService()
