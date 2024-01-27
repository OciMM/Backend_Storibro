from django.db import models


"""Модели по изменению контента на лендинге (оба)"""

class TypeLending(models.Model):
    """Объектов этой модели может быть всего лишь 2, а именно виды лендингов"""
    name = models.CharField(max_length=100, verbose_name="Название лендинга")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Тип лендинга"
        verbose_name_plural = "Типы лендинга"
# основная модель лендинга для админов
class ContentLendingModel(models.Model):
    type_lending = models.ForeignKey(
        TypeLending, 
        on_delete=models.PROTECT, 
        verbose_name="Вид лендинга"
    )
    # Первая рамка (блок)
    first_text_bold = models.CharField(
        max_length=500,
        verbose_name="Главный текст в первой рамке",
        blank=True
    )
    first_text_small = models.CharField(
        max_length=500,
        verbose_name="Второстепенный текст в первой рамке",
        blank=True
    )
    first_image = models.ImageField(
        upload_to="",
        verbose_name="Изображение в первой рамке",
        blank=True
    )
    # Вторая рамка (блок)
    second_main_text = models.CharField(
        max_length=500, 
        verbose_name="Текст во второй рамке",
        blank=True
    )
    author_text = models.CharField(
        max_length=500,
        verbose_name="Автор текст",
        blank=True
    )
    second_image = models.ImageField(
        upload_to="",
        verbose_name="Изображение во второй рамке",
        blank=True
    )
    # сообщества
    community_main_text = models.CharField(
        max_length=500,
        verbose_name="Главный текст в разделе сообществ",
        blank=True
    )
    community_count = models.PositiveIntegerField(
        verbose_name="Количество сообществ",
        default=0
    )
    # Примеры рекламных креативов
    creative_main_text = models.CharField(
        max_length=500,
        verbose_name="Главный текст раздела",
        blank=True
    )
    creative_one = models.ImageField(
        upload_to="",
        verbose_name="Креатив №1",
        blank=True
    )
    creative_two = models.ImageField(
        upload_to="",
        verbose_name="Креатив №2",
        blank=True
    )
    creative_three = models.ImageField(
        upload_to="",
        verbose_name="Креатив №3",
        blank=True
    )
    # третья рамка
    third_text_bold = models.CharField(
        max_length=500,
        verbose_name="Главный текст в третьей рамке",
        blank=True
    )
    third_text_small = models.CharField(
        max_length=500,
        verbose_name="Второстепенный текст в третьей рамке",
        blank=True
    )
    third_image = models.ImageField(
        upload_to="",
        verbose_name="Изображение в третьей рамке",
        blank=True
    )
    # VK блок
    vk_main_text = models.CharField(
        max_length=500,
        verbose_name="Главный текст в рамке vk",
        blank=True
    )
    vk_second_text = models.CharField(
        max_length=500,
        verbose_name="Второстепенный текст в рамке vk",
        blank=True
    )
    vk_link = models.URLField(
        verbose_name="Ссылка на vk",
        blank=True
    )

    def __str__(self):
        return "Контент на лендинге для админов"
    
    class Meta:
        verbose_name = "Лендинг"


# Дополнительные модели в которых поля, которые не вошли в первую модель
class PositiveContentLendingModel(models.Model):
    """Преимущество Storisbro"""
    type_lending = models.ForeignKey(
        TypeLending, 
        on_delete=models.PROTECT, 
        verbose_name="К какому лендингу относится"
    )
    text = models.TextField(verbose_name="Текст преимущества")
    image = models.ImageField(upload_to="", verbose_name="Изображение преимущества")

    def __str__(self):
        return f"Преимущество - {self.text}"
    
    class Meta:
        verbose_name = "Лендинг (Преимущество)"


class QuestionContentLendingModel(models.Model):
    """FAQ Storisbro"""
    type_lending = models.ForeignKey(
        TypeLending, 
        on_delete=models.PROTECT, 
        verbose_name="К какому лендингу относится"
    )
    name = models.CharField(max_length=500, verbose_name="Вопрос")
    text = models.TextField(verbose_name="Текст вопроса")

    def __str__(self):
        return f"Вопрос - {self.name}"
    
    class Meta:
        verbose_name = "Лендинг (Вопрос)"
        
    
