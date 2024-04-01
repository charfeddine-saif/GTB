# utils.py
from collections import defaultdict

from .models import Noeud, Lampe

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


