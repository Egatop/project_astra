import time

def check_compliance(rules, processes_df):
    current_time = time.time()
    violations = []

    for rule in rules:
        proc_name = rule['process_name'].lower()
        condition = rule['condition']
        
        matching = processes_df[processes_df['name'] == proc_name]
        
        # Условие: процесс ДОЛЖЕН быть запущен
        if condition == 'running':
            if matching.empty:
                violations.append({
                    'rule': rule['name'],
                    'process': proc_name,
                    'issue': 'Процесс не запущен, но должен быть'
                })
        
        # Условие: процесс НЕ ДОЛЖЕН быть запущен
        elif condition == 'not_running':
            if not matching.empty:
                violations.append({
                    'rule': rule['name'],
                    'process': proc_name,
                    'issue': f'Запрещённый процесс обнаружен.'
                })
        # УСЛОВИЕ: процесс МОЖЕТ быть запущен, но если запущен - не дольше N секунд
        elif condition == 'max_time_if_running':
            if not matching.empty:  # проверяем только если процесс запущен
                for _, proc in matching.iterrows():
                    create_time = proc['create_time']
                    if create_time:
                        elapsed = current_time - create_time
                        if elapsed > rule['max_seconds']:
                            violations.append({
                                'rule': rule['name'],
                                'process': proc_name,
                                'issue': f'Превышено время работы: {elapsed:.0f} сек., максимум {rule["max_seconds"]} сек.'
                            })
        # Условие по умолчанию
        else:
            violations.append({
                'rule': rule['name'],
                'process': proc_name,
                'issue': f'Неизвестный тип условия: {condition}'
            })
    
    return violations
