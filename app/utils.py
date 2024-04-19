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



def get_data_for_node_for_specific_date(node_name, period):
    if period == "year":
        get_data_for_node_for_specific_date_year(node_name, period)
        
        


def get_data_for_node_for_specific_date_year(node_name, period):
    lampes = get_lampes_by_noeud_name(node_name)
    data_for_year = []
    for lampe in lampes:
        my_lampe = Lampe.objects.get(id=lampe.id)
        planifications = Planification.objects.filter(lampe=my_lampe)
        years = set()
        for plan  in planifications:
            print("plan",plan)
            year_start = str(plan.start_date)[:4]
            print("year_start",year_start)
            years.add(year_start)
        years = ["2024","2025"]
        years.sort()
        data_for_year_single_lampe = []
        for year in years:
            cons = 0
            for plan in planifications:
                if str(plan.start_date)[:4]==year:
                    cons += get_hours_difference(str(plan.start_date),str(plan.end_date)) * plan.lampe.puissance
            data_for_year_single_lampe.append(cons)
        data_for_year.append(data_for_year_single_lampe)
    print("hyhyhy",data_for_year)
    final_data = []
    for j in range(len(data_for_year[0])):
        x = 0
        for i in range(len(data_for_year)):
            x += data_for_year[i][j]
        final_data.append(x/len(data_for_year))
            
    return ("annee", final_data)   
                
    
print("little pig little pig let me in", get_data_for_node_for_specific_date_year("test","y"))

