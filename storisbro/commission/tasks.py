from celery import shared_task
from commission.services import check_link_in_community 
from commission.models import PublicModel

@shared_task(bind=True)
def run_patch_task(self):
    # Ваш код для вызова метода patch здесь
    # Например:

    public_models = PublicModel.objects.all()
    for public_model in public_models:
        link_to_check = public_model.url
        link_found = check_link_in_community(public_model.name, link_to_check)
        print(f"Link found for {public_model.name}: {link_found}")

        if link_found:
            public_model.status = True
        else:
            public_model.status = False
        public_model.save()

    public_model.refresh_from_db()
