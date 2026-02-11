from django.db import models


class Submission(models.Model):
    full_name = models.CharField("ФИО", max_length=255)
    email = models.EmailField("Email", blank=True, null=True)
    message = models.TextField("Сообщение")

    ip_address = models.GenericIPAddressField("IP-адрес")
    forwarded_ip = models.GenericIPAddressField("IP через прокси", blank=True, null=True)
    user_agent = models.TextField("User-Agent")
    accept_language = models.CharField("Accept-Language", max_length=100, blank=True, null=True)
    request_method = models.CharField("Метод запроса", max_length=10)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Форма обратной связи"
        verbose_name_plural = "Форма обратной связи"

    def __str__(self):
        return f"{self.full_name} ({self.ip_address})"


class TrapEvent(models.Model):
    TRAP_CHOICES = [
        ('HONEYPOT_INPUT', 'Скрытое input поле'),
        ('HONEYPOT_TEXTAREA', 'Скрытое textarea поле'),
        ('FAST_SUBMIT', 'Быстрое заполнение формы'),
        ('JS_ENABLED', 'Проверка на включенный JS'),
        ('NO_REFERER', 'Отсутствие HTTP Referer'),
    ]

    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='traps', verbose_name="Форма обратной связи")
    trap_type = models.CharField("Тип ловушки", max_length=50, choices=TRAP_CHOICES)
    triggered = models.BooleanField("Сработала", default=False)
    value = models.TextField("Значение поля", blank=True, null=True, help_text="Значение поля, если применимо")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Событие ловушки"
        verbose_name_plural = "События ловушек"

    def __str__(self):
        status = "Сработала" if self.triggered else "Не сработала"
        return f"{self.trap_type} - {status} ({self.submission.ip_address})"


class TrapLink(models.Model):
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    trap_name = models.CharField(max_length=100)
    trap_category = models.CharField(max_length=50)
    trap_type = models.CharField(max_length=10)
    source_page = models.CharField(max_length=100)
    referer = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ссылки ловушки"
        verbose_name_plural = "Ссылки ловушки"

    def __str__(self):
        return f"{self.ip_address} | {self.trap_category}"


class ScanAttempt(models.Model):
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    requested_path = models.CharField(max_length=255)
    referer = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Попытка сканирования"
        verbose_name_plural = "Попытки сканирования"

    def __str__(self):
        return f"{self.ip_address} | {self.requested_path}"