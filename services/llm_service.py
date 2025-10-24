import httpx
from typing import List, Dict, Any
import config
from utils.formatters import format_context_for_llm
from utils.logger import logger


class LLMService:
    def __init__(self):
        self.api_url = config.LLM_API_URL
        
        self.system_prompt = """تو یک دستیار فروش حرفه‌ای هستی که به مشتریان در مورد محصولات الکترونیکی کمک می‌کنی.
وظیفه تو این است که:
1. به سوالات مشتری در مورد محصولات پاسخ دهی
2. اطلاعات دقیق و کامل از محصولات موجود ارائه دهی
3. در صورت نیاز، محصولات مشابه پیشنهاد دهی
4. همیشه مودب و حرفه‌ای باشی
5. فقط به زبان فارسی پاسخ دهی

اگر محصول مورد نظر موجود نبود، به مشتری اطلاع بده و محصولات مشابه پیشنهاد بده.
اگر سوال مشتری مربوط به محصولات نبود، به او بگو که فقط می‌توانی در مورد محصولات الکترونیکی کمک کنی."""
    
    async def generate_response(self, user_message: str, context_products: List[Dict[str, Any]]) -> str:
        context = format_context_for_llm(context_products)
        
        prompt = f"""{self.system_prompt}

اطلاعات محصولات:
{context}

سوال مشتری: {user_message}

پاسخ تو (فقط فارسی):"""
        
        try:
            logger.info(f"Sending request to LLM API: {self.api_url}")
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.api_url,
                    json={"message": prompt},
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                data = response.json()
                
                if isinstance(data, dict) and "response" in data:
                    return data["response"].strip()
                elif isinstance(data, dict) and "message" in data:
                    return data["message"].strip()
                elif isinstance(data, str):
                    return data.strip()
                else:
                    return str(data).strip()
                    
        except httpx.TimeoutException:
            logger.error("LLM API timeout")
            return "متأسفانه زمان پاسخگویی به پایان رسید. لطفاً دوباره تلاش کنید."
        except httpx.HTTPError as e:
            logger.error(f"LLM API HTTP error: {str(e)}")
            return "متأسفانه در حال حاضر قادر به پاسخگویی نیستم. لطفاً بعداً تلاش کنید."
        except Exception as e:
            logger.error(f"LLM API unexpected error: {str(e)}")
            return "متأسفانه خطایی رخ داد. لطفاً بعداً تلاش کنید."
