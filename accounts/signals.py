from django.db.models.signals import post_save , pre_save
from django.dispatch import receiver
from .models import User,UserProfile

@receiver(post_save,sender=User)
def post_save_create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()        
        except:
            UserProfile.objects.create(user=instance)
 
 
'''        
We can send  signal  by dispatch signal .....Also

We can send signal like this!     
post_save.connect(post_save_create_user_profile,sender=User)

'''
           

#Let's Test Pre Save as Well 
           
def pre_save_user_profile_alart(sender, instance, **kwargs):
    pass
    
pre_save.connect(pre_save_user_profile_alart,sender=User)





