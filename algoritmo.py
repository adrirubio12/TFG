import pandas as pd
import random


def inicializar(edad, altura, peso, sexo, nivel_actividad, objetivos):
    df_alimentos = pd.read_csv("data/BaseDatosAlimentos.csv", on_bad_lines="skip")
    df_ejercicios = pd.read_csv("data/BaseDatosGym.csv", on_bad_lines="skip")
    tmb = calcular_tmb(edad, altura, peso, sexo)
    ne = calcular_necesidades_energeticas(tmb, nivel_actividad)
    macros = obtener_macronutrientes(nivel_actividad, objetivos)
    alimentos_seleccionados = buscar_alimentos(df_alimentos, macros)
    rutina = generar_rutina(df_ejercicios, nivel_actividad)
    return alimentos_seleccionados, ne, rutina


def calcular_tmb(edad, altura, peso, sexo):
    if sexo == "masculino":
        return (10 * peso) + (6.25 * altura) - (5 * edad) + 5
    elif sexo == "femenino":
        return (10 * peso) + (6.25 * altura) - (5 * edad) - 161


def calcular_necesidades_energeticas(tmb, nivel_actividad):
    factores_actividad = {
        "sedentario": 1.2,
        "ligero": 1.375,
        "moderado": 1.55,
        "intenso": 1.725,
        "extremo": 1.9,
    }

    if nivel_actividad not in factores_actividad:
        raise ValueError("error")

    return tmb * factores_actividad[nivel_actividad]


def obtener_tipo_rutina(nivel_actividad):
    rutinas = {
        "sedentario": "Cuerpo completo",
        "ligero": "Torso/pierna",
        "moderado": "Push-Pull-Legs",
        "intenso": "Push-Pull-Legs",
        "extremo": "División por grupos musculares o Weider",
    }

    if nivel_actividad not in rutinas:
        raise ValueError("error")

    return rutinas[nivel_actividad]


def obtener_macronutrientes(nivel_actividad, objetivo):
    porcentajes_macros = {
        "sedentario": {
            "perdida peso": {"HC": 45, "P": 35, "G": 20},
            "ganancia muscular": {"HC": 50, "P": 30, "G": 20},
            "mantenimiento": {"HC": 50, "P": 20, "G": 30},
            "mejora salud": {"HC": 50, "P": 20, "G": 30},
        },
        "ligero": {
            "perdida peso": {"HC": 45, "P": 30, "G": 25},
            "ganancia muscular": {"HC": 55, "P": 25, "G": 20},
            "mantenimiento": {"HC": 50, "P": 25, "G": 25},
            "mejora salud": {"HC": 50, "P": 25, "G": 25},
        },
        "moderado": {
            "perdida peso": {"HC": 45, "P": 30, "G": 25},
            "ganancia muscular": {"HC": 60, "P": 25, "G": 15},
            "mantenimiento": {"HC": 55, "P": 25, "G": 20},
            "mejora salud": {"HC": 55, "P": 25, "G": 20},
        },
        "intenso": {
            "perdida peso": {"HC": 50, "P": 30, "G": 20},
            "ganancia muscular": {"HC": 60, "P": 25, "G": 15},
            "mantenimiento": {"HC": 60, "P": 20, "G": 20},
            "mejora salud": {"HC": 60, "P": 20, "G": 20},
        },
        "extremo": {
            "perdida peso": {"HC": 50, "P": 30, "G": 20},
            "ganancia muscular": {"HC": 65, "P": 25, "G": 10},
            "mantenimiento": {"HC": 65, "P": 20, "G": 15},
            "mejora salud": {"HC": 65, "P": 20, "G": 15},
        },
    }

    return porcentajes_macros[nivel_actividad][objetivo]


