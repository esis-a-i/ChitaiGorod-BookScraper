# ChitaiGorod-BookScraper

Scrapy spider для сбора данных о книгах с сайта Читай-город с сохранением в MongoDB и FastAPI сервисом для поиска по ISBN.

## FastAPI сервис

### Эндпоинт для поиска книг по ISBN

**URL:** `GET /search_by_isbn`

**Параметры:**
- `isbn` (string, обязательный) - ISBN код книги

### Пример запроса

```bash
curl "http://localhost:8000/search_by_isbn?isbn=978-5-9614-6362-0"
```

### Пример ответа

```json
{"title": "Дело не в генах: Почему (на самом деле) мы похожи на родителей", "author": " Оливер Джеймс", "description": "Джеймс О. Дело не в генах: Почему (на самом деле) мы похожи на родителей / Оливер Джеймс ; Пер. с англ. — М. : Альпина Паблишер, 2021. — 387 с. Во многих своих промахах и недостатках мы склонны винить наследственность. Мы не виноваты, это все гены: от ни", "price_amount": 884.0, "price_currency": "₽", "rating_value": null, "rating_count": null, "publication_year": 2017, "isbn": "978-5-9614-6362-0", "pages_cnt": 387, "publisher": "Альпина Паблишер", "book_cover": "https://content.img-gorod.ru/pim/products/images/09/24/018ede31-4214-74e9-a69c-207ef57e0924.jpg?width=304&height=438&fit=bounds", "source_url": "https://www.chitai-gorod.ru/product/delo-ne-v-genah-pochemu-na-samom-dele-my-pohozhi-na-roditeley-2597917"}
```
