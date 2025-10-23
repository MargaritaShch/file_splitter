import csv

# имя исходного файла
input_file = 'files/v2_write.csv'

# создаём два выходных файла
x5id_file = 'write_x5id.csv'
mobile_file = 'write_mobilePhone.csv'

# читаем исходный CSV
with open(input_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')

    with open(x5id_file, 'w', newline='', encoding='utf-8') as x5, \
         open(mobile_file, 'w', newline='', encoding='utf-8') as mob:

        x5_writer = csv.writer(x5)
        mob_writer = csv.writer(mob)

        # каждая строка — список вроде ['12345', '79001112233']
        for row in reader:
            if len(row) >= 2:  # чтобы пропустить пустые строки
                x5_writer.writerow([row[0]])  # первый столбец
                mob_writer.writerow([row[1]])  # второй столбец

print("delete_x5id.csv и delete_mobilePhone.csv")
