from typing import List, Dict, Any
import re
from database.db_manager import DatabaseManager
import config


class RAGService:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def retrieve_relevant_products(self, user_query: str) -> List[Dict[str, Any]]:
        cleaned_query = self._clean_query(user_query)
        keywords = self._extract_keywords(cleaned_query)
        
        all_results = []
        seen_ids = set()
        
        for keyword in keywords:
            results = self.db_manager.search_products(keyword, limit=config.RAG_TOP_K)
            for product in results:
                if product['id'] not in seen_ids:
                    all_results.append(product)
                    seen_ids.add(product['id'])
        
        if not all_results:
            results = self.db_manager.search_products(cleaned_query, limit=config.RAG_TOP_K)
            all_results = results
        
        return all_results[:config.RAG_TOP_K]
    
    def _clean_query(self, query: str) -> str:
        query = re.sub(r'[^\w\s]', ' ', query)
        query = ' '.join(query.split())
        return query.strip()
    
    def _extract_keywords(self, query: str) -> List[str]:
        stopwords = {
            'چیه', 'چیست', 'چی', 'چیا', 'چه', 'چها',
            'هست', 'هستم', 'هستی', 'هستید', 'هستند', 'است', 'استم', 'بود', 'بودم', 'بودی', 'بودند',
            'می', 'میشه', 'میشود', 'شد', 'شده', 'شو', 'شوید',
            'را', 'رو', 'به', 'از', 'در', 'درون', 'داخل', 'بیرون', 'که', 'کی', 'کجا',
            'این', 'اون', 'آن', 'اینها', 'آنها', 'اونها',
            'یک', 'یه', 'دو', 'سه', 'چند', 'چندتا', 'تا',
            'برای', 'واسه', 'برا', 'بابت',
            'با', 'بدون', 'بی',
            'و', 'یا', 'اما', 'ولی', 'پس', 'اگر', 'اگه',
            'چرا', 'چطور', 'چطوری', 'چجوری', 'چگونه',
            'چقدر', 'چقدره', 'چند', 'کدام', 'کدوم', 'کدومش',
            'هر', 'همه', 'تمام', 'کل', 'جمیع',
            'دارد', 'دارم', 'داری', 'دارید', 'دارن', 'دارند', 'داره', 'دارین',
            'میخوام', 'میخواهم', 'میخوای', 'میخواید', 'میخوان', 'میخواهید', 'خواستم',
            'بگو', 'بگید', 'بگین', 'بگویید', 'بفرما', 'بفرمایید',
            'لطفا', 'لطفاً', 'خواهش', 'خواهشا', 'ممنون', 'متشکرم', 'سپاس',
            'سلام', 'درود', 'صبح', 'عصر', 'شب', 'روز',
            'آیا', 'آیه', 'ایا', 'مگر', 'مگه',
            'نه', 'نی', 'خیر', 'بله', 'آره', 'اره', 'بلی',
            'من', 'تو', 'ما', 'شما', 'او', 'اون', 'ایشان',
            'مال', 'متعلق', 'مربوط', 'درباره', 'راجب', 'راجع',
            'باید', 'بایست', 'باش', 'نباید',
            'کن', 'کنم', 'کنی', 'کنید', 'کنند', 'کنن',
            'شود', 'شوم', 'شوی', 'شوند', 'شدم', 'شدی', 'شدند',
            'توی', 'تو', 'داخل', 'بین', 'میان', 'وسط',
            'روی', 'زیر', 'کنار', 'پشت', 'جلو', 'بالا', 'پایین',
            'الان', 'حالا', 'اکنون', 'فعلا', 'فعلاً', 'هنوز',
            'دیگه', 'دیگر', 'هم', 'نیز', 'همچنین', 'علاوه'
        }
        
        words = query.split()
        keywords = [w for w in words if w not in stopwords and len(w) > 2]
        
        return keywords if keywords else [query]
    

