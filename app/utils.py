# utils.py
from collections import defaultdict

from .models import Noeud, Lampe, Planification


from django.utils import timezone
import threading
import time
from datetime import datetime

#utils fichier nehtou fyh des fonctions (ne9es 3ala rouhy el khdema , ye3ni bech tekhoun medhema el khdema )

def get_week_number(day_str, month_str):# le nombre de la semaine

    day = int(day_str)
    month = int(month_str)

    current_year = datetime.now().year# le nombre de l'annee


    
    date_obj = datetime(current_year, month, day)# le nombre de la date


    
    week_number = date_obj.isocalendar()[1]# le nombre de la semaine


    
    return week_number


def get_hours_difference(start_date_str, end_date_str):#te3tiha deux data terje3lk diff bintehom
    
    start_date = datetime.fromisoformat(start_date_str[:-6])#Transforme une chaîne de caractères qui décrit une date et une heure selon le standard ISO 8601 en un objet datetime.

    end_date = datetime.fromisoformat(end_date_str[:-6]) 
    
    time_difference = end_date - start_date# le nombre de la difference entre les deux dates
    

    if  time_difference.days < 0:# si la difference est negative

        return 0
    difference_in_hours = time_difference.total_seconds() / 3600
    
    return difference_in_hours




def get_lampes_by_noeud_name(noeud_name):# le nombre de la lampe selon le noeud


    try:
                # Cherche le nœud dans la base de données par son nom

        noeud = Noeud.objects.get(name=noeud_name)
       # Filtre les lampes qui sont associées à ce nœud => nadhemhoum ye3ni
        lampes = Lampe.objects.filter(noeud=noeud)
        return lampes
    except Noeud.DoesNotExist:
       
        return None





def get_lampes_by_noeud_id(noeud_id):
    try:
        
        noeud = Noeud.objects.get(id=noeud_id)
       
        lampes = Lampe.objects.filter(noeud=noeud)
        return lampes
    except Noeud.DoesNotExist:# si le noeud n'existe pas

        
        return None



def get_nodes_with_lampes():# le nombre de noeuds avec les lampes


    all_noeuds = Noeud.objects.all()# Récupère tous les nœuds de la base de données(nerje3 tous les noeuds)


    result = defaultdict(list)# Crée un dictionnaire avec des listes comme valeurs par défaut


    # Pour chaque nœud, récupère les lampes associées et formate les informations
    for noeud in all_noeuds:
        related_lampes = Lampe.objects.filter(noeud=noeud)# on chercher   les lampes qui sont reliées au noeud

        # C'est un dictionnaire qui contient des informations sur chaque lampe
        lampes_info = [{'id': str(lampe.id), 'name': lampe.name, 'puissance': lampe.puissance} for lampe in related_lampes]
       
        # Ajoute les informations du nœud et des lampes au dictionnaire 
        result[noeud.name] = {'id': str(noeud.id), 'lampes': lampes_info}





   # on retourne les noeuds avec les lampes
    return [{'noeud_name': noeud_name, 'id': info['id'], 'lampes': info['lampes']} for noeud_name, info in result.items()]








    
def autoUpdateStatus():# on met à jour le status des lampes

    current_date = timezone.now() #nekhou fy data mte3 tawa
    planifications = Planification.objects.all()# nekhou fel planification lkoul
    for planification in planifications: # inboucli 3la les planification elkol
        start_datetime = planification.start_date #na5dho el start date mta3a el planification
        end_datetime = planification.end_date #na5dho el end date mta3a el planification
        
        if start_datetime <= current_date and end_datetime > current_date: #n9arno idha ken el start date bdet
            planification.status = 'pending' #n7oto els status mta3 el planification lil pending
            planification.save() 
        if end_datetime <= current_date:
            planification.status = 'completed' #n7oto els status mta3 el planification lil completed
            planification.save() 
  
    threading.Timer(60.0, autoUpdateStatus).start()

# autoUpdateStatus()

# qui calcule des données مجمعة sur la consommation d'énergie pour chaque année spécifique pour les lampes associées à un nœud donné. 


