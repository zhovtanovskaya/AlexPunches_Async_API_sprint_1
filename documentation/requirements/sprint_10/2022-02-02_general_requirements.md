# Общие рассуждения

Шаблон + Контекст = Уведомление пользователю
(Обогащение данными)

Где собирать контекст? До воркера, воркером, там и там?

Админ-панель, где менеджеры вручную создают
рассылку пользователям.  Например, по случаю
новой маркетинговой компании.
Генератор создает еженедельную рассылку.
UGC.

События: еженедельная рассылка, ручная рассылка,
рассылка о UGC.

# Функционал

* Поддержка управления уведомлениями для пользователей.
Отказ от определенных рассылок.

* Админ-панель для ручных рассылок.
* Генератор рассылок по расписанию.
* Генератор событий о лайках и прочем UGC. Activity API 
пишет в Kafka событие, после записи Mongo.
* Приветственное письмо. Auth.

* Создание шаблонов уведомлений.
* Короткая ссылка подтверждения email'а.
* Модуль, отвечающий за генерацию и отправку 
персонализированных писем. Что содержит такое письмо?
Это единственное письмо одному пользователю?
Индивидуальные рекомендации по фильмам?

* Рассылать email-ы.
* Реализуйте модуль для работы с Websoket. Между 
получателем уведомления и воркером-отправителем.

# Технические требования

* Поддержка часовых поясов пользователей.
* Персонализация уведомлений через шаблоны и контексты.

# Вопросы к демо

1. Реализовывать поддержку websoket?
2. Что такое "персонализированные письмо"? Они
связаны с рекомендательной системой? Или это
одно частное письмо одному пользователю?