"""Модели контента авторизации и регистрации"""


class ContentAuth(models.Model):
    # линия №1
    error_login_pass = models.CharField(
        max_length=500,
        verbose_name="Текст ошибка в логине или пароле",
        blank=True
    )
    confirmation_login = models.CharField(
        max_length=500,
        verbose_name="Текст при подтверждении входа",
        blank=True
    )
    error_false_confirmation_login = models.CharField(
        max_length=500,
        verbose_name="Текст ошибки при подтверждении входа",
        blank=True
    )

    message_successful = models.CharField(
        max_length=500,
        verbose_name="Текст успешного восстановления",
        blank=True
    )
    message_successful_image = models.ImageField(upload_to='', verbose_name="Иконка")
    message_successful_button = models.CharField(
        max_length=500,
        verbose_name="Текст кнопки успешного восстановления",
        blank=True
    )

    message_error = models.CharField(
        max_length=500,
        verbose_name="Текст неудачной привязки",
        blank=True
    )
    message_error_image = models.ImageField(upload_to='', verbose_name="Иконка")
    message_error_button = models.CharField(
        max_length=500,
        verbose_name="Текст кнопки неудачной привязки восстановления",
        blank=True
    )
    # линия №2
    error_change_pass = models.CharField(
        max_length=500,
        verbose_name="Текст ошибки при смене пароля",
        blank=True
    )

    def __str__(self):
        return "Настройка авторизации"
    
    class Meta:
        verbose_name = "Настройка авторизации"
        verbose_name_plural = "Настройки авторизации"


class ContentRegistration(models.Model):
    # линия №3
    error_repeat_pass = models.CharField(
        max_length=500,
        verbose_name="Текст ошибки с эл.почтой",
        blank=True
    )

    error_false_pass = models.CharField(
        max_length=500,
        verbose_name="Текст ошибки с паролем",
        blank=True
    )
    # линия №4
    error_confirmation_email = models.CharField(
        max_length=500,
        verbose_name="Текст ошибки при подтверждение почты",
        blank=True
    )

    def __str__(self):
        return "Настройка регистрации"
    
    class Meta:
        verbose_name = "Настройка регистрации"
        verbose_name_plural = "Настройки регистрации"


"""Контент техподдержки"""


class TypeTechnicalSupport(models.Model):
    """Тут находится только 2 разных объекта (Для заказчиков и для админов)"""
    name = models.CharField(max_length=150, verbose_name="Тип поддержки (для кого)")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Тип поддержки"
        verbose_name_plural = "Типы поддержки"


class ContentTechnicalSupport(models.Model):
    type = models.ForeignKey(
        TypeTechnicalSupport,
        on_delete=models.PROTECT,
        verbose_name="К какому типу относятся настройки"
    )
    text = models.TextField(verbose_name='Цитата', blank=True)
    author = models.CharField(max_length=150, verbose_name='Автор цитаты', blank=True)
    url = models.URLField(verbose_name='Ссылка на техподдержку VK', blank=True)

    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = "Настройка контента техподдержка"
        verbose_name_plural = "Настройки контента техподдержка"


"""Контент по реферальной системе"""


class TypeReferralSystem(models.Model):
    """Тут находится только 2 разных объекта (Для заказчиков и для админов)"""
    name = models.CharField(max_length=150, verbose_name="Тип реферальной системы (для кого)")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Тип реферальной системы"
        verbose_name_plural = "Типы реферальной системы"


class ContentReferralSystem(models.Model):
    type = models.ForeignKey(
        TypeReferralSystem,
        on_delete=models.PROTECT,
        verbose_name="К какому типу относятся настройки"
    )
    text = models.TextField(verbose_name='Основной текст в разделе', blank=True)
    first_icon = models.ImageField(upload_to='', verbose_name='Первая иконка', blank=True)
    second_icon = models.ImageField(upload_to='', verbose_name='Вторая иконка', blank=True)
    main_image = models.ImageField(upload_to='', verbose_name='Основное изображение', blank=True)

    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = "Настройка контента реферальной системы"
        verbose_name_plural = "Настройки контента реферальной системы"


