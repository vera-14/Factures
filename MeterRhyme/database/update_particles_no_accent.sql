UPDATE words
SET accent = NULL,
word_type = 3
WHERE word_form IN
(
"ДЕ",
"КА",
"КОЕ",
"КОЙ",
"КАСЬ",
"ЛИБО",
"НИБУДЬ",
"С",
"ТКА",
"ТКО",
"ТО");
