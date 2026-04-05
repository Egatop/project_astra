import os
import json
from modules.check import check_compliance
from modules.get_process import get_processes_info, normalize_processes
from modules.report import generate_report
from modules.threat_analyzer import analyze_violation

def load_rules(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    # Загружаем правила
    rules_path = 'rules/rules_v2.json'
    try:
        rules = load_rules(rules_path)
        print('Правила успешно загружены.')
    except FileNotFoundError:
        print(f'Ошибка: не найден файл правил {rules_path}')
        return
    except json.JSONDecodeError:
        print('Ошибка: файл правил повреждён')
        return

    #  Получаем и нормализуем процессы
    processes = get_processes_info()
    if not processes:
        print('Не удалось получить список процессов.')
        return
    df_processes = normalize_processes(processes)
    print(f'Получено процессов: {len(df_processes)}')

    #  Базовая проверка
    violations = check_compliance(rules, df_processes)

    #  Получаем имя пользователя
    try:
        current_user = os.getlogin()
    except:
        current_user = 'unknown'

    # Обогащаем каждое нарушение через конструктор
    enhanced_violations = []
    for v in violations:
        # Находим правило по имени (простой цикл)
        found_rule = None
        for r in rules:
            if r['name'] == v['rule']:
                found_rule = r
                break
        if found_rule:
            analysis = analyze_violation(v, found_rule, current_user)
            v['is_threat'] = analysis['is_threat']
            v['is_false_positive'] = analysis['is_false_positive']
            v['threat_reason'] = analysis['threat_reason']
        else:
            v['is_threat'] = False
            v['is_false_positive'] = False
            v['threat_reason'] = 'Правило не найдено'
        enhanced_violations.append(v)

   
    report_file = generate_report(enhanced_violations, 'v2', len(rules))

    #  Вывод в консоль
  
    print('РЕЗУЛЬТАТЫ ПРОВЕРКИ (с анализом угроз):')

    print(f'Правил: {len(rules)}')
    print(f'Нарушений: {len(enhanced_violations)}')
    print(f'Подробный отчёт: {report_file}')

    threats = [v for v in enhanced_violations if v.get('is_threat')]
    false_positives = [v for v in enhanced_violations if v.get('is_false_positive')]
    if threats:
        print(f'\nУГРОЗЫ ({len(threats)}):')
        for t in threats:
            print(f'  - {t["process"]} : {t.get("threat_reason")}')
    if false_positives:
        print(f'\nЛОЖНЫЕ СРАБАТЫВАНИЯ ({len(false_positives)}):')
        for fp in false_positives:
            print(f'  - {fp["process"]} : {fp.get("threat_reason")}')


if __name__ == '__main__':
    main()