"""Контент личного профиля"""


class ContentProfile(models.Model):
    # линия №1
    error_change_email = models.CharField(
        max_length=500,
        verbose_name="Текст ошибки подтверждения почты",
        blank=True
    )
    success_change_email = models.CharField(
        max_length=500,
        verbose_name="Текст ответа на успешное изменение почты",
        blank=True
    )
    success_change_email_icon = models.ImageField(
        upload_to='', 
        verbose_name='иконка в ответе на успешное изменение почты',
        blank=True
    )
    # линия №2
    comment_refill = models.CharField(
        max_length=500,
        verbose_name="Комментарий в разделе 'пополнение'",
        blank=True
    )
    error_refill = models.CharField(
        max_length=500,
        verbose_name="Ошибка с платежом (пополнение)",
        blank=True
    )
    error_withdrawal = models.CharField(
        max_length=500,
        verbose_name="Ошибка с платежом (вывод денег)",
        blank=True
    )
    error_false_confirmation_code = models.CharField(
        max_length=500,
        verbose_name="Ошибка с подтверждением кода",
        blank=True
    )
    # линия №3
    error_pass_mismatch = models.CharField(
        max_length=500,
        verbose_name="Ошибка с несовпадением паролей",
        blank=True
    )
    error_pass_small = models.CharField(
        max_length=500,
        verbose_name="Ошибка с некорректным паролем",
        blank=True
    )


"""Контент шапки и футера"""

class ContentHeader(models.Model):
    logo = models.ImageField(upload_to='', verbose_name='Лого шапки', blank=True)

    def __str__(self):
        return "Контент шапки"
    
    class Meta:
        verbose_name = "Настройка контента шапки"
        verbose_name_plural = "Настройки контента шапки"


class ContentFooter(models.Model):
    logo = models.ImageField(upload_to='', verbose_name='Лого шапки', blank=True)
    all_rights = models.CharField(
        max_length=500,
        verbose_name='Текст "Все права защищены"',
        blank=True
    )
    terms_of_use_first = models.URLField(verbose_name='Ссылка на правила пользования')
    terms_of_use_second = models.URLField(verbose_name='Ссылка на пользовательское соглашение')

    def __str__(self):
        return "Контент футера"
    
    class Meta:
        verbose_name = "Настройка контента футера"
        verbose_name_plural = "Настройки контента футера"


"""Контент в разделе пониженной комиссии"""


class ContentSpecialCommission(models.Model):
    main_text = models.CharField(
        max_length=500,
        verbose_name="Текст главного раздела",
        blank=True
    )
    help_text = models.CharField(
        max_length=500,
        verbose_name="Текст в рамке",
        blank=True
    )
    help_image = models.ImageField(
        upload_to='',
        verbose_name='Изображение в рамке',
        blank=True
    )
    error = models.CharField(
        max_length=500,
        verbose_name="Текст в случае ошибки или неудачи",
        blank=True
    )
    success = models.CharField(
        max_length=500,
        verbose_name="Текст в случае успешной проверки",
        blank=True
    )

    def __str__(self):
        return "Контент пониженной комиссии"
    
    class Meta:
        verbose_name = "Настройка контента пониженной комисии"
        verbose_name_plural = "Настройки контента пониженной комисии"


"""Контент в разделе заказчика"""


class ContentClientHelp(models.Model):
    first_main_text = models.CharField(
        max_length=500,
        verbose_name="Главный верхний текст",
        blank=True
    )
    main_image = models.ImageField(upload_to='', verbose_name="Главное верхнее изображение", blank=True)

    second_main_text = models.CharField(
        max_length=500,
        verbose_name="Главный верхний текст",
        blank=True
    )
    second_full_text = models.TextField(verbose_name='Основной текст в середине', blank=True)

    third_main_text = models.CharField(
        max_length=500,
        verbose_name="Главный текст в третий части",
        blank=True
    )
    third_full_text = models.TextField(verbose_name='Основной текст в третий части', blank=True)

    last_main_text = models.CharField(
        max_length=500,
        verbose_name="Главный последний текст",
        blank=True
    )
    last_full_text = models.TextField(verbose_name='Основной последний текст', blank=True)

    def __str__(self):
        return "Контент в разделе заказчики (помощь)"
    
    class Meta:
        verbose_name = "Настройка контента в разделе заказчиков"
        verbose_name_plural = "Настройки контента в разделе заказчиков"


