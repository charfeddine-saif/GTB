# utils.py
from collections import defaultdict
from .models import Noeud, Lampe, Planification

from django.utils import timezone
import threading
import time


from datetime import datetime


def get_hours_difference(start_date_str, end_date_str):
    
    # Parse start_date and end_date strings into datetime objects
    start_date = datetime.fromisoformat(start_date_str[:-6])  # Strip timezone information (+00:00) for parsing
    end_date = datetime.fromisoformat(end_date_str[:-6])  # Strip timezone information (+00:00) for parsing
    
    # Calculate time difference in hours
    time_difference = end_date - start_date
    if  time_difference.days < 0:
        return 0
    difference_in_hours = time_difference.total_seconds() / 3600  # Convert seconds to hours
    
    return difference_in_hours




def get_lampes_by_noeud_name(noeud_name):
    try:
        # Get the Noeud object with the given name
        noeud = Noeud.objects.get(name=noeud_name)
        # # Retrieve all the Lampe objects associated with the Noeud
        lampes = Lampe.objects.filter(noeud=noeud)
        return lampes
    except Noeud.DoesNotExist:
        # Handle the case where the Noeud does not exist
        return None





def get_lampes_by_noeud_id(noeud_id):
    try:
        # Get the Noeud object with the given name
        noeud = Noeud.objects.get(id=noeud_id)
        # # Retrieve all the Lampe objects associated with the Noeud
        lampes = Lampe.objects.filter(noeud=noeud)
        return lampes
    except Noeud.DoesNotExist:
        # Handle the case where the Noeud does not exist
        return None


from collections import defaultdict

def get_nodes_with_lampes():
    all_noeuds = Noeud.objects.all()

    # Create a dictionary to hold the result
    result = defaultdict(list)

    # Iterate over each Noeud
    for noeud in all_noeuds:
        # Retrieve all related Lampe objects for the current Noeud
        related_lampes = Lampe.objects.filter(noeud=noeud)
        
        # Construct an array of lampes' information
        lampes_info = [{'id': str(lampe.id), 'name': lampe.name, 'puissance': lampe.puissance} for lampe in related_lampes]
        
        # Add the current Noeud's name, ID, and related lampes' information to the result dictionary
        result[noeud.name] = {'id': str(noeud.id), 'lampes': lampes_info}

    # Convert the result dictionary to a list of dictionaries
    return [{'noeud_name': noeud_name, 'id': info['id'], 'lampes': info['lampes']} for noeud_name, info in result.items()]




    
def autoUpdateStatus():
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


def get_data_for_node_for_specific_date(node_name, period):
    if period == "year":
        get_data_for_node_for_specific_date_year(node_name, period)
    



def get_data_for_node_for_specific_date_year(node_name, period):
    lampes = get_lampes_by_noeud_name(node_name) #te3ith noeud 1 yerje3lek les lampes lkoul eli tb3in noeud 1
    print("=====",lampes[0],"==========")
    data_for_year = []
    planifications = Planification.objects.all() #nejib fel data mel bd
    years = set() #tekhbi fyha hajet unique
    for plan  in planifications:
        print("plan",plan)
        year_start = str(plan.start_date)[:4] # 2023-02, 2024-02
        print("year_start",year_start)
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
            
    return ("annee", final_data)
                


print("little pig little pig let me in", get_data_for_node_for_specific_date_year("test","y"))
   
   
   
#[[150,50],[125,15],[140,200]]
# [ , ]




#def get_data_for_node_for_specific_date_month(node_name, period):
    #lampes = get_lampes_by_noeud_name(node_name)
    #data_for_month = []
    #planifications = Planification.objects.all()
    #months = set()  
    
    #for plan in planifications:
        #date = plan.start_date
        #months.add(date.strftime('%B'))  # Add month name to set of unique months

    #months = sorted(months)  
    
    #data_for_month = []
    #for lampe in lampes:
        #my_lampe = Lampe.objects.get(id=lampe.id)
        #planifications = Planification.objects.filter(lampe=my_lampe)
        
        #data_for_single_lampe = []
        #for month in months:
            #cons = 0
            #for plan in planifications:
                #if plan.start_date.month == date.month:  
                    #cons += get_hours_difference(plan.start_date, plan.end_date) * plan.lampe.puissance
            #data_for_single_lampe.append(cons)
        #data_for_month.append(data_for_single_lampe)

    #final_data = []
    #for j in range(len(data_for_month[0])):
        #x = 0
        #for i in range(len(data_for_month)):
            #x += data_for_month[i][j]
        #final_data.append(x / len(data_for_month))
    
    #return ("mois", final_data)

#result = get_data_for_node_for_specific_date_month("test", "y")
#print(result)