def obtener_imagen(nivel_actividad, objetivo):
    fotos = {
        "sedentario": {
            "perdida peso": "assets/1.png",
            "ganancia muscular": "assets/2.png",
            "mantenimiento": "assets/3.png",
            "mejora salud": "assets/3.png",
        },
        "ligero": {
            "perdida peso": "assets/4.jpg",
            "ganancia muscular": "assets/5.jpg",
            "mantenimiento": "assets/6.jpg",
            "mejora salud": "assets/6.jpg",
        },
        "moderado": {
            "perdida peso": "assets/4.png",
            "ganancia muscular": "assets/7.png",
            "mantenimiento": "assets/5.png",
            "mejora salud": "assets/5.png",
        },
        "intenso": {
            "perdida peso": "assets/2.png",
            "ganancia muscular": "assets/7.png",
            "mantenimiento": "assets/8.png",
            "mejora salud": "assets/8.png",
        },
        "extremo": {
            "perdida peso": "assets/2.png",
            "ganancia muscular": "assets/9.png",
            "mantenimiento": "assets/10.png",
            "mejora salud": "assets/10.png",
        },
    }

    return fotos[nivel_actividad][objetivo]


def buscar_alimentos(df, macros_objetivo):
    # Calcular calorías para cada macronutriente
    df["Calorias_HC"] = df["Carbohydrt_(g)"] * 4
    df["Calorias_P"] = df["Protein_(g)"] * 4
    df["Calorias_G"] = df["Lipid_Tot_(g)"] * 9

    # Calcular total de calorías por alimento
    df["Calorias_Totales"] = df["Calorias_HC"] + df["Calorias_P"] + df["Calorias_G"]

    # Calcular porcentajes de macronutrientes para cada alimento
    df["Porcentaje_HC"] = (df["Calorias_HC"] / df["Calorias_Totales"]) * 100
    df["Porcentaje_P"] = (df["Calorias_P"] / df["Calorias_Totales"]) * 100
    df["Porcentaje_G"] = (df["Calorias_G"] / df["Calorias_Totales"]) * 100

    # Numero que define un rango aceptable de margen
    rango = 4

    # Filtrar alimentos que se ajusten a los porcentajes deseados
    alimentos_seleccionados = df[
        (
            df["Porcentaje_HC"].between(
                macros_objetivo["HC"] - rango, macros_objetivo["HC"] + rango
            )
        )
        & (
            df["Porcentaje_P"].between(
                macros_objetivo["P"] - rango, macros_objetivo["P"] + rango
            )
        )
        & (
            df["Porcentaje_G"].between(
                macros_objetivo["G"] - rango, macros_objetivo["G"] + rango
            )
        )
    ]

    return alimentos_seleccionados


# Listas de vitaminas, minerales 
vitaminas = [
    "Vit_C_(mg)",
    "Thiamin_(mg)",
    "Riboflavin_(mg)",
    "Niacin_(mg)",
    "Panto_Acid_mg)",
    "Vit_B6_(mg)",
    "Folate_Tot_(µg)",
    "Folic_Acid_(µg)",
    "Food_Folate_(µg)",
    "Folate_DFE_(µg)",
    "Choline_Tot_ (mg)",
    "Vit_B12_(µg)",
    "Vit_A_IU",
    "Vit_A_RAE",
    "Retinol_(µg)",
    "Alpha_Carot_(µg)",
    "Beta_Carot_(µg)",
    "Beta_Crypt_(µg)",
    "Lycopene_(µg)",
    "Lut+Zea_ (µg)",
    "Vit_E_(mg)",
    "Vit_D_µg",
    "Vit_D_IU",
    "Vit_K_(µg)",
]

minerales = [
    "Calcium_(mg)",
    "Iron_(mg)",
    "Magnesium_(mg)",
    "Phosphorus_(mg)",
    "Potassium_(mg)",
    "Sodium_(mg)",
    "Zinc_(mg)",
    "Copper_mg)",
    "Manganese_(mg)",
    "Selenium_(µg)",
]
musculos = [
    "Abdominals",
    "Adductors",
    "Abductors",
    "Biceps",
    "Calves",
    "Chest",
    "Forearms",
    "Glutes",
    "Hamstrings",
    "Lats",
    "Lower Back",
    "Middle Back",
    "Traps",
    "Neck",
    "Quadriceps",
    "Shoulders",
    "Triceps",
]