class ContentClientReservation(models.Model):
    main_text_panel = models.CharField(
        max_length=500,
        verbose_name="Главный текст в рамке",
        blank=True
    )
    main_image_panel = models.ImageField(upload_to='', verbose_name='Главное изображение в рамке', blank=True)

    thanks_text = models.CharField(
        max_length=500,
        verbose_name="Текст благодарности",
        blank=True
    )

    refill_main_text = models.CharField(
        max_length=500,
        verbose_name="Главный текст в рамке пополнения",
        blank=True
    )
    refill_full_text = models.TextField(verbose_name='Основной текст пополнения', blank=True)
    refill_image = models.ImageField(upload_to='', verbose_name='Изображение в рамке "Пополнение"', blank=True)
    refill_help_text = models.CharField(
        max_length=500,
        verbose_name="Текст подсказки",
        blank=True
    )

    error_cansel_reservation = models.CharField(
        max_length=500,
        verbose_name="Текст в случае ошибки при отмене брони",
        blank=True
    )
    success_cansel_reservation = models.CharField(
        max_length=500,
        verbose_name="Текст в случае успеха при отмене брони",
        blank=True
    )

    def __str__(self):
        return "Контент в разделе заказчики (бронь)"
    
    class Meta:
        verbose_name = "Настройка контента в разделе заказчиков"
        verbose_name_plural = "Настройки контента в разделе заказчиков"


class ContentClientCreative(models.Model):
    CTR_help_text = models.CharField(
        max_length=500,
        verbose_name="Текст в подсказке CTR",
        blank=True
    )

    act_creative_text = models.CharField(
        max_length=500,
        verbose_name="Текст действия с креативом",
        blank=True
    )
    delete_creative_text = models.CharField(
        max_length=500,
        verbose_name="Текст при удалении креатива",
        blank=True
    )
    success_add_creative_text = models.CharField(
        max_length=500,
        verbose_name="Текст успешном добавлении креатива",
        blank=True
    )

    error_search_story_text = models.CharField(
        max_length=500,
        verbose_name="Текст в случае, если история не будет найдена",
        blank=True
    )

    def __str__(self):
        return "Контент в разделе заказчики (креативы)"
    
    class Meta:
        verbose_name = "Настройка контента в разделе заказчиков"
        verbose_name_plural = "Настройки контента в разделе заказчиков"


"""Контент в разделе админов"""


