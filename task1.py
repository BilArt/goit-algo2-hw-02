from typing import List, Dict
from dataclasses import dataclass


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """
    # Перетворюємо вхідні дані у список об'єктів PrintJob
    jobs = [PrintJob(**job) for job in print_jobs]
    
    # Сортуємо завдання за пріоритетом (1 - найвищий) та часом друку (за зростанням)
    jobs.sort(key=lambda job: (job.priority, job.print_time))

    print_order = []  # список для збереження порядку друку
    total_time = 0  # загальний час друку
    current_volume = 0  # поточний об'єм завдань у черзі
    current_batch = []  # список поточних завдань для друку
    max_items = constraints["max_items"]  # максимальна кількість моделей на друк
    max_volume = constraints["max_volume"]  # максимальний об'єм друку за один раз

    for job in jobs:
        # Перевіряємо, чи можна додати модель до поточної черги
        if (len(current_batch) < max_items and
                current_volume + job.volume <= max_volume):
            current_batch.append(job)
            current_volume += job.volume
        else:
            # Якщо обмеження перевищено, друкуємо поточну партію
            total_time += max(j.print_time for j in current_batch)
            print_order.extend(j.id for j in current_batch)
            # Починаємо нову партію
            current_batch = [job]
            current_volume = job.volume

    # Додаємо останню партію до загального підрахунку
    if current_batch:
        total_time += max(j.print_time for j in current_batch)
        print_order.extend(j.id for j in current_batch)

    return {
        "print_order": print_order,
        "total_time": total_time
    }


# Тестування
def test_printing_optimization():
    # Тест 1: Завдання з однаковим пріоритетом
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Завдання з різними пріоритетами
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},  # дипломна
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}  # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень принтера
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")


if __name__ == "__main__":
    test_printing_optimization()
