"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    import re
    import pandas as pd
    
    # Leer el archivo
    with open('files/input/clusters_report.txt', 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    clusters_data = []
    current_cluster = None
    
    for line in lines:
        # Buscar línea de cluster: "   N     XXX             YY,Y %          keywords..."
        cluster_match = re.match(r'^\s*(\d+)\s+(\d+)\s+([\d,]+)\s+%\s+(.*)', line)
        
        if cluster_match:
            if current_cluster is not None:
                clusters_data.append(current_cluster)
            
            cluster_num, cantidad, porcentaje, keywords = cluster_match.groups()
            current_cluster = {
                'cluster': int(cluster_num),
                'cantidad': int(cantidad),
                'porcentaje': porcentaje,
                'keywords': [keywords] if keywords.strip() else []
            }
        elif current_cluster is not None and line.strip() and not line.startswith('--'):
            # Las líneas de continuación están indentadas con muchos espacios
            if line.startswith(' ' * 40):
                current_cluster['keywords'].append(line.strip())
    
    # No olvides guardar el último cluster
    if current_cluster is not None:
        clusters_data.append(current_cluster)
    
    # Procesar los datos
    data = []
    for cluster in clusters_data:
        # Consolidar las palabras clave
        keywords_str = ' '.join(cluster['keywords'])
        # Limpiar espacios múltiples
        keywords_str = re.sub(r'\s+', ' ', keywords_str)
        # Remover el punto final
        if keywords_str.endswith('.'):
            keywords_str = keywords_str[:-1]
        
        # Convertir porcentaje
        porcentaje_float = float(cluster['porcentaje'].replace(',', '.'))
        
        data.append({
            'cluster': cluster['cluster'],
            'cantidad_de_palabras_clave': cluster['cantidad'],
            'porcentaje_de_palabras_clave': porcentaje_float,
            'principales_palabras_clave': keywords_str
        })
    
    return pd.DataFrame(data)