class ContentAdminHelp(models.Model):
    first_main_text = models.CharField(
        max_length=500,
        verbose_name="Главный верхний текст",
        blank=True
    )
    main_image = models.ImageField(upload_to='', verbose_name="Главное верхнее изображение", blank=True)

    second_main_text = models.CharField(
        max_length=500,
        verbose_name="Главный текст",
        blank=True
    )
    second_full_text = models.TextField(verbose_name='Основной текст в середине', blank=True)
    second_main_image = models.ImageField(upload_to='', verbose_name="Главное верхнее изображение", blank=True)

    third_main_text = models.CharField(
        max_length=500,
        verbose_name="Главный текст",
        blank=True
    )
    third_full_text = models.TextField(verbose_name='Основной текст в третий части', blank=True)

    MCA_creative_text = models.CharField(
        max_length=500,
        verbose_name="Главный текст МЦА",
        blank=True
    )
    MCA_creative_one = models.ImageField(upload_to='', verbose_name="Креатив МЦА №1", blank=True)
    MCA_creative_two = models.ImageField(upload_to='', verbose_name="Креатив МЦА №2", blank=True)
    MCA_creative_three = models.ImageField(upload_to='', verbose_name="Креатив МЦА №3", blank=True)

    ZHCA_creative_text = models.CharField(
        max_length=500,
        verbose_name="Главный текст ЖЦА",
        blank=True
    )
    ZHCA_creative_one = models.ImageField(upload_to='', verbose_name="Креатив ЖЦА №1", blank=True)
    ZHCA_creative_two = models.ImageField(upload_to='', verbose_name="Креатив ЖЦА №2", blank=True)
    ZHCA_creative_three = models.ImageField(upload_to='', verbose_name="Креатив ЖЦА №3", blank=True)

    SCA_creative_text = models.CharField(
        max_length=500,
        verbose_name="Главный текст СЦА",
        blank=True
    )
    SCA_creative_one = models.ImageField(upload_to='', verbose_name="Креатив СЦА №1", blank=True)
    SCA_creative_two = models.ImageField(upload_to='', verbose_name="Креатив СЦА №2", blank=True)
    SCA_creative_three = models.ImageField(upload_to='', verbose_name="Креатив СЦА №3", blank=True)

    four_main_text = models.CharField(
        max_length=500,
        verbose_name="Главный текст",
        blank=True
    )
    four_full_text = models.TextField(verbose_name='Основной текст в третий части', blank=True)

    five_main_text = models.CharField(
        max_length=500,
        verbose_name="Главный текст",
        blank=True
    )
    five_full_text = models.TextField(verbose_name='Основной текст в третий части', blank=True)

    def __str__(self):
        return "Контент в разделе админы (помощь)"
    
    class Meta:
        verbose_name = "Настройка контента в разделе админов"
        verbose_name_plural = "Настройки контента в разделе админ"


class ContentAdminHelpRequest(models.Model):
    request_text = models.CharField(
        max_length=500,
        verbose_name="Требование",
        blank=True
    )

    def __str__(self):
        return "Контент в разделе админы (помощь)[требование]"
    
    class Meta:
        verbose_name = "Настройка контента в разделе админов (доп)"
        verbose_name_plural = "Настройки контента в разделе админ (доп)"


class ContentAdminHelpIncrease(models.Model):
    increase_main_text = models.CharField(
        max_length=500,
        verbose_name="Название совета",
        blank=True
    )
    increase_full_text = models.CharField(
        max_length=500,
        verbose_name="Содержание совета",
        blank=True
    )

    def __str__(self):
        return "Контент в разделе админы (помощь)[советы]"
    
    class Meta:
        verbose_name = "Настройка контента в разделе админов (доп)"
        verbose_name_plural = "Настройки контента в разделе админ (доп)"


class ContentAdminStatistic(models.Model):
    first_comment_text = models.CharField(
        max_length=500,
        verbose_name="Первый комментарий в разделе статистика",
        blank=True
    )

    income_comment_text = models.CharField(
        max_length=500,
        verbose_name="Комментарий к заработку в разделе статистика",
        blank=True
    )

    def __str__(self):
        return "Контент в разделе админы (статистика)"
    
    class Meta:
        verbose_name = "Настройка контента в разделе админов"
        verbose_name_plural = "Настройки контента в разделе админ"


class ContentAdminCommunity(models.Model):
    error_add_community = models.CharField(
        max_length=500,
        verbose_name="Текст ошибки при добавлении сообщества",
        blank=True
    )

    repeat_download_text = models.CharField(
        max_length=500,
        verbose_name="Комментарий на повторую загрузку",
        blank=True
    )

    erroe_cansel_story = models.CharField(
        max_length=500,
        verbose_name="Ошибка в случае отсутствия прав на публикацию",
        blank=True
    )

    success_text = models.CharField(
        max_length=500,
        verbose_name="сообщение в случае успеха",
        blank=True
    )

    delete_comment_text = models.CharField(
        max_length=500,
        verbose_name="сообщение в случае удаления сообщества",
        blank=True
    )

    error_tg = models.CharField(
        max_length=500,
        verbose_name="сообщение в случае ошибки с тг каналом",
        blank=True
    )

    def __str__(self):
        return "Контент в разделе админы (сообщества)"
    
    class Meta:
        verbose_name = "Настройка контента в разделе админов"
        verbose_name_plural = "Настройки контента в разделе админ"