def get_data_for_node_for_specific_date(node_name, period, d1, d2):# on chercher les données pour un noeud et une periode donnée

    if period == "year":
        return get_data_for_node_for_specific_date_year(node_name, d1, d2)
    elif period == "month":
        return get_data_for_node_for_specific_date_month(node_name, d1, d2)
    elif period == "week":
        return get_data_for_node_for_specific_date_week(node_name, d1, d2)
    else:
        return get_data_for_node_for_specific_date_day(node_name, d1, d2)

    



def get_data_for_node_for_specific_date_year(node_name, date1, date2):#chercher  des données pour un nœud mou3ina pour
    #une année mou3ina
    lampes = get_lampes_by_noeud_name(node_name) #te3ith noeud 1 yerje3lek les lampes lkoul eli tb3in noeud 1
    print("=====",lampes[0],"==========")
    data_for_year = []
    planifications = Planification.objects.all() #nejib fel data mel bd
    years = set() #tekhbi fyha hajet unique
    for plan  in planifications:
        print("plan",plan)
        if (((date1 != None and  date2 !=None) and (date1 <= str(plan.start_date)[:10] and date2 >= str(plan.start_date)[:10])) or (date1 == None and  date2==None)):
            year_start = str(plan.start_date)[:4] # 2023-02, 2024-02
            print("plan.start_date-----",plan.start_date)
            years.add(year_start)

    years = list(years)
    years.sort()
    for lampe in lampes:
        my_lampe = Lampe.objects.get(id=lampe.id)
        print(f"lampe id = {my_lampe}")
        planifications = Planification.objects.filter(lampe=my_lampe) #nejib fel data mel bd
        
        data_for_year_single_lampe = []
        for year in years:
            cons = 0
            for plan in planifications:
                if str(plan.start_date)[:4]==year:# nehseb consommation mte3  date eli hchti bih
                    cons += get_hours_difference(str(plan.start_date),str(plan.end_date)) * plan.lampe.puissance# terje3li nbr swie3
            data_for_year_single_lampe.append(cons)
        data_for_year.append(data_for_year_single_lampe)
    print("hyhyhy",data_for_year)
   
    final_data = []
    for j in range(len(data_for_year[0])):
        x = 0
        for i in range(len(data_for_year)):
            x += data_for_year[i][j]
        final_data.append(x/len(data_for_year))# nehseb consommation totale mte3  noeud  khw ()
            
    return final_data,years
                


#[[150,50],[125,15],[140,200]]
# [ , ]


   
def get_data_for_node_for_specific_date_month(node_name,date1, date2):
    lampes = get_lampes_by_noeud_name(node_name) #te3ith noeud 1 yerje3lek les lampes lkoul eli tb3in noeud 1
    data_for_month = []
    planifications = Planification.objects.all() #nejib fel data mel bd
    months = set() #tekhbi fyha hajet unique
    for plan  in planifications:
        if (((date1 != None and  date2!=None) and (date1 <= str(plan.start_date)[:10] and date2 >= str(plan.start_date)[:10])) or (date1 == None and  date2==None)):        
            month_start = str(plan.start_date)[:7] 
            print("month_start",month_start)
            months.add(month_start)

    months = list(months)
    months.sort()
    print("0.0.0.0",months)
    for lampe in lampes:
        my_lampe = Lampe.objects.get(id=lampe.id)
        print(f"lampe id = {my_lampe}")
        planifications = Planification.objects.filter(lampe=my_lampe) #nejib fel data mel bd
        
        data_for_month_single_lampe = []
        for month in months:
            cons = 0
            for plan in planifications:
                if str(plan.start_date)[:7]==month:# nehseb consommation mte3  date eli hchti bih
                    cons += get_hours_difference(str(plan.start_date),str(plan.end_date)) * plan.lampe.puissance# terje3li nbr swie3
                    print("-+-+-+-+-",get_hours_difference(str(plan.start_date),str(plan.end_date)), "debut",str(plan.start_date) , "fin:", str(plan.end_date) )
            data_for_month_single_lampe.append(cons)
        data_for_month.append(data_for_month_single_lampe)
    print("hyhyhy",data_for_month)

    final_data = []
    for j in range(len(data_for_month[0])):
        x = 0
        for i in range(len(data_for_month)):
            x += data_for_month[i][j]
        final_data.append(x/len(data_for_month))# nehseb consommation totale mte3  noeud  khw ()
            
    return final_data, months


