"""
Schema for trainer response validation
"""
from voluptuous import Schema, Required, Optional, PREVENT_EXTRA, All, Any

valid_single_trainer= Schema(
    {
        Required("status"): "success",
        Required("data"): [{
            Required("id"): All(str, lambda s: s.isdigit()),
            Required("trainer_name"): str,
            Required("level"): All(str, lambda s: s.isdigit()),
            Required("pokemons"): [All(str, lambda s: s.isdigit())],
            Required("pokemons_alive"): [All(str, lambda s: s.isdigit())],
            Required("pokemons_in_pokeballs"): list,
            Required("get_history_battle"): All(str, lambda s: s.isdigit()),
            Required("is_premium"): bool,
            Required("premium_duration"): int,
            Required("avatar_id"): int,
            Required("city"): str,
            # Необязательные поля, которые могут появиться в ответе
            Optional("other_field"): Any(str, int, bool, None)
        }]
    },
    extra=PREVENT_EXTRA,
    required=True
)

# Схема для ответа со списком тренеров (когда trainer_id не указан)
valid_trainers_list = Schema(
    {
        "status": "success",
        "data": list,  # Список тренеров
        Optional("next_page"): bool,  # Поле пагинации
        Optional("previous_page"): bool  # Поле пагинации
    },
    extra=PREVENT_EXTRA
)

# Ответ с ошибкой
error_response = Schema(
    {
        "status": str,
        "message": str
    },
    extra=PREVENT_EXTRA
)