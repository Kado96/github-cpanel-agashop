from datetime import datetime, timedelta
from django.utils.dateparse import parse_datetime
from django.utils import timezone

def safe_parse_datetime(date_str):
    """
    Parse une chaîne de date de manière robuste (ISO ou YYYY-MM-DD).
    Renvoie un objet datetime aware ou None.
    """
    if not date_str:
        return None
    
    # Tentative format ISO (commun via DRF/JS)
    dt = parse_datetime(date_str)
    if dt:
        if timezone.is_naive(dt):
            return timezone.make_aware(dt)
        return dt
        
    # Tentative format date simple YYYY-MM-DD
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return timezone.make_aware(dt)
    except ValueError:
        pass
        
    return None

def parse_date_range(str_du, str_au):
    """
    Prend deux chaînes de caractères et renvoie une plage de recherche 
    (start_dt, end_dt) optimisée pour le filtrage Django.
    """
    start_dt = safe_parse_datetime(str_du)
    end_dt = safe_parse_datetime(str_au)
    
    if end_dt:
        # Si c'était juste une date YYYY-MM-DD, end_dt est à 00:00:00.
        # On le déplace à 23:59:59 pour inclure toute la journée.
        if end_dt.hour == 0 and end_dt.minute == 0 and end_dt.second == 0:
            end_dt = end_dt + timedelta(days=1) - timedelta(seconds=1)
            
    return start_dt, end_dt
