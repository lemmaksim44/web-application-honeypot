from django.contrib import admin
from .models import Submission, TrapEvent, TrapLink, ScanAttempt, CaptchaEvent


class TrapEventInline(admin.TabularInline):
    model = TrapEvent
    extra = 0
    readonly_fields = ('trap_type', 'triggered', 'value', 'created_at')
    can_delete = False


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'ip_address', 'created_at', 'triggered_traps_count')
    list_filter = ('created_at',)
    search_fields = ('full_name', 'email', 'ip_address', 'user_agent')
    inlines = [TrapEventInline]

    def triggered_traps_count(self, obj):
        return obj.traps.filter(triggered=True).count()
    triggered_traps_count.short_description = "Сработавшие ловушки"


@admin.register(TrapEvent)
class TrapEventAdmin(admin.ModelAdmin):
    list_display = ('submission', 'trap_type', 'triggered', 'created_at')
    list_filter = ('trap_type', 'triggered', 'created_at')
    search_fields = ('submission__full_name', 'submission__email', 'submission__ip_address')
    readonly_fields = ('submission', 'trap_type', 'triggered', 'value', 'created_at')


@admin.register(TrapLink)
class TrapLinkAdmin(admin.ModelAdmin):
    list_display = ('trap_name', 'trap_category', 'trap_type', 'source_page', 'ip_address', 'short_user_agent', 'created_at')
    list_filter = ('trap_category', 'trap_type', 'source_page', 'created_at')
    search_fields = ('ip_address', 'trap_name', 'user_agent')
    readonly_fields = ('trap_name', 'trap_category', 'trap_type', 'source_page', 'ip_address', 'user_agent', 'referer', 'created_at')
    ordering = ('-created_at',)

    def short_user_agent(self, obj):
        return obj.user_agent[:50]
    short_user_agent.short_description = "User Agent"


@admin.register(ScanAttempt)
class ScanAttemptAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'requested_path', 'referer', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('ip_address', 'requested_path', 'referer')
    readonly_fields = ('ip_address', 'user_agent', 'requested_path', 'referer', 'created_at')
    ordering = ('-created_at',)


@admin.register(CaptchaEvent)
class CaptchaEventAdmin(admin.ModelAdmin):
    list_display = ("submission", "captcha_type", "success", "time_on_page", "js_enabled", "created_at")
    list_filter = ("captcha_type", "success", "js_enabled", "created_at")
    search_fields = ("submission__full_name", "submission__email", "submission__ip_address")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)