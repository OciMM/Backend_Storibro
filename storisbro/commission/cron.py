# Ваш файл cron.py в приложении
import random

from django_cron import CronJobBase, Schedule
from .views import UpdatePublicModelStatusAPIView
from .models import PublicModel

class DailyPatchJob(CronJobBase):
    RUN_AT_TIMES = 1

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'commission.daily_patch_job'  # Уникальный код задачи

    def do(self):
        try:
            print("Задача DailyPatchJob начинает выполнение")
            view = UpdatePublicModelStatusAPIView()

            # Создание фейкового запроса (Request)
            class FakeRequest:
                method = 'PATCH'
        
            # Создание фейкового запроса
            fake_request = FakeRequest()
        
            # Получение всех объектов PublicModel
            public_models = PublicModel.objects.all()
        
            for public_model in public_models:
                # Выполнение PATCH-запроса на вашем представлении для каждого объекта PublicModel
                response = view.patch(fake_request, pk=public_model.pk)
            
                if response.status_code == 200:
                    print(f"Обновление объекта с pk={public_model.pk} выполнено успешно!")
                else:
                    print(f"Что-то пошло не так при обновлении объекта с pk={public_model.pk}.")
        except Exception as e:
            print(f"Произошла ошибка при выполнении запроса: {e}")