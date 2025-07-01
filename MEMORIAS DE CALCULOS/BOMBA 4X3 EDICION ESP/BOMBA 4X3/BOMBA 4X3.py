import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
import math

def calcular():
    try:
        rpm_motor = float(entry_rpm_motor.get())
        rpm_bomba = float(entry_rpm_bomba.get())
        potencia_hp = float(entry_potencia.get())
        diametro_motor = float(entry_diametro_motor.get())
        distancia_centros = float(entry_distancia_centros.get())

        # Cálculo del diámetro de la polea conducida
        relacion = rpm_motor / rpm_bomba
        diametro_bomba = diametro_motor / relacion

        # Verificación número de canales 5V (capacidad típica por canal: 18.5 HP)
        capacidad_canal = 18.5
        canales_necesarios = math.ceil(potencia_hp / capacidad_canal)

        # Factor de seguridad
        potencia_total_correas = canales_necesarios * capacidad_canal
        fs = potencia_total_correas / potencia_hp

        # Resultados
        resultado.set(f"Diámetro polea bomba: {diametro_bomba:.2f} pulgadas\n"
                      f"Canales necesarios tipo 5V: {canales_necesarios}\n"
                      f"Factor de seguridad: {fs:.2f}")

        # Graficar curva
        plot_curva_bomba(rpm_motor, rpm_bomba)

    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa valores válidos.")

def plot_curva_bomba(rpm_base, rpm_target):
    flow_range = np.linspace(40, 160, 200)
    flow_base = 88
    head_base = 43.8

    def pump_head(Q, Q0=88, H0=43.8):
        return H0 * (1 - ((Q - Q0) / Q0) ** 2)

    head_2020 = pump_head(flow_range, Q0=88, H0=43.8)
    scaling_factor = (rpm_target / 2020) ** 2
    head_target = head_2020 * scaling_factor

    plt.figure(figsize=(8, 5))
    plt.plot(flow_range, head_2020, label="Bomba a 2020 RPM", linestyle='--')
    plt.plot(flow_range, head_target, label=f"Bomba a {rpm_target} RPM", linewidth=2)
    plt.xlabel("Caudal [m³/h]")
    plt.ylabel("Altura manométrica [m]")
    plt.title("Curvas de la bomba WPA43A03")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Interfaz gráfica
root = tk.Tk()
root.title("Cálculo de Transmisión y Curva de Bomba")

mainframe = ttk.Frame(root, padding="10")
mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(mainframe, text="RPM del motor:").grid(column=0, row=0, sticky=tk.W)
entry_rpm_motor = ttk.Entry(mainframe)
entry_rpm_motor.insert(0, "1800")
entry_rpm_motor.grid(column=1, row=0)

ttk.Label(mainframe, text="RPM deseada de la bomba:").grid(column=0, row=1, sticky=tk.W)
entry_rpm_bomba = ttk.Entry(mainframe)
entry_rpm_bomba.insert(0, "1600")
entry_rpm_bomba.grid(column=1, row=1)

ttk.Label(mainframe, text="Potencia del motor (HP):").grid(column=0, row=2, sticky=tk.W)
entry_potencia = ttk.Entry(mainframe)
entry_potencia.insert(0, "75")
entry_potencia.grid(column=1, row=2)

ttk.Label(mainframe, text="Diámetro polea del motor (pulg):").grid(column=0, row=3, sticky=tk.W)
entry_diametro_motor = ttk.Entry(mainframe)
entry_diametro_motor.insert(0, "8.95")
entry_diametro_motor.grid(column=1, row=3)

ttk.Label(mainframe, text="Distancia entre centros (mm):").grid(column=0, row=4, sticky=tk.W)
entry_distancia_centros = ttk.Entry(mainframe)
entry_distancia_centros.insert(0, "620")
entry_distancia_centros.grid(column=1, row=4)

ttk.Button(mainframe, text="Calcular y Graficar", command=calcular).grid(column=0, row=5, columnspan=2, pady=10)

resultado = tk.StringVar()
ttk.Label(mainframe, textvariable=resultado, foreground="blue").grid(column=0, row=6, columnspan=2)

root.mainloop()
