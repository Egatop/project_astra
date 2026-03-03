import psutil
import pandas as pd
def get_processes_info():
    #получаес список процессов
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'create_time']):
        try:
            pinfo = proc.info
            processes.append({
                'pid': pinfo['pid'],
                'name': pinfo['name'],
                'create_time': pinfo['create_time']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    return processes
#приводим их к нормальному виду DataFrame
def normalize_processes(processes):

    df = pd.DataFrame(processes)
    if not df.empty:
        df['name'] = df['name'].str.lower()
    return df