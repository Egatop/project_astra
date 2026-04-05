import json
import os

INCIDENTS_FILE = 'data/incidents.json'

def load_incidents():
    """Загружает историю инцидентов из JSON-файла."""
    if not os.path.exists(INCIDENTS_FILE):
        return []
    with open(INCIDENTS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_unique_hosts_count(process_name, incidents, is_threat=True):
    """
    Считает, сколько уникальных хостов зафиксировали этот процесс
    как угрозу (is_threat=True) или как ложное срабатывание (is_threat=False).
    """
    hosts = set()
    process_name_lower = process_name.lower()
    for inc in incidents:
        # Проверяем, есть ли поле 'process', и приводим его к нижнему регистру
        inc_process = inc.get('process', '')
        if inc_process.lower() == process_name_lower:
            if is_threat and inc.get('is_threat', False):
                hosts.add(inc.get('host', 'unknown'))
            elif not is_threat and inc.get('is_false_positive', False):
                hosts.add(inc.get('host', 'unknown'))
    return len(hosts)

def was_false_positive(process_name, incidents):
    """Проверяет, был ли процесс когда-либо помечен как ложное срабатывание."""
    process_name_lower = process_name.lower()
    for inc in incidents:
        inc_process = inc.get('process', '')
        if inc_process.lower() == process_name_lower and inc.get('is_false_positive', False):
            return True
    return False

def analyze_violation(violation, rule, current_user):
    """
    Конструктор политик: принимает нарушение, правило и пользователя.
    Возвращает словарь с полями is_threat, is_false_positive, threat_reason.
    """
    process_name = violation['process']
    incidents = load_incidents()

    # 1. Исключение по пользователю
    exception_users = rule.get('exception_users', [])
    if current_user and current_user in exception_users:
        return {
            'is_threat': False,
            'is_false_positive': True,
            'threat_reason': f'Пользователь {current_user} в списке исключений правила'
        }

    # 2. Угроза по умолчанию (категория/тип правила)
    if rule.get('is_threat_by_default', False):
        category = rule.get('category', 'unknown')
        rule_type = rule.get('rule_type', 'unknown')
        return {
            'is_threat': True,
            'is_false_positive': False,
            'threat_reason': f'Правило "{rule["name"]}" (категория: {category}, тип: {rule_type}) помечено как угроза по умолчанию'
        }

    # 3. История ложных срабатываний
    if was_false_positive(process_name, incidents):
        return {
            'is_threat': False,
            'is_false_positive': True,
            'threat_reason': f'Процесс {process_name} ранее был помечен как ложное срабатывание (история инцидентов)'
        }

    # 4. Статистика угроз в других системах
    threat_count = get_unique_hosts_count(process_name, incidents, is_threat=True)
    threshold = rule.get('threshold_count', 1)
    if threat_count >= threshold:
        return {
            'is_threat': True,
            'is_false_positive': False,
            'threat_reason': f'Процесс {process_name} отмечен как угроза в {threat_count} системах (порог {threshold})'
        }

    # 5. Всё остальное – просто нарушение
    return {
        'is_threat': False,
        'is_false_positive': False,
        'threat_reason': 'Недостаточно оснований считать угрозой (нет истории, нет флага по умолчанию)'
    }