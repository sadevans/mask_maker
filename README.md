# Редактор масок

GUI для редактирования бинарных масок после первичной разметки. Фактически - минимальный функционал Paint из Windows.

# Установка зависимостей
Сначала создайте вирутальную среду:

```bash
python -m venv venv
```

После этого активируйте ее:
```bash
source venv/bin/activate
```

Установите зависимости из файла `requirements.txt`
```bash
pip install -r requirements.txt
```
# Запуск
Для использования GUI необходимо запустить файл `run.py`
```bash
python run.py
```

Теперь можно пользоваться GUI и редактировать маски.

# Этапы работы
В окне `Select Folders` выберите пути к папкам, которые содержат изображения после шумоподавления и первичные бинарные маски.
![image](https://github.com/sadevans/mask_maker/assets/82286355/f8681791-2b00-43bc-843a-9ed393c41d1a)

После этого нажмите `Submit paths`.

Если не для всех изображений есть пара (чистое изображение или маска), на экране появится окно с общим количеством изображений и количеством изображений без масок. Вы можете либо продолжить работу только с парными изображениями, либо вернуться и выбрать пути заново.

