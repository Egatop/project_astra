import json

from modules.check import check_compliance
from modules.get_process import get_processes_info, normalize_processes
from modules.report import generate_report


def load_rules(filepath):
    """Загружает правила из JSON-файла."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
def main():

    rules_path = 'rules/rules_v1.json'
    
    # Загружаем правила
    try:
        rules = load_rules(rules_path)
        print('Правила успешно загружены.')
    except FileNotFoundError:
        print(f' Ошибка: не найден файл правил {rules_path}')
        return
    except json.JSONDecodeError:
        print('Ошибка: файл правил повреждён (неверный формат JSON)')
        return
    
    # Получаем процессы
    processes = get_processes_info()
    if not processes:
        print('Не удалось получить список процессов. Проверьте права доступа.')
        return
    
    df_processes = normalize_processes(processes)

    
    # Проверяем соответствие

    violations = check_compliance(rules, df_processes)
    
    # Сохраняем отчёт
    report_file = generate_report(violations, 'v1', len(rules))
    
    # Выводим краткую сводку в консоль
    print('\nРЕЗУЛЬТАТЫ ПРОВЕРКИ:')
    print(f' Правил: {len(rules)}')
    print(f' Нарушений: {len(violations)}')
    print(f'\n📄 Подробный отчёт: {report_file}')
    


    # Пример структуры таблицы:
    """
    CREATE TABLE IF NOT EXISTS checks (
        id INTEGER PRIMARY KEY,
        check_time TEXT,
        rules_version TEXT,
        rules_count INTEGER,
        violations_count INTEGER,
        report_path TEXT
    );
    """

if __name__ == '__main__':
    main()