with open('settings.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    
lines = [line.strip() for line in lines]
# lines = [line for line in lines if not line.startswith('#')]
# lines = [line.strip() for line in lines]

keys = []
for line in lines[2:]:
    filename, key = line.split()
    keys.append((filename, key))

for filename, key in keys:
    print(f"Назва файлу: {filename}, Ключ: {key}")
        