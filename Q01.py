import random
import copy
import matplotlib.pyplot as plt

class Processo:
    def __init__(self, pid, arrival, burst):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.remaining = burst
        self.start_time = None
        self.finish_time = None

# Cálculo de métricas: espera média, tempo médio de retorno e vazão
def calcular_metricas(processos, total_time):
    n = len(processos)
    tempos_espera = [(p.finish_time - p.arrival - p.burst) for p in processos]
    tempos_retorno = [(p.finish_time - p.arrival) for p in processos]
    avg_wait = sum(tempos_espera) / n
    avg_return = sum(tempos_retorno) / n
    vazao = n / total_time
    return avg_wait, avg_return, vazao

# FCFS (First Come, First Served) - não pré-emptivo
def escalonamento_fcfs(processos):
    tempo = 0
    seq = []
    proc_list = sorted(processos, key=lambda p: p.arrival)
    for p in proc_list:
        if tempo < p.arrival:
            tempo = p.arrival
        p.start_time = tempo
        seq.append((p.pid, tempo, tempo + p.burst))
        tempo += p.burst + 1
        p.finish_time = tempo - 1
    return seq, calcular_metricas(proc_list, tempo)

# SJF (Shortest Job First) - não pré-emptivo
def escalonamento_sjf(processos):
    tempo = 0
    seq = []
    lista = copy.deepcopy(processos)
    prontos = []
    concluidos = []
    while lista or prontos:
        for p in lista[:]:
            if p.arrival <= tempo:
                prontos.append(p)
                lista.remove(p)
        if not prontos:
            tempo += 1
            continue
        p = min(prontos, key=lambda x: x.burst)
        prontos.remove(p)
        p.start_time = tempo
        seq.append((p.pid, tempo, tempo + p.burst))
        tempo += p.burst + 1
        p.finish_time = tempo - 1
        concluidos.append(p)
    return seq, calcular_metricas(concluidos, tempo)

# Round Robin (RR)
def escalonamento_rr(processos, quantum):
    tempo = 0
    seq = []
    fila = []
    lista = sorted(copy.deepcopy(processos), key=lambda p: p.arrival)
    concluidos = []
    while lista or fila:
        for p in lista[:]:
            if p.arrival <= tempo:
                fila.append(p)
                lista.remove(p)
        if not fila:
            tempo += 1
            continue
        p = fila.pop(0)
        if p.start_time is None:
            p.start_time = tempo
        exec_time = min(p.remaining, quantum)
        seq.append((p.pid, tempo, tempo + exec_time))
        tempo += exec_time + 1
        p.remaining -= exec_time
        for q in lista[:]:
            if q.arrival <= tempo:
                fila.append(q)
                lista.remove(q)
        if p.remaining > 0:
            fila.append(p)
        else:
            p.finish_time = tempo - 1
            concluidos.append(p)
    return seq, calcular_metricas(concluidos, tempo)

    
def main():
    random.seed(42)
    N = 100

    arrivals = random.sample(range(0, 100), N)
    bursts = [random.randint(1, 30) for _ in range(N)]
    processos = [Processo(pid=i+1, arrival=arrivals[i], burst=bursts[i]) for i in range(N)]

    quantums = [2, 4, 6]

    resultados = {}
    _, met_fcfs = escalonamento_fcfs(copy.deepcopy(processos))
    resultados['FCFS'] = met_fcfs
    _, met_sjf = escalonamento_sjf(copy.deepcopy(processos))
    resultados['SJF'] = met_sjf
    for q in quantums:
        label = f'RR-{q}'
        _, met_rr = escalonamento_rr(copy.deepcopy(processos), q)
        resultados[label] = met_rr

    algoritmos = list(resultados.keys())
    espera = [resultados[a][0] for a in algoritmos]
    retorno = [resultados[a][1] for a in algoritmos]
    vazao = [resultados[a][2] for a in algoritmos]
    x = range(len(algoritmos))
    width = 0.25

    plt.figure()
    plt.bar([i - width for i in x], espera, width)
    plt.xticks(x, algoritmos)
    plt.title('Tempo Médio de Espera')
    plt.ylabel('Tempo')
    plt.xlabel('Algoritmos')

    plt.figure()
    plt.bar(x, retorno, width)
    plt.xticks(x, algoritmos)
    plt.title('Tempo Médio de Retorno')
    plt.ylabel('Tempo')
    plt.xlabel('Algoritmos')

    plt.figure()
    plt.bar([i + width for i in x], vazao, width)
    plt.xticks(x, algoritmos)
    plt.title('Vazão (processos por unidade de tempo)')
    plt.ylabel('Vazão')
    plt.xlabel('Algoritmos')

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
