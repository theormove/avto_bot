#Описание услуг 
json_string = '''
{
"-- Защита авто от угона --" : "Prime Security Lab  занимается авторской защитой автомобилей от угона.\\n Мы не применяем шаблонные подходы в защите. Реализуем несколько сложных технических блокировок по автомобилю. \\n Дополнительно реализуем автозапуск и установку електромеханических замков капота и КПП. Также реализуем Защиту от угона ретранслятором (блокировака KeyLass), блокировку OBD и много дополнительных мероприятий по защите Вашего авто!",
"--Бронипленка--" : "Антигравийная пленка для автомобилей - это самое лучшее решение для защиты лакокрасочного покрытия авто от царапин, сколов, химических и органических веществ и других потенциальных дорожных угроз.\\n Пленка абсолютно невидима для глаз. Возможно полное или частичное покрытие автомобиля. Благодаря высокой эластичности возможна установка пленки на поверхности любой сложности. Также реализуем брендирование авто и покрытие в цветную пленку.",
"--Карбон--" : "Собственное производство карбоновых изделий любой сложности позволяет изготовлять от карбоновых частей отделки авто до частей кузова и тюнинга авто.\\nМы изготовим крутой карбоновый обвес для авто или придадим авто спортивного стиля салону.",
"--Шумоизоляция--" : "Большинство современных автомобилей не отличаются такой шумоизоляцией, которая бы полностью нас устраивала, и со временем раздражают водителя воем ветра, шумом колесных арок , невозможностью насладиться тишиной в салоне после 60 км/ч. \\nРешение проблемы найдено уже давно - частичная или комплексная шумоизоляция (в простонародии шумка). Проклеиваем только качественными материалами в несколько слоев без просветов. Отработанная методология на сотнях автомобилей.",
"--Парковочные системы--":"Парковочные системы будут полезны людям в большом городе, где приходится биться за каждый сантиметр парковочного места и парковаться впритык к другим автомобилям. Парктроники станут очень полезны, поскольку мелкий ремонт машины порой обходиться намного дороже чем сама парковочная система.\\nПомните, что купить хорошую парковочную систему недостаточно – ее надо правильно и аккуратно установить. Мастера нашего установочного центра подберут и установят парктроники, камеры заднего вида и круговой обзор для авто.",
"--Мультимедиа, регистраторы и акустика--":"Подберем и качественно установим Магнитолы и переходные рамки, регистраторы всех типов, колонки и сабвуферы. Наши специалисты имеют большой опыт по скрытным установкам мультимедийного оборудования. Подберем только проверенные образцы.",
"--Автосвет--": "Ужасный свет фар вашего автомобиля - это не только дискомфорт и вред зрению. В первую очередь - это угроза оказаться в ДТП!\\nНе рискуйте своим здоровьем и здоровьем своих близких!\\nМы подберем и качественно установим качественный ксенон, светодиодные лампы и дополнительный свет на авто.",
"--Покраска, полировка--":"При автосервисе работает малярный цех, где наши специалисты произведут лакокрасочные работы по Вашему авто. Полная и частичная покраска авто, полировка кузова и фар. Гарантия на работу обязательна!" 
 }'''
#вставки в меню услуг
json_string_2 = '''
{
"-- Защита авто от угона --" :["Защиту","Защите","https://www.youtube.com/watch?v=oayzrpfx1BM"],
"--Бронипленка--" : ["Бронипленку","Бронипленке","https://www.youtube.com/watch?v=uJpVjeWDCoU"],
"--Карбон--" : ["Карбон","Карбоне","https://www.youtube.com/watch?v=M_A5vgtczhA"],
"--Шумоизоляция--" : ["Шумоизоляцию","Шумоизоляции","https://www.youtube.com/watch?v=IFb7re-joaw&list=PLhGvRaeSy0EbEuQEYfSmgjVJm-L0PMD8y"], 
"--Парковочные системы--":["Парковочную систему","Парковочных системах","https://www.youtube.com/watch?v=G9YQV2IAuCI&list=PLhGvRaeSy0EamdivDs9PnNL0AXQALxm2Y"],
"--Мультимедиа, регистраторы и акустика--":["Мультимедиа","Мультимедиа","https://www.youtube.com/channel/UCwSYt0TIq9QixeVR7fZytFg/featured"],
"--Автосвет--": ["Автосвет","Автосвете","https://www.youtube.com/watch?v=zQZq8nLieP0&list=PLhGvRaeSy0EamdivDs9PnNL0AXQALxm2Y&index=2"],
"--Покраска, полировка--":["покраску/полировку","покраске/полировке","https://www.youtube.com/channel/UCwSYt0TIq9QixeVR7fZytFg/featured"]
 }'''

#Вопросы и ответы (рубрики в том порядке как в словарях сверху)
json_string_3 = '''
{
"1" :"<b>Как дела?</b>\\n<b>Все хорошо!</b>",
"2" :"<b>Как дела?</b>\\n<b>Все хорошо!</b>",
"3" :"<b>Как дела?</b>\\n<b>Все хорошо!</b>",
"4" :"<b>Как дела?</b>\\n<b>Все хорошо!</b>", 
"5":"<b>Как дела?</b>\\n<b>Все хорошо!</b>",
"6":"<b>Как дела?</b>\\n<b>Все хорошо!</b>",
"7":"<b>Как дела?</b>\\n<b>Все хорошо!</b>",
"8":"<b>Как дела?</b>\\n<b>Все хорошо!</b>"
 }'''

#ссылки на ютуб видео 
video_links = ["https://www.youtube.com/watch?v=oayzrpfx1BM&t=4s","https://www.youtube.com/watch?v=vcecNAZlW9g","https://www.youtube.com/watch?v=fBapI1iS6s0","https://www.youtube.com/watch?v=uJpVjeWDCoU&t=2s","https://www.youtube.com/watch?v=OcIkkn1u5xw"]
#sql inj
sql_commands = ['DROP','GRANT ALL', 'TRUNCATE', 'DELETE', 'COMMIT', 'CREATE OR REPLACE', 'SELECT', '.execute']





