import datetime
import os
def generate_report(violations, rules_version, rules_count):
    os.makedirs('reports', exist_ok=True)
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'reports/report_{timestamp}.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('=' * 60 + '\n')
        f.write('ОТЧЁТ О СООТВЕТСТВИИ ПОЛИТИКАМ\n')
        f.write('=' * 60 + '\n')
        f.write(f'Дата и время: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
        f.write(f'Версия правил: {rules_version}\n')
        f.write(f'Всего проверено правил: {rules_count}\n')
        f.write(f'Нарушений: {len(violations)}\n')
        f.write('-' * 60 + '\n')
        if violations:
            # Разделяем на группы
            threats = [v for v in violations if v.get('is_threat')]
            false_positives = [v for v in violations if v.get('is_false_positive')]
            normal = [v for v in violations if not v.get('is_threat') and not v.get('is_false_positive')]
            # Угрозы
            if threats:
                f.write('\nУГРОЗЫ (требуют внимания администратора):\n')
                f.write('=' * 60 + '\n')
                for idx, v in enumerate(threats, 1):
                    f.write(f'{idx}. Правило: "{v["rule"]}"\n')
                    f.write(f'   Процесс: {v["process"]}\n')
                    f.write(f'   Проблема: {v["issue"]}\n')
                    f.write(f'   Обоснование: {v.get("threat_reason", "")}\n')
                    f.write('\n')
            # Ложные срабатывания
            if false_positives:
                f.write('\nЛОЖНЫЕ СРАБАТЫВАНИЯ (можно игнорировать):\n')
                f.write('=' * 60 + '\n')
                for idx, v in enumerate(false_positives, 1):
                    f.write(f'{idx}. Правило: "{v["rule"]}"\n')
                    f.write(f'   Процесс: {v["process"]}\n')
                    f.write(f'   Проблема: {v["issue"]}\n')
                    f.write(f'   Обоснование: {v.get("threat_reason", "")}\n')
                    f.write('\n')
            # Обычные нарушения
            if normal:
                f.write('\nОБЫЧНЫЕ НАРУШЕНИЯ (без признаков угрозы):\n')
                f.write('=' * 60 + '\n')
                for idx, v in enumerate(normal, 1):
                    f.write(f'{idx}. Правило: "{v["rule"]}"\n')
                    f.write(f'   Процесс: {v["process"]}\n')
                    f.write(f'   Проблема: {v["issue"]}\n')
                    f.write(f'   Обоснование: {v.get("threat_reason", "")}\n')
                    f.write('\n')
        else:
            f.write('\nНарушений не обнаружено. Все правила соблюдены.\n')
    return filename