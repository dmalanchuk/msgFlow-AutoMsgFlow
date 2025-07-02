CONDITIONS_METADATA = {
    "contains_word": {
        "description": "Перевіряє, чи містить текст певне слово",
        "params": {
            "word": {
                "type": "string",
                "description": "Слово, яке потрібно знайти у тексті"
            }
        }
    },
    "starts_with": {
        "description": "Перевіряє, чи починається текст з певного префікса",
        "params": {
            "prefix": {
                "type": "string",
                "description": "Префікс, з якого повинен починатися текст"
            }
        }
    },
    "equals": {
        "description": "Перевіряє, чи текст дорівнює заданому значенню",
        "params": {
            "value": {
                "type": "string",
                "description": "Значення, з яким порівнюється текст"
            }
        }
    }
}

ACTIONS_METADATA = {
    "send_message": {
        "description": "Надіслати повідомлення у месенджер",
        "params": {
            "chat_id": {
                "type": "integer",
                "description": "Ідентифікатор чату, куди надсилати"
            },
            "text": {
                "type": "string",
                "description": "Текст повідомлення"
            }
        }
    },
    "forward": {
        "description": "Переслати повідомлення іншому користувачу",
        "params": {
            "to_chat_id": {
                "type": "integer",
                "description": "Ідентифікатор користувача або чату для пересилки"
            }
        }
    },
    "notion_record": {
        "description": "Записати дані у базу Notion",
        "params": {
            "database_id": {
                "type": "string",
                "description": "Ідентифікатор бази даних Notion"
            },
            "properties": {
                "type": "object",
                "description": "Властивості сторінки Notion"
            }
        }
    }
}
