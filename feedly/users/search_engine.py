from .models import MyProfile
from django.db.models import Q


def Search(search_list,quer,i):
        if i == len(search_list) or len(quer)==0:
            print(quer)
            return quer

        else:
            result = quer.filter(Q(user__username__icontains=search_list[i])|Q(first_name__icontains=search_list[i])|
                              Q(last_name__icontains=search_list[i])|Q(user__email__icontains=search_list[i])|
                              Q(phone_number=search_list[i]))
            if(len(result)==0):
                return quer
            i+=1
            Search(search_list,result,i)