# def get_data_for_node_for_specific_date_month(node_name, period):
#     lampes = get_lampes_by_noeud_name(node_name) #te3ith noeud 1 yerje3lek les lampes lkoul eli tb3in noeud 1
#     data_for_months = []
#     planifications = Planification.objects.all() #nejib fel data mel bd
#     months = set()  # Cet ensemble stockera des dates uniques au format "YYYY-MM"
#     for plan in planifications:
#         year_month = str(plan.start_date)[:7]  # Obtenez l'année et le mois au format "YYYY-MM"
#         print(year_month)
#         print( months.add(year_month))
#     sorted_months = sorted(months)  # Triez les dates au format "YYYY-MM"
#     print(sorted_months)          # Affichez la liste triée des années et mois uniques
#         #years.add(year_start)
#         #years = list(years)
#         #years.sort()
#     for lampe in lampes:
#         my_lampe = Lampe.objects.get(id=lampe.id)
#         planifications = Planification.objects.filter(lampe=my_lampe) #nejib fel data mel bd
        
#         data_for_month_single_lampe = []
#         for month in months:
#             cons = 0
#             for plan in planifications:
#                 if str(plan.start_date)[:7]==month:# nehseb consommation mte3  date eli hchti bih
#                     cons += get_hours_difference(str(plan.start_date),str(plan.end_date)) * plan.lampe.puissance# terje3li nbr swie3
#             data_for_month_single_lampe.append(cons)
#         data_for_month.append(data_for_single_lampe)
#     print("hyhyhy",data_for_month)
   
#     final_data = []
#     for j in range(len(data_for_month[0])):
#         x = 0
#         for i in range(len(data_for_month)):
#             x += data_for_year[i][j]
#         final_data.append(x/len(data_for_year))# nehseb consommation totale mte3  noeud  khw ()
            
#     return ("mois", final_data)
                


# print("little pig little pig let me in", get_data_for_node_for_specific_date_month("test","y"))
   
   
def test(node_name, period):
    lampes = get_lampes_by_noeud_name(node_name) #te3ith noeud 1 yerje3lek les lampes lkoul eli tb3in noeud 1
    data_for_month = []
    planifications = Planification.objects.all() #nejib fel data mel bd
    months = set() #tekhbi fyha hajet unique
    for plan  in planifications:
        print("plan",plan)
        month_start = str(plan.start_date)[:7] # 2023-02, 2024-02
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
            
    return ("month", final_data)

print("little pig little pig let me in", test("test","y"))
# print("little pig little pig let me in year", get_data_for_node_for_specific_date_year("test","y"))










  # def get_data_for_node_for_specific_date_month(node_name, period):
        # Récupère les lampes associées au nœud spécifié
   # lampes = get_lampes_by_noeud_name(node_name)

    # Liste vide pour stocker les données par mois
    #data_for_month = []

    # Récupère toutes les planifications dans la base de données
    #planifications = Planification.objects.all()

    # Ensemble pour stocker les mois uniques
    #months = set()  # Ensemble pour collecter les mois uniques

    # Parcourt toutes les planifications pour extraire les mois uniques
    #for plan in planifications:
        # Supposons que plan.start_date est déjà un objet datetime
        #date = plan.start_date
        # Extrait le mois de l'objet datetime et l'ajoute à l'ensemble des mois uniques
        #months.add(date.strftime('%B'))  # Ajoute le nom du mois à l'ensemble des mois uniques

    # Trie les mois par ordre alphabétique
    #months = sorted(months)  # Trie les mois par ordre alphabétique
      
    # Liste vide pour stocker les données par lampe et par mois
    #data_for_month = []

    # Parcourt chaque lampe associée au nœud
    #for lampe in lampes:
        # Récupère l'objet Lampe correspondant à partir de son ID
        #my_lampe = Lampe.objects.get(id=lampe.id)
        
        # Récupère toutes les planifications pour cette lampe
        #planifications = Planification.objects.filter(lampe=my_lampe)
        
        # Liste pour stocker la consommation par mois pour cette lampe
        #data_for_single_lampe = []

        # Parcourt chaque mois dans l'ordre trié
        #for month in months:
            #cons = 0
            # Parcourt chaque planification pour cette lampe
            #for plan in planifications:
                # Vérifie si le mois de la planification correspond au mois actuel dans la boucle
                #if plan.start_date.strftime('%B') == month:
                    # Calcule la consommation en heures
                    #cons += get_hours_difference(plan.start_date, plan.end_date) * plan.lampe.puissance
            # Ajoute la consommation pour ce mois à la liste de données pour cette lampe
            #data_for_single_lampe.append(cons)

        # Ajoute les données de consommation par mois pour cette lampe à la liste principale
        #data_for_month.append(data_for_single_lampe)

    # Liste finale pour stocker les moyennes de consommation par mois pour toutes les lampes
    #final_data = []

    # Parcourt chaque index (mois) dans les données par mois
    #for j in range(len(data_for_month[0])):
        #x = 0
        # Parcourt chaque lampe dans les données par lampe
        #for i in range(len(data_for_month)):
            # Ajoute la consommation pour ce mois et cette lampe à x
            #x += data_for_month[i][j]
        # Calcule la moyenne de la consommation pour ce mois sur toutes les lampes
        #final_data.append(x / len(data_for_month))
    
    # Retourne une paire de valeurs (mois, moyenne de consommation pour ce mois)
    #return ("mois", final_data)

