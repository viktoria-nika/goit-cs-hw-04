# Завдання 1 

# Реалізація багатопотокового підходу до обробки файлів. 


import threading
import os
import time

# Функція для пошуку ключових слів у файлі
def search_in_file(file_path, keywords, result_dict):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    if keyword not in result_dict:
                        result_dict[keyword] = []
                    result_dict[keyword].append(file_path)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

# Функція для обробки файлів багатьма потоками
def search_in_files_threading(files, keywords):
    result_dict = {}
    threads = []
    
    # Розподіляємо файли по потоках
    files_per_thread = len(files) // 4  # Для 4 потоків
    for i in range(4):
        start_index = i * files_per_thread
        end_index = (i + 1) * files_per_thread if i < 3 else len(files)
        thread_files = files[start_index:end_index]
        
        thread = threading.Thread(target=process_files, args=(thread_files, keywords, result_dict))
        threads.append(thread)
        thread.start()
    
    # Чекаємо на завершення всіх потоків
    for thread in threads:
        thread.join()
    
    return result_dict

# Функція для обробки файлів в одному потоці
def process_files(files, keywords, result_dict):
    for file_path in files:
        search_in_file(file_path, keywords, result_dict)

# Головна частина програми
def main_threading():
    file_paths = ["file1.txt", "file2.txt", "file3.txt"]

    keywords = ["модель", "поток", "мова"]
    
    start_time = time.time()
    result_dict = search_in_files_threading(file_paths, keywords)
    end_time = time.time()
    
    print(f"Results: {result_dict}")
    print(f"Threading took {end_time - start_time} seconds.")

if __name__ == "__main__":
    main_threading()
