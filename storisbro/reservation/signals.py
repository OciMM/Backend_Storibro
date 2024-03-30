# Ваш signals.py
# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver
# from .models import DateOfReservation
# from creatives.models import AddSingleCreative 

# @receiver(m2m_changed, sender=AddSingleCreative.reservation.through)
# def update_count_room(sender, instance, action, **kwargs):
#     if action == 'post_add' or action == 'post_remove':
#         date_of_reservation = instance.reservation.first()
        
#         if date_of_reservation:
#             date_of_reservation.count_room = instance.reservation.count()
#             date_of_reservation.save()