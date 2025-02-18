from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Получение полного пути к файлу скрипта
file_path = os.path.realpath(__file__)
# Получение директории, в которой находится файл скрипта
script_dir = os.path.dirname(file_path)

def decrypt_file(key_hex: str, input_file: str, output_file: str):
    # Преобразование ключа из HEX-строки в байты
    key = bytes.fromhex(key_hex)
    
    # IV из 16 нулевых байтов
    iv = b'\x00' * 16
    
    # Чтение зашифрованных данных
    with open(input_file, 'rb') as f:
        encrypted_data = f.read()
    
    # Инициализация шифра
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    
    # Дешифровка данных
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    
    # Пропуск первых 16 байт
    result_data = decrypted_data[16:]
    
    # Запись результата
    with open(output_file, 'wb') as f:
        f.write(result_data)

# Пример использования
KEY = "babb4a9f774ab853c96c2d653dfe544a"
CONFIG_JSON = os.path.join(script_dir, "credentials-config.json")
OUTPUT_FILE = os.path.join(script_dir, "ass.txt")

decrypt_file(KEY, CONFIG_JSON, OUTPUT_FILE)
