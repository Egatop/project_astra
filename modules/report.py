import datetime
import os

def generate_report(violations, rules_version, rules_count):
    #Сохраняет отчёт в текстовый файл
    os.makedirs('reports', exist_ok=True)
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'reports/report_{timestamp}.txt'
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('=' * 60 + '\n')
        f.write('Отчёт о соответствии политикам \n')
        f.write('=' * 60 + '\n')
        f.write(f'Дата и время: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
        f.write(f'Версия правил: {rules_version}\n')
        f.write(f'Всего проверено правил: {rules_count}\n')
        f.write(f'Нарушений: {len(violations)}\n')
        f.write('-' * 60 + '\n')
        
        if violations:
            f.write('Список нарушений:\n')
            for idx, v in enumerate(violations, 1):
                f.write(f'{idx}. Правило: "{v["rule"]}"\n')
                f.write(f'   Процесс: {v["process"]}\n')
                f.write(f'   Проблема: {v["issue"]}\n')
                f.write('\n')
        else:
            f.write('Нарушений не обнаружено. Все правила соблюдены.\n')
    
    return filename