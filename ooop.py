from tabulate import tabulate


class Table:
    def __init__(self):
        self.columns = ["Марка", "Модель", "Год выпуска", "Гос.номер", "Цвет"]
        self.table = []

    def display_table(self):
        if self.table:
            table_with_indices = [{"#": i, **row} for i, row in enumerate(self.table, start=1)]
            print(tabulate(table_with_indices, headers="keys", tablefmt="grid"))
        else:
            print("Таблица пуста")

    def load_table(self, file_name="cars", extension=".txt"):
        full_path = f"{file_name}{extension}"
        try:
            with open(full_path, 'r', encoding='utf-8') as file:
                headers = file.readline().strip().split(",")
                self.columns = headers
                self.table.clear()
                for line in file:
                    records = line.strip().split("|")
                    row = dict(zip(headers, records))
                    self.table.extend([row])
                print(f"Таблица успешно загружена из файла: {full_path}")
        except FileNotFoundError:
            print(f"Указанный файл {full_path} не существует")
        except Exception as e:
            print(f"При обработке файла произошла ошибка: {e}")

    def save_table(self, file_name):
        if not self.table:
            print("Таблица пуста.Нечего сохранять.")
            return
        if not file_name.endswith(".txt"):
            file_name += ".txt"
        full_path = file_name
        with open(full_path, 'w', encoding='utf-8') as file:
            header_line = ",".join(self.columns)
            file.write(header_line + "\n")
            for row in self.table:
                values = [str(row[column]) for column in self.columns]
                file.write("|".join(values) + "\n")
            print(f"Таблица успешно сохранена в файл: {full_path}")


class Car(Table):
    def __init__(self):
        super().__init__()


class Features(Table):
    def __init__(self):
        super().__init__()

    def add_row(self):
        new_row = {}
        for column in self.columns:
            if column == "Марка":
                while True:
                    marka = input("Введите Марку: ").upper()
                    if marka:
                        new_row[column] = marka
                        break
            elif column == "Модель":
                while True:
                    model = input("Введите Модель: ").upper()
                    if model:
                        new_row[column] = model
                        break
            elif column == "Цвет":
                while True:
                    tsvet = input("Введите Цвет: ").upper()
                    if tsvet:
                        new_row[column] = tsvet
                        break
            elif column == "Год выпуска":
                age = input("Введите Год выпуска: ")
                new_row[column] = age
                           
            elif column == "Гос.номер":
                number = input(f"Введите {column}: ").upper()
                new_row[column] = number
            else:
                value = input(f"Введите {column}: ").upper()
                new_row[column] = value
        self.table += [new_row]
        print("Строка успешно добавлена")
        self.save_table("cars.txt")
        print("Изменения сохранены")

    def delete_row(self, index):
        if not self.table:
            print("Таблица пуста. Невозможно удалить строки.")
            return
        try:
            index = int(index)
            if 1 <= index <= len(self.table):
                del self.table[index - 1]
                print(f"Строка под номером {index} удалена.")
            else:
                print("Такого номера строки нет в таблице.")
        except ValueError:
            print("Номер строки должен быть числом!")
            self.save_table("cars.txt")
            print("Изменения сохранены")

    def update_row(self):
        if not self.table:
            print("Таблица пуста. Невозможно изменить строки.")
            return
        while True:
            try:
                row_index = int(input("Введите номер строки для изменения: ")) - 1
                column_name = input("Введите имя столбца для изменения: ")
                if column_name not in self.columns:
                    print("Такого столбца не существует, попробуйте снова.")
                    continue
                new_value = input("Введите новое значение: ")
                try:
                    self.table[row_index][column_name] = new_value
                    break
                except IndexError:
                    print("Введён неверный номер строки, попробуйте снова.")
            except ValueError:
                print("Номер строки должен быть числом, попробуйте снова.")
        self.save_table("cars.txt")
        print("Изменения сохранены")

    def search(self):
        if not self.table:
            print("Таблица пуста. Нечего искать.")
            return

        search_query = input("Введите параметр для поиска: ").upper()
        found = False

        search_results = []

        for i, row in enumerate(self.table, start=1):
            found_in_row = any(search_query.lower() in str(value).lower() for value in row.values())
            if found_in_row:
                if not found:
                    print("Результаты поиска:\n")
                    found = True
                print(f"Найдено в строке #{i}:")
                print(tabulate([row], headers="keys", tablefmt="double_grid"))
                print()
                search_results.append({"#": i, **row})
        if not found:
            print(f"Нет совпадений для запроса <{search_query}>.")
        else:
            print("Результаты в виде таблицы:")
            print(tabulate(search_results, headers="keys", tablefmt="double_grid"))


car_data = Car()
features = Features()

while True:
    print("\nМеню:")
    print("1. Добавить строку")
    print("2. Удалить строку")
    print("3. Внести изменения")
    print("4. Поиск")
    print("5. Показать таблицу")
    print("6. Сохранить таблицу")
    print("7. Загрузить таблицу")
    print("8. Выйти")

    choice = input("Выберите действие: ")

    if choice == "1":
        features.add_row()
    elif choice == "2":
        row_to_delete = input("Введите номер строки для удаления: ")
        features.delete_row(row_to_delete)
    elif choice == "3":
        features.update_row()
    elif choice == "4":
        features.search()
    elif choice == "5":
        features.display_table()
    elif choice == "6":
        file_name = input("Введите название файла для сохранения (без расширения, например, table): ")
        features.save_table(file_name)
    elif choice == "7":
        load_auto = input("Загрузить автоматически (1) или вручную (2)?: ")
        if load_auto.strip().lower() in ["а", "авто", "1"]:
            features.load_table()
        elif load_auto.strip().lower() in ["б", "вручную", "2"]:
            file_name = input("Введите название файла для загрузки (без расширения, например, table): ")
            features.load_table(file_name)
        else:
            print("Неверный выбор.")
    elif choice == "8":
        save_exit = input("Сохраниться перед выходом?: ")
        if save_exit.lower() in ['yes', '1', 'да']:
            file_name = input("Введите название файла для сохранения (без расширения, например, table): ")
            features.save_table(file_name)
            break
        elif save_exit.lower() in ['no', '2', 'нет']:
            break
        else:
            print('Неверный выбор')
            break
    else:
        print("Неверный выбор. Попробуйте снова.")