def get_data_for_node_for_specific_date_day(node_name, date1, date2):#nty  te3tiha date mou3in o hya tekherjlek consommation mte3 3am kmel
    lampes = get_lampes_by_noeud_name(node_name) #te3ith noeud 1 yerje3lek les lampes lkoul eli tb3in noeud 1
    print("=====",lampes[0],"==========")
    data_for_day = []
    planifications = Planification.objects.all() #nejib fel data mel bd
    days= set() #tekhbi fyha hajet unique
    for plan  in planifications:
        print("plan",plan)
        if (((date1 != None and  date2!=None) and (date1 <= str(plan.start_date)[:10] and date2 >= str(plan.start_date)[:10])) or (date1 == None and  date2==None)):
            day_start = str(plan.start_date)[:10]  # 2023-02-22, 2024-02   
            print("sur",str(plan.start_date)[:10])
            days.add(day_start)

    days = list(days)
    days.sort()
    for lampe in lampes:
        my_lampe = Lampe.objects.get(id=lampe.id)
        print(f"lampe id = {my_lampe}")
        planifications = Planification.objects.filter(lampe=my_lampe) #nejib fel data mel bd
        
        data_for_day_single_lampe = []
        for day in days:
            cons = 0
            for plan in planifications:
                if str(plan.start_date)[:10]==day:# nehseb consommation mte3  date eli hchti bih
                    cons += get_hours_difference(str(plan.start_date),str(plan.end_date)) * plan.lampe.puissance# terje3li nbr swie3
            data_for_day_single_lampe.append(cons)
        data_for_day.append(data_for_day_single_lampe)
    print("hyhyhy",data_for_day)
   
    final_data = []
    for j in range(len(data_for_day[0])):
        x = 0
        for i in range(len(data_for_day)):
            x += data_for_day[i][j]
        final_data.append(x/len(data_for_day))# nehseb consommation totale mte3  noeud  khw ()
            
    return final_data, days
                




def get_data_for_node_for_specific_date_week(node_name, date1, date2):
    lampes = get_lampes_by_noeud_name(node_name) #te3ith noeud 1 yerje3lek les lampes lkoul eli tb3in noeud 1
    print("=====",lampes[0],"==========")
    data_for_week = []
    planifications = Planification.objects.all() #nejib fel data mel bd
    weeks = set() #tekhbi fyha hajet unique
    for plan  in planifications:
        if(((date1 != None and  date2!=None) and (date1 <= str(plan.start_date)[:10] and date2 >= str(plan.start_date)[:10])) or (date1 == None and  date2==None)):
            week_start = str(plan.start_date)[:4] + str(get_week_number(str(plan.start_date)[8:10],str(plan.start_date)[5:7])) # 2023-02, 2024-02-10
            weeks.add(week_start)

    weeks = list(weeks)
    weeks.sort()
    for lampe in lampes:
        my_lampe = Lampe.objects.get(id=lampe.id)
        planifications = Planification.objects.filter(lampe=my_lampe) #nejib fel data mel bd
        
        data_for_week_single_lampe = []
        for week in weeks:
            cons = 0
            for plan in planifications:
                if str(plan.start_date)[:4]+str(int(str(plan.start_date)[8:10]))==week:# nehseb consommation mte3  date eli hchti bih
                    cons += get_hours_difference(str(plan.start_date),str(plan.end_date)) * plan.lampe.puissance# terje3li nbr swie3
            data_for_week_single_lampe.append(cons)
        data_for_week.append(data_for_week_single_lampe)
   
    final_data = []
    for j in range(len(data_for_week[0])):
        x = 0
        for i in range(len(data_for_week)):
            x += data_for_week[i][j]
        final_data.append(x/len(data_for_week))# nehseb consommation totale mte3  noeud  khw ()
            
    return final_data,weeks


