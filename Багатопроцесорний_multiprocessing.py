# Завдання 2 

# Реалізація багатопроцесорного підходу до обробки файлів. 

import multiprocessing
import os
import time

# Функція для пошуку ключових слів у файлі
def search_in_file(file_path, keywords, result_queue):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            result = {}
            for keyword in keywords:
                if keyword in content:
                    result[keyword] = file_path
            if result:
                result_queue.put(result)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

# Функція для обробки файлів багатьма процесами
def search_in_files_multiprocessing(files, keywords):
    result_queue = multiprocessing.Queue()
    processes = []
    
    # Розподіляємо файли по процесах
    files_per_process = len(files) // 4  # Для 4 процесів
    for i in range(4):
        start_index = i * files_per_process
        end_index = (i + 1) * files_per_process if i < 3 else len(files)
        process_files = files[start_index:end_index]
        
        process = multiprocessing.Process(target=process_files_func, args=(process_files, keywords, result_queue))
        processes.append(process)
        process.start()
    
    # Чекаємо на завершення всіх процесів
    for process in processes:
        process.join()
    
    # Збираємо всі результати з черги
    result_dict = {}
    while not result_queue.empty():
        result = result_queue.get()
        for keyword, file_path in result.items():
            if keyword not in result_dict:
                result_dict[keyword] = []
            result_dict[keyword].append(file_path)
    
    return result_dict

# Функція для обробки файлів в одному процесі
def process_files_func(files, keywords, result_queue):
    for file_path in files:
        search_in_file(file_path, keywords, result_queue)

# Головна частина програми
def main_multiprocessing():
    file_paths = ["file1.txt", "file2.txt", "file3.txt"] # Файли для пошуку

    keywords = ["модель", "поток", "мова"] # Ключові слова для пошуку
    
    
    start_time = time.time()
    result_dict = search_in_files_multiprocessing(file_paths, keywords)
    end_time = time.time()
    
    print(f"Results: {result_dict}")
    print(f"Multiprocessing took {end_time - start_time} seconds.")

if __name__ == "__main__":
    main_multiprocessing()
