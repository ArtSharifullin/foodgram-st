#!/bin/bash

# Проверка наличия аргумента с путём к helm-директории
if [ $# -lt 1 ]; then
    echo "Использование: $0 <путь_к_helm_директории> [файл_вывода]"
    exit 1
fi

HELM_DIR="$1"
OUTPUT_FILE="${2:-helm_dump.txt}"

# Проверка существования директории
if [ ! -d "$HELM_DIR" ]; then
    echo "Ошибка: директория '$HELM_DIR' не существует"
    exit 1
fi

# Очистка/создание файла вывода
> "$OUTPUT_FILE"

# Функция вывода содержимого файла (в файл)
print_file() {
    local file="$1"
    echo "=== $file ===" >> "$OUTPUT_FILE"
    if [ ! -s "$file" ]; then
        echo "[Empty file]" >> "$OUTPUT_FILE"
    else
        cat "$file" >> "$OUTPUT_FILE"
    fi
    echo "" >> "$OUTPUT_FILE"
}

# Обработка всех файлов (включая пустые)
find "$HELM_DIR" -type f -print0 | while IFS= read -r -d '' file; do
    print_file "$file"
done

# Обработка пустых директорий
find "$HELM_DIR" -type d -empty -print0 | while IFS= read -r -d '' dir; do
    echo "=== $dir ===" >> "$OUTPUT_FILE"
    echo "[Empty directory]" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
done

echo "Результат сохранён в файл: $OUTPUT_FILE"