# Appel de la fonction avec des valeurs spécifiques
#result = get_data_for_node_for_specific_date_month("test", "y")
#print(result)

   





#def get_data_for_node_for_specific_date_month (node_name, period):
    #lampes = get_lampes_by_noeud_name(node_name) #te3ith noeud 1 yerje3lek les lampes lkoul eli tb3in noeud 1
    #data_for_month = []
    #planifications = Planification.objects.all() #nejib fel data mel bd
    #years = set() #tekhbi fyha hajet unique
    #for plan  in planifications:
        #print("plan",plan)
        #year_start = str(plan.start_date)[:4] # 2023-02, 2024-02
        #year_start = int(year_start)  # Convertit l'année en entier pour effectuer des opérations arithmétiques
        #print("year_start",year_start)
        #years.add(year_start)
        #months_in_year = list(range(1, 13))  # Liste des mois en format numérique (1 pour janvier, 2 pour février, etc.) 
         
    #for month in months_in_year:
        #print(month)# Affiche uniquement le numéro du mois pour chaque mois de l'année

    #years.sort()
    #for lampe in lampes:
        #my_lampe = Lampe.objects.get(id=lampe.id)
        #planifications = Planification.objects.filter(lampe=my_lampe) #nejib fel data mel bd
        
        #data_for_year_single_lampe = []
        #for year in years:
            #cons = 0
            #for plan in planifications:
                #if str(plan.start_date)[:4]==year:# nehseb consommation mte3  date eli hchti bih
                    #cons += get_hours_difference(str(plan.start_date),str(plan.end_date)) * plan.lampe.puissance# terje3li nbr swie3
            #data_for_year_single_lampe.append(cons)
        #data_for_year.append(data_for_year_single_lampe)
    #print("hyhyhy",data_for_year)
   
    #final_data = []
    #for j in range(len(data_for_year[0])):
        #x = 0
        #for i in range(len(data_for_year)):
            #x += data_for_year[i][j]
        #final_data.append(x/len(data_for_year))# nehseb consommation totale mte3  noeud  khw ()
            
    #return ("annee", final_data)
                


#print("little pig little pig let me in", get_data_for_node_for_specific_date_year("test","y"))





#def get_data_for_node_for_specific_month(node_name, month):
    #lampes = get_lampes_by_noeud_name(node_name)  # Récupérer les lampes associées au nœud
      #data_for_month = []
    #planifications = Planification.objects.filter(start_date__year=year)  # Filtrer les planifications pour l'année spécifiée

    #months = {str(i): 0 for i in range(1, 13)}  # Initialiser les mois avec une consommation de 0

    #for lampe in lampes:
        #my_lampe = Lampe.objects.get(id=lampe.id)
        #planifications_lampe = planifications.filter(lampe=my_lampe)  # Filtrer les planifications pour chaque lampe

        #for plan in planifications_lampe:
            #month_start = str(plan.start_date)[5:7]  # Extraire le mois de la date de début
            #if month_start[0] == '0':  # Enlever le zéro initial si le mois est < 10
                #month_start = month_start[1]
            #cons = get_hours_difference(str(plan.start_date), str(plan.end_date)) * plan.lampe.puissance
            #months[month_start] += cons  # Ajouter la consommation au mois correspondant

    # Convertir les données en liste pour les mois
    #for month in sorted(months.keys()):
        #data_for_month.append(months[month])

    #return ("mois", data_for_month)



#print("little pig little pig let me in", get_data_for_node_for_specific_date_month("test","y"))
   
   




def get_data_for_node_for_specific_date_day(node_name, period):
    lampes = get_lampes_by_noeud_name(node_name) #te3ith noeud 1 yerje3lek les lampes lkoul eli tb3in noeud 1
    print("=====",lampes[0],"==========")
    data_for_day = []
    planifications = Planification.objects.all() #nejib fel data mel bd
    days= set() #tekhbi fyha hajet unique
    for plan  in planifications:
        print("plan",plan)
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
            
    return ("day", final_data)
                


print("little pig little pig let me in", get_data_for_node_for_specific_date_day("test","y"))



