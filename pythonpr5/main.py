import os
import multiprocessing
import time
import psutil
import argparse

def caesar_cipher(text, key, mode='encrypt'):
    result = ''
    for char in text:
        if char.isalpha():
            start = ord('a') if char.islower() else ord('A')
            shifted_char = chr((ord(char) - start + key if mode == 'encrypt' else ord(char) - start - key) % 26 + start)
        elif char.isdigit():
            shifted_char = str((int(char) + key if mode == 'encrypt' else int(char) - key) % 10)
        else:
            shifted_char = char
        result += shifted_char
    return result

def process_chunk(chunk, key, mode, chunk_number, queue):
    try:
        encrypted_chunk = caesar_cipher(chunk, key, mode)
        queue.put((chunk_number, encrypted_chunk))
    except Exception:
        queue.put((chunk_number, None))

def writer_process(queue, output_file, total_chunks):
    results = [None] * total_chunks
    completed_chunks = 0
    with open(output_file, 'w', encoding='utf-8') as outfile:
        while True:
            item = queue.get()
            if item is None:
                break
            chunk_number, chunk_data = item
            if chunk_data is None:
                results[chunk_number] = ''
            else:
                results[chunk_number] = chunk_data
            while results and results[0] is not None:
                outfile.write(results.pop(0))
                results.append(None)
                completed_chunks += 1
    print("Запись завершена.")

def encrypt_decrypt_file(input_file, output_file, key, mode, num_processes):
    chunks = []
    with open(input_file, 'rb') as infile:
        while True:
            chunk = infile.read(1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)

    total_chunks = len(chunks)
    queue = multiprocessing.Queue()

    writer = multiprocessing.Process(target=writer_process, args=(queue, output_file, total_chunks))
    writer.start()

    processes = []

    for idx, chunk in enumerate(chunks):
        p = multiprocessing.Process(target=process_chunk, args=(chunk.decode('utf-8', errors='ignore'), key, mode, idx, queue))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    for _ in range(1):
        queue.put(None)

    writer.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encrypt or decrypt a file using multiprocessing.")
    parser.add_argument("--input_file", "-i", required=True, help="Path to the input file.")
    parser.add_argument("--output_file", "-o", required=True, help="Path to the output file.")
    parser.add_argument("--key", "-k", type=int, required=True, help="Encryption/decryption key (integer).")
    parser.add_argument("--mode", "-m", choices=['encrypt', 'decrypt'], required=True, help="Mode: encrypt или decrypt.")
    parser.add_argument("-p", "--processes", type=int, help="Количество процессов (по умолчанию адаптивно).")
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    key = args.key
    mode = args.mode

    if args.processes:
        num_processes = min(args.processes, multiprocessing.cpu_count())
    else:
        def get_optimal_processes():
            cpu_load = psutil.cpu_percent()
            cpu_count = multiprocessing.cpu_count()
            if cpu_load < 25:
                return cpu_count
            elif cpu_load < 75:
                return cpu_count // 2
            else:
                return 1
        num_processes = get_optimal_processes()

    print(f"Используется {num_processes} процессов.")

    start_time = time.time()
    encrypt_decrypt_file(input_file, output_file, key, mode, num_processes)
    end_time = time.time()

    print(f"Завершено за {end_time - start_time:.2f} секунд.")
