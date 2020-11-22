from django.contrib import admin
from django.conf.urls import url
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from core.apps.statistic import models as statistic_models
import csv


@admin.register(statistic_models.TelegramAccountStatistic)
class TelegramAccountStatisticAdmin(admin.ModelAdmin):
    list_display = ("tg_id", "username", "first_name", "last_name", "source", "type_action", "data", "created",)
    change_list_template = "admin/model_change_list.html"

    def get_urls(self):
        urls = super(TelegramAccountStatisticAdmin, self).get_urls()

        custom_urls = [
            url('^import/all/$', self.process_import_all, name='process_import_all'),
            url('^import/30d/$', self.process_import_30d, name='process_import_30d'),
            url('^import/7d/$', self.process_import_7d, name='process_import_7d'),
        ]
        return custom_urls + urls

    def process_import_all(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="tgstatistic_{timezone.now().strftime("%m_%d_%Y_%H_%M")}.csv"'

        self.message_user(request, "Статистика за всё время успешно импортирована!")
        writer = csv.writer(response)
        statistic = [i for i in statistic_models.TelegramAccountStatistic.objects.all().values()]
        writer.writerow(statistic)

        return response

    def process_import_30d(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="tgstatistic_{timezone.now().strftime("%m_%d_%Y_%H_%M")}_last30d.csv"'

        self.message_user(request, "Статистика за последние 30 дней успешно импортирована!")
        writer = csv.writer(response)
        statistic = [i for i in statistic_models.TelegramAccountStatistic.objects.filter(
            created__gte=timezone.now()-timezone.timedelta(days=30)).values()]
        writer.writerow(statistic)

        return response

    def process_import_7d(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="tgstatistic_{timezone.now().strftime("%m_%d_%Y_%H_%M")}_last7d.csv"'

        self.message_user(request, "Статистика за последние 7 дней успешно импортирована!")
        writer = csv.writer(response)
        statistic = [i for i in statistic_models.TelegramAccountStatistic.objects.filter(
            created__gte=timezone.now() - timezone.timedelta(days=7)).values()]
        writer.writerow(statistic)

        return response
