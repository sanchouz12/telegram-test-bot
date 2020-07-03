from telegram import InlineKeyboardButton, InlineKeyboardMarkup

button_list = [
    InlineKeyboardButton("col1", callback_data = "callback_col1"),
    InlineKeyboardButton("col2", callback_data = "callback_col2"),
    InlineKeyboardButton("row2", callback_data = "callback_row2")
]

def _build_menu(buttons, n_cols, header_buttons = None, footer_buttons = None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]

    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])

    return menu

def get_markup():
    return InlineKeyboardMarkup(_build_menu(button_list, n_cols = 2))
