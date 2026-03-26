import gradio as gr

# Conversion factors to base unit
CATEGORIES = {
    "Longueur": {
        "base": "Mètre (m)",
        "units": {
            "Kilomètre (km)": 1000,
            "Mètre (m)": 1,
            "Centimètre (cm)": 0.01,
            "Millimètre (mm)": 0.001,
            "Mile (mi)": 1609.344,
            "Yard (yd)": 0.9144,
            "Pied (ft)": 0.3048,
            "Pouce (in)": 0.0254,
            "Mille marin (nmi)": 1852,
        }
    },
    "Masse": {
        "base": "Kilogramme (kg)",
        "units": {
            "Tonne (t)": 1000,
            "Kilogramme (kg)": 1,
            "Gramme (g)": 0.001,
            "Milligramme (mg)": 0.000001,
            "Livre (lb)": 0.45359237,
            "Once (oz)": 0.028349523,
        }
    },
    "Température": {
        "base": "Celsius (°C)",
        "units": {
            "Celsius (°C)": "C",
            "Fahrenheit (°F)": "F",
            "Kelvin (K)": "K",
        }
    },
    "Vitesse": {
        "base": "m/s",
        "units": {
            "km/h": 1/3.6,
            "m/s": 1,
            "mph": 0.44704,
            "Nœud (kn)": 0.514444,
            "Mach": 340.29,
        }
    },
    "Surface": {
        "base": "m²",
        "units": {
            "km²": 1e6,
            "m²": 1,
            "cm²": 0.0001,
            "Hectare (ha)": 10000,
            "Acre": 4046.856,
            "mi²": 2589988.1,
            "ft²": 0.092903,
        }
    },
}

def get_units(category):
    return list(CATEGORIES[category]["units"].keys())

def convert_temp(val, from_unit, to_unit):
    units = CATEGORIES["Température"]["units"]
    from_k = units[from_unit]
    to_k = units[to_unit]
    if from_k == "C":
        celsius = val
    elif from_k == "F":
        celsius = (val - 32) * 5 / 9
    else:
        celsius = val - 273.15
    if to_k == "C":
        return celsius
    elif to_k == "F":
        return celsius * 9 / 5 + 32
    else:
        return celsius + 273.15

def convert(value, category, from_unit, to_unit):
    try:
        val = float(value)
    except (ValueError, TypeError):
        return "Valeur invalide"

    if category == "Température":
        result = convert_temp(val, from_unit, to_unit)
    else:
        units = CATEGORIES[category]["units"]
        result = val * units[from_unit] / units[to_unit]

    if abs(result) >= 0.001 and abs(result) < 1e7:
        formatted = f"{float(f'{result:.6g}')}"
    else:
        formatted = f"{result:.4e}"

    return f"{formatted} {to_unit.split('(')[0].strip()}"

def update_units(category):
    units = get_units(category)
    return (
        gr.Dropdown(choices=units, value=units[0]),
        gr.Dropdown(choices=units, value=units[1] if len(units) > 1 else units[0]),
    )

with gr.Blocks(title="Convertisseur d'unités") as demo:
    gr.Markdown("# Convertisseur d'unités")
    gr.Markdown("Convertissez facilement entre différentes unités de mesure.")

    with gr.Row():
        category = gr.Dropdown(
            choices=list(CATEGORIES.keys()),
            value="Longueur",
            label="Catégorie",
            scale=1,
        )

    default_units = get_units("Longueur")

    with gr.Row():
        value_input = gr.Number(value=1, label="Valeur", scale=1)
        from_unit = gr.Dropdown(choices=default_units, value=default_units[0], label="De", scale=1)
        to_unit = gr.Dropdown(choices=default_units, value=default_units[1], label="Vers", scale=1)

    result = gr.Textbox(label="Résultat", interactive=False, scale=1)

    convert_btn = gr.Button("Convertir", variant="primary")

    category.change(fn=update_units, inputs=category, outputs=[from_unit, to_unit])
    convert_btn.click(fn=convert, inputs=[value_input, category, from_unit, to_unit], outputs=result)
    value_input.change(fn=convert, inputs=[value_input, category, from_unit, to_unit], outputs=result)
    from_unit.change(fn=convert, inputs=[value_input, category, from_unit, to_unit], outputs=result)
    to_unit.change(fn=convert, inputs=[value_input, category, from_unit, to_unit], outputs=result)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False, theme=gr.themes.Soft())
