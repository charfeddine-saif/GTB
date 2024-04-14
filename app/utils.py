# utils.py
from collections import defaultdict
from .models import Noeud, Lampe, Planification

from django.utils import timezone
import threading
import time
from datetime import datetime


def get_lampes_by_noeud_name(noeud_name):
    try:
        # Get the Noeud object with the given name
        # noeud = Noeud.objects.get(name=noeud_name)
        # # # Retrieve all the Lampe objects associated with the Noeud
        # lampes = Lampe.objects.filter(noeud=noeud)
        return []
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
        pass
        