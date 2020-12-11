UPDATE words
SET accent = NULL,
word_type = 2
WHERE word_form IN
("А",
"БЫ",
"ВЕДЬ",
"ДА",
"ДЛЯ",
"ЖЕ",
"И",
"КО",
"ЛИ",
"МЕЖ",
"МОЛ",
"НАД",
"ПРЕД ",
"СРЕДЬ",
"ТАК",
"ЧРЕЗ");
