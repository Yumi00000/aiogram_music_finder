from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def paginate_response(items: list, page: int = 0, page_size: int = 5):
    start = page * page_size
    end = start + page_size
    page_items = items[start:end]

    response = "📜 *Your recognition history:*\n\n"
    for i, entry in enumerate(page_items, start=start+1):
        response += entry + "\n\n"

    buttons = []
    if page > 0:
        buttons.append(InlineKeyboardButton(text="⬅️ Prev", callback_data=f"history:{page-1}"))
    if end < len(items):
        buttons.append(InlineKeyboardButton(text="➡️ Next", callback_data=f"history:{page+1}"))

    kb = InlineKeyboardMarkup(row_width=2, inline_keyboard=[])
    if buttons:
        kb.inline_keyboard.append(buttons)

    return response, kb