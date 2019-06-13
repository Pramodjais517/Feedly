from .models import MyProfile
from django.db.models import Q


def Search(search_list,quer,i,user):
        if i == len(search_list):
            if quer == MyProfile.objects:
                quer = MyProfile.objects.filter(user=None)
                return quer
            return quer
        else:
            result = quer.filter(Q(user__username__icontains=search_list[i])|Q(first_name__icontains=search_list[i])|
                              Q(last_name__icontains=search_list[i])|Q(user__email__icontains=search_list[i])|
                              Q(phone_number__icontains=search_list[i])).exclude(user=user)
            if len(result)==0:
                result = quer
            i+=1
            return Search(search_list,result,i,user)