def filtro_V_M(df, Vit_Min):
    alimentos_elegidos = []
    micronutrientes_cubiertos = set()
    micronutrientes_no_encontrados = []

    for micronutrientes in Vit_Min:
        # Buscar un alimento con valor no cero de ese micronutrientes
        alimentos_con_micronutrientes = df[df[micronutrientes] > 0]

        if alimentos_con_micronutrientes.empty:
            # Si no se encuentra un alimento con el micronutrientes, agrega el nutriente a la lista de no encontrados
            micronutrientes_no_encontrados.append(micronutrientes)
            continue

        alimento_micronutriente = alimentos_con_micronutrientes.iloc[0]
        
        # Agregar el alimento a la lista y actualiza el conjunto de micronutrientes cubiertos
        alimentos_elegidos.append(alimento_micronutriente)
        for nut in Vit_Min:
            if alimento_micronutriente[nut] > 0:
                micronutrientes_cubiertos.add(nut)

        # Eliminar el alimento del dataframe
        df = df.drop(alimento_micronutriente.name)

    return alimentos_elegidos, df


def generar_dieta(alimentos_seleccionados):
    # Seleccionar alimentos basados en vitaminas y minerales
    alimentos_vitaminas, alimentos_restantes = filtro_V_M(
        alimentos_seleccionados, vitaminas
    )
    alimentos_minerales, alimentos_restantes = filtro_V_M(
        alimentos_restantes, minerales
    )

    # Combinar las listas de alimentos seleccionados
    alimentos_elegidos = alimentos_vitaminas + alimentos_minerales

    # Rellenar con alimentos al azar
    cantidad_faltante = 70 - len(alimentos_elegidos)

    # Limitamos el tamaño de la muestra para no exceder la cantidad disponible
    tamaño_muestra = min(cantidad_faltante, len(alimentos_restantes.index))

    alimentos_aleatorios = random.sample(
        list(alimentos_restantes.index), tamaño_muestra
    )
    for idx in alimentos_aleatorios:
        alimentos_elegidos.append(alimentos_seleccionados.loc[idx])

    # Dividir en grupos de 10
    dieta = [
        alimentos_elegidos[i : i + 10] for i in range(0, len(alimentos_elegidos), 10)
    ]

    dieta_formato = []
    # Itera a través de cada grupo de alimentos en la dieta
    for grupo in dieta:
        grupo_formato = []
        for alimento in grupo:
            grupo_formato.append(
                {"nombre": alimento["Shrt_Desc"], "kcal": alimento["Energ_Kcal"]}
            )
        dieta_formato.append(grupo_formato)
    return dieta_formato


def generar_rutina(df_ejercicios, nivel_actividad):
    # Definir prioridad de nivel según nivel_actividad
    if nivel_actividad in ["sedentario", "ligero"]:
        priority_levels = ["Beginner", "Intermediate"]
    elif nivel_actividad == "extremo":
        priority_levels = ["Expert", "Intermediate"]
    else:
        priority_levels = ["Intermediate", "Beginner"]

    # Construir rutina
    rutina = {}

    for musculo in musculos:
        ejercicios_musculo = df_ejercicios[df_ejercicios["BodyPart"] == musculo]
        ejercicios_seleccionados = []

        for level in priority_levels:
            ejercicios_level = ejercicios_musculo[ejercicios_musculo["Level"] == level]

            # Ordenar por Rating (y descartar aquellos sin valor en 'Rating')
            ejercicios_level = ejercicios_level.dropna(subset=["Rating"]).sort_values(
                by="Rating", ascending=False
            )

            # Agregar ejercicios al listado hasta completar 20
            for _, row in ejercicios_level.iterrows():
                if len(ejercicios_seleccionados) < 20:
                    ejercicios_seleccionados.append(row["Title"])
                else:
                    break

        rutina[musculo] = ejercicios_seleccionados

    return rutina
