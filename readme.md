# Homework_11_2

**Описание**
Домашнее задание по уроку "Декораторы" унивеситета Sky Pro.
На момент составления данного документа программа содержит 5 модулей на тему обработка данных пользователей в банковской сфере.


**Структура**

 `src\masks.py` - модуль с функциями обработки номеров карт и счетов в цифровом формате.  
 `src\widget.py` - модуль функциями обработки даты, номеров карт и счетов с названием карты и счёта.  
 `src\processing.py` - модуль с фунциями сортировки данных клиентов по заданному признаку/критерию.  
 `src\generators.py` - модуль с функциями отбора транзакций по валюте, выводу транзакций и генерации номера банковской карты.  
 `src\decorators.py` - модуль с декоратором простейшей функции.

**Инструкция по установке**

Для пользователя:

`poetry install --no-dev`

Для разработчика:

`poetry install`

**Зависимости:**

 python 3.12.4  
 requests 2.32.3

**Запуск программы:**

`python main.py`

**Тестирование**

 Тестовые модули :

  `tests\test_masks.py`  
  `tests\test_processing.py`  
  `tasts\test_widget.py`  
  `tests\test_generators.py`  
  `tests\test_decorators.py`
  

**Лицензия**

Лицензия MIT

Copyright © «2024» Фоменко Алексей  
Данная лицензия разрешает лицам, получившим копию данного программного обеспечения и сопутствующей документации (в дальнейшем именуемыми «Программное Обеспечение»), безвозмездно использовать Программное Обеспечение без ограничений, включая неограниченное право на использование, копирование, изменение, слияние, публикацию, распространение, сублицензирование и/или продажу копий Программного Обеспечения, а также лицам, которым предоставляется данное Программное Обеспечение, при соблюдении следующих условий:

Указанное выше уведомление об авторском праве и данные условия должны быть включены во все копии или значимые части данного Программного Обеспечения.

ДАННОЕ ПРОГРАММНОЕ ОБЕСПЕЧЕНИЕ ПРЕДОСТАВЛЯЕТСЯ «КАК ЕСТЬ», БЕЗ КАКИХ-ЛИБО ГАРАНТИЙ, ЯВНО ВЫРАЖЕННЫХ ИЛИ ПОДРАЗУМЕВАЕМЫХ, ВКЛЮЧАЯ ГАРАНТИИ ТОВАРНОЙ ПРИГОДНОСТИ, СООТВЕТСТВИЯ ПО ЕГО КОНКРЕТНОМУ НАЗНАЧЕНИЮ И ОТСУТСТВИЯ НАРУШЕНИЙ, НО НЕ ОГРАНИЧИВАЯСЬ ИМИ. НИ В КАКОМ СЛУЧАЕ АВТОРЫ ИЛИ ПРАВООБЛАДАТЕЛИ НЕ НЕСУТ ОТВЕТСТВЕННОСТИ ПО КАКИМ-ЛИБО ИСКАМ, ЗА УЩЕРБ ИЛИ ПО ИНЫМ ТРЕБОВАНИЯМ, В ТОМ ЧИСЛЕ, ПРИ ДЕЙСТВИИ КОНТРАКТА, ДЕЛИКТЕ ИЛИ ИНОЙ СИТУАЦИИ, ВОЗНИКШИМ ИЗ-ЗА ИСПОЛЬЗОВАНИЯ ПРОГРАММНОГО ОБЕСПЕЧЕНИЯ ИЛИ ИНЫХ ДЕЙСТВИЙ С ПРОГРАММНЫМ ОБЕСПЕЧЕНИЕМ.
