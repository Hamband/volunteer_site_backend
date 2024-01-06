import os

db_uri = os.environ.get("DB")
path_prefix = os.environ.get("PATH_PREFIX") or ""
api_keys = (os.environ.get("API_KEYS") or "").split(",")
show_docs = (os.environ.get("SHOW_DOCS") or "1") != "0"
no_http = (os.environ.get("NO_HTTP") or "1") != "0"
version = "1"
api_title = "Hamband Volunteer Data API"
api_summary = ""
api_description = """
All requests must have a path parameter api_key containing your API key. Requests with invalid API keys would get a 403 response.

A 200 response code will be returned only upon success.

A 422 code will be returned if the request data is invalid, and additional info will be available in the response body, according to PyDantic docs.
"""

completion_defaults = {
    "contacts/type": ["email", "phone", "telegram"],
    "degrees/major": ["ریاضی", "علوم کامپیوتر", "مهندسی کامپیوتر", "فیزیک", "مهندسی برق"],
    "degrees/uni": ["دانشگاه صنعتی شریف", "دانشگاه تهران", "دانشگاه صنعتی امیرکبیر", "دانشگاه شهید بهشتی", "پژوهشگاه دانش‌های بنیادی", "دانشگاه صنعتی اصفهان", "دانشگاه شیراز"],
    "fields": ["احتمال", "جبر", "آنالیز", "منطق", "سیستم‌های دینامیکی", "ترکیبیات", "الگوریتم", "نظریه محاسبه", "رمزنگاری", "نظریه اطلاعات"]
}
