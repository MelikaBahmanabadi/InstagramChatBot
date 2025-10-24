from typing import List, Dict, Any
import config


def format_context_for_llm(products: List[Dict[str, Any]]) -> str:
    if not products:
        return "هیچ محصولی یافت نشد."
    
    context = "محصولات موجود:\n\n"
    for idx, product in enumerate(products, 1):
        context += f"{idx}. {product['name']}\n"
        context += f"   توضیحات: {product['description']}\n"
        context += f"   قیمت: {product['price']:,.0f} تومان\n\n"
    
    return context[:config.MAX_CONTEXT_LENGTH]

