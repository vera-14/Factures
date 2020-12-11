UPDATE words
SET accent = NULL,
word_type = 1
WHERE word_form IN
('БЕЗ',
'ВО',
'ДО',
'ЗА',
'ИЗ',
'НА',
'НЕ',
'НИ',
'О',
'ОБ',
'ОТ',
'ПО',
'ПОД', 
'ПРИ',
'ПРО',
'СО',
'У');
