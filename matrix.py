import random
import threading
import time
import queue
import matplotlib.pyplot as plt

def generate_matrix(rows, cols):
    return [[random.randint(1, 10) for _ in range(cols)] for _ in range(rows)]

def multiply_row_col(A, B, result, row, col, lock, output_queue):
    total = 0
    for i in range(len(A[row])):
        total += A[row][i] * B[i][col]
    with lock:
        result[row][col] = total
    output_queue.put(f"Element [{row},{col}] = {total}")

def multiply_matrices(A, B, num_threads, output_queue):
    n = len(A)
    m = len(A[0])
    k = len(B[0])
    result = [[0 for _ in range(k)] for _ in range(n)]
    lock = threading.Lock()
    threads = []

    # Створення і запуск потоків
    for row in range(n):
        for col in range(k):
            thread = threading.Thread(target=multiply_row_col, args=(A, B, result, row, col, lock, output_queue))
            threads.append(thread)
            thread.start()
            if len(threads) >= num_threads:
                for thread in threads:
                    thread.join()
                threads = []

    for thread in threads:
        thread.join()

    return result

# Генеруємо матриці A та B
n, m, k = 3, 3, 4
A = generate_matrix(n, m)
B = generate_matrix(m, k)
output_queue = queue.Queue()

# Вимірюємо час виконання при різній кількості потоків
num_threads_list = range(1, n*k + 1)
#num_threads_list = [1, 2, 4, 8]   
execution_times = []
for num_threads in num_threads_list:
    start_time = time.time()
    multiply_matrices(A, B, num_threads, output_queue)
    execution_times.append(time.time() - start_time)

# Виведення обчислених елементів
while not output_queue.empty():
    print(output_queue.get())

# Виведення матриць та результату
print("Matrix A:")
for row in A:
    print(row)

print("\nMatrix B:")
for row in B:
    print(row)

print("\nResult of Multiplication:")
result = multiply_matrices(A, B, 1, queue.Queue())  # Create a new queue for clean output
for row in result:
    print(row)

# Побудова графіка
plt.figure(figsize=(10, 6))
plt.plot(num_threads_list, execution_times, marker='o')
plt.xlabel('Number of Threads')
plt.ylabel('Execution Time (seconds)')
plt.title('Matrix Multiplication Performance vs. Number of Threads')
plt.grid(True)
plt.xticks(num_threads_list)
plt.show()
