# -*- coding: utf-8 -*-
"""
Created on Thu Sep 18 08:22:10 2025

@author: yefri
"""

import random
import math

ciudades = {
    'A': (0,0),
    'B': (1,5),
    'C': (2,3),
    'D': (5,2),
    'E': (6,6),
    'F': (7,1),
    'G': (8,4),
    'H': (9,9)  
}

def distancia_ruta(ruta):
    """Calcular la distancia total de la ruta"""
    total = 0
    for i in range(len(ruta)):
        ciudad_actual = ruta[i]
        ciudad_siguiente = ruta[(i + 1) % len(ruta)]  # Volver al inicio si es la última ciudad
        x1, y1 = ciudades[ciudad_actual]
        x2, y2 = ciudades[ciudad_siguiente]
        total += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return total

def crear_poblacion_inicial(tam_poblacion):
    """Crear población inicial de rutas aleatorias"""
    poblacion = []
    ciudades_lista = list(ciudades.keys())
    for _ in range(tam_poblacion):
        ruta = ciudades_lista.copy()
        random.shuffle(ruta)
        poblacion.append(ruta)
    return poblacion

def seleccion(poblacion, distancias):
    """Implementar selección por torneo"""
    torneo_tam = 3
    seleccionados = []
    for _ in range(len(poblacion)):
        torneo = random.sample(list(zip(poblacion, distancias)), torneo_tam)
        ganador = min(torneo, key=lambda x: x[1])[0]
        seleccionados.append(ganador.copy())
    return seleccionados

def cruce(padre1, padre2):
    """Implementar cruce ordenado (OX)"""
    tam = len(padre1)
    inicio, fin = sorted(random.sample(range(tam), 2))
    
    # Tomar segmento del padre1
    hijo = [None] * tam
    for i in range(inicio, fin + 1):
        hijo[i] = padre1[i]
    
    # Completar con ciudades del padre2 en orden
    pos_hijo = (fin + 1) % tam
    pos_padre2 = (fin + 1) % tam
    while None in hijo:
        if padre2[pos_padre2] not in hijo:
            hijo[pos_hijo] = padre2[pos_padre2]
            pos_hijo = (pos_hijo + 1) % tam
        pos_padre2 = (pos_padre2 + 1) % tam
    
    return hijo

def mutacion(ruta, tasa_mutacion):
    """Implementar mutación por intercambio"""
    ruta = ruta.copy()
    if random.random() < tasa_mutacion:
        i, j = random.sample(range(len(ruta)), 2)
        ruta[i], ruta[j] = ruta[j], ruta[i]
    return ruta

def algoritmo_genetico(tam_poblacion=100, generaciones=1000, tasa_mutacion=0.1):
    """Algoritmo genético principal para resolver el TSP"""
    # Inicializar población
    poblacion = crear_poblacion_inicial(tam_poblacion)
    
    # Variables para tracking de la mejor solución
    mejor_ruta = None
    mejor_distancia = float('inf')
    
    for _ in range(generaciones):
        # Calcular distancias de todas las rutas
        distancias = [distancia_ruta(ruta) for ruta in poblacion]
        
        # Actualizar mejor solución
        min_distancia = min(distancias)
        if min_distancia < mejor_distancia:
            mejor_distancia = min_distancia
            mejor_ruta = poblacion[distancias.index(min_distancia)].copy()
        
        # Selección
        nueva_poblacion = seleccion(poblacion, distancias)
        
        # Cruce
        for i in range(0, tam_poblacion, 2):
            if i + 1 < tam_poblacion and random.random() < 0.8:  # Tasa de cruce
                nueva_poblacion[i], nueva_poblacion[i+1] = (
                    cruce(nueva_poblacion[i], nueva_poblacion[i+1]),
                    cruce(nueva_poblacion[i+1], nueva_poblacion[i])
                )
        
        # Mutación
        nueva_poblacion = [mutacion(ruta, tasa_mutacion) for ruta in nueva_poblacion]
        
        # Actualizar población
        poblacion = nueva_poblacion
    
    return mejor_ruta, mejor_distancia

if __name__ == "__main__":
    # Ejecutar el algoritmo
    mejor_ruta, mejor_distancia = algoritmo_genetico()
    print(f"Mejor ruta encontrada: {mejor_ruta}")
    print(f"Distancia total: {mejor_distancia:.2f}")