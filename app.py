import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuración inicial de la página
st.set_page_config(
    page_title="Calculadora de Química Ácido-Base",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 Calculadora Química: pH, Molaridad y Equilibrio")
st.markdown("Herramienta integral para cálculo de soluciones, ácidos/bases y curvas de titulación.")

# Sidebar de navegación
menu = st.sidebar.selectbox(
    "Selecciona la herramienta:",
    [
        "1. pH y pOH (Ácidos/Bases Fuertes y Débiles)",
        "2. Molaridad y Soluciones",
        "3. Constantes de Acidez/Basicidad (Ka, Kb, pKa, pKb)",
        "4. Calculadora de Diluciones (C1V1 = C2V2)",
        "5. Simulador de Curva de Titulación",
        "6. Tabla de Referencia Ka/Kb"
    ]
)

# ---------------------------------------------------------
# MÓDULO 1: pH Y pOH
# ---------------------------------------------------------
if menu == "1. pH y pOH (Ácidos/Bases Fuertes y Débiles)":
    st.header("1. Cálculo de pH y pOH")
    
    tipo_sol = st.radio("Selecciona el tipo de sustancia:", ["Ácido Fuerte", "Base Fuerte", "Ácido Débil", "Base Débil"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        if tipo_sol in ["Ácido Fuerte", "Base Fuerte"]:
            conc = st.number_input("Concentración molar (M):", min_value=1e-14, max_value=10.0, value=0.01, format="%.6f")
            if tipo_sol == "Ácido Fuerte":
                ph = -np.log10(conc)
                poh = 14 - ph
                h_conc = conc
                oh_conc = 10**(-poh)
            else:
                poh = -np.log10(conc)
                ph = 14 - poh
                oh_conc = conc
                h_conc = 10**(-ph)
                
        elif tipo_sol == "Ácido Débil":
            conc = st.number_input("Concentración inicial (M):", min_value=1e-14, max_value=10.0, value=0.1, format="%.6f")
            ka = st.number_input("Constante Ka (ej. 1.8e-5 para ácido acético):", min_value=1e-16, value=1.8e-5, format="%.2e")
            # Resolver x^2 + Ka*x - Ka*C = 0
            a = 1
            b = ka
            c = -ka * conc
            h_conc = (-b + np.sqrt(b**2 - 4*a*c)) / (2*a)
            ph = -np.log10(h_conc)
            poh = 14 - ph
            oh_conc = 10**(-poh)
            
        elif tipo_sol == "Base Débil":
            conc = st.number_input("Concentración inicial (M):", min_value=1e-14, max_value=10.0, value=0.1, format="%.6f")
            kb = st.number_input("Constante Kb (ej. 1.8e-5 para amoníaco):", min_value=1e-16, value=1.8e-5, format="%.2e")
            # Resolver x^2 + Kb*x - Kb*C = 0
            a = 1
            b = kb
            c = -kb * conc
            oh_conc = (-b + np.sqrt(b**2 - 4*a*c)) / (2*a)
            poh = -np.log10(oh_conc)
            ph = 14 - poh
            h_conc = 10**(-ph)

    with col2:
        st.subheader("Resultados:")
        st.metric("pH", f"{ph:.2f}")
        st.metric("pOH", f"{poh:.2f}")
        st.write(f"**[H⁺]:** {h_conc:.2e} M")
        st.write(f"**[OH⁻]:** {oh_conc:.2e} M")

# ---------------------------------------------------------
# MÓDULO 2: MOLARIDAD
# ---------------------------------------------------------
elif menu == "2. Molaridad y Soluciones":
    st.header("2. Calculadora de Molaridad")
    
    opcion_mol = st.selectbox("¿Qué deseas calcular?", ["Molaridad (M)", "Masa de Soluto (g)", "Volumen de Solución (L)"])
    
    if opcion_mol == "Molaridad (M)":
        masa = st.number_input("Masa del soluto (g):", min_value=0.0, value=5.85)
        pm = st.number_input("Peso Molecular / Masa Molar (g/mol):", min_value=0.1, value=58.44)
        vol = st.number_input("Volumen de la solución (L):", min_value=0.001, value=1.0)
        
        if st.button("Calcular Molaridad"):
            moles = masa / pm
            molaridad = moles / vol
            st.success(f"**Molaridad:** {molaridad:.4f} M (mol/L)")
            
    elif opcion_mol == "Masa de Soluto (g)":
        molaridad = st.number_input("Molaridad deseada (M):", min_value=0.0, value=0.1)
        pm = st.number_input("Peso Molecular / Masa Molar (g/mol):", min_value=0.1, value=58.44)
        vol = st.number_input("Volumen de la solución (L):", min_value=0.001, value=0.5)
        
        if st.button("Calcular Masa Necesaria"):
            masa = molaridad * vol * pm
            st.success(f"**Masa requerida:** {masa:.4f} gramos")
            
    elif opcion_mol == "Volumen de Solución (L)":
        masa = st.number_input("Masa del soluto (g):", min_value=0.0, value=5.85)
        pm = st.number_input("Peso Molecular / Masa Molar (g/mol):", min_value=0.1, value=58.44)
        molaridad = st.number_input("Molaridad deseada (M):", min_value=0.001, value=0.1)
        
        if st.button("Calcular Volumen"):
            vol = (masa / pm) / molaridad
            st.success(f"**Volumen requerido:** {vol:.4f} Litros ({vol*1000:.1f} mL)")

# ---------------------------------------------------------
# MÓDULO 3: CONSTANTES Ka, Kb, pKa, pKb
# ---------------------------------------------------------
elif menu == "3. Constantes de Acidez/Basicidad (Ka, Kb, pKa, pKb)":
    st.header("3. Conversor y Calculadora de Constantes")
    
    col_k1, col_k2 = st.columns(2)
    
    with col_k1:
        st.subheader("Conversión Ka <-> pKa / Kb <-> pKb")
        modo_k = st.radio("Selecciona conversión:", ["Dado K -> Calcular pK", "Dado pK -> Calcular K"])
        
        if modo_k == "Dado K -> Calcular pK":
            val_k = st.number_input("Valor de K (Ka o Kb):", min_value=1e-20, value=1.8e-5, format="%.2e")
            pk = -np.log10(val_k)
            st.info(f"**pK (pKa o pKb):** {pk:.2f}")
        else:
            val_pk = st.number_input("Valor de pK (pKa o pKb):", min_value=-2.0, max_value=20.0, value=4.74)
            k = 10**(-val_pk)
            st.info(f"**K (Ka o Kb):** {k:.2e}")

    with col_k2:
        st.subheader("Relación Ácido-Base Conjugado")
        st.caption("A 25 °C: Ka × Kb = Kw (1×10⁻¹⁴)  -->  pKa + pKb = 14")
        
        input_par = st.number_input("Ingresa pKa o pKb conocido:", min_value=0.0, max_value=14.0, value=4.74)
        resultado_par = 14.0 - input_par
        st.success(f"**El par conjugado tiene un pK de:** {resultado_par:.2f}")
        st.write(f"**Valor equivalente de K:** {10**(-resultado_par):.2e}")

# ---------------------------------------------------------
# MÓDULO 4: DILUCIONES
# ---------------------------------------------------------
elif menu == "4. Calculadora de Diluciones (C1V1 = C2V2)":
    st.header("4. Calculadora de Diluciones")
    st.write("Fórmula: **C₁ × V₁ = C₂ × V₂**")
    
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        c1 = st.number_input("Concentración Inicial C₁ (M):", min_value=0.0, value=12.0)
        v1 = st.number_input("Volumen Inicial V₁ (mL):", min_value=0.0, value=10.0)
        c2 = st.number_input("Concentración Final C₂ deseada (M):", min_value=0.0, value=0.1)
        
    with col_d2:
        if c1 > 0 and c2 > 0:
            if c2 >= c1:
                st.warning("⚠️ La concentración final (C₂) debe ser menor que la inicial (C₁) para ser una dilución.")
            else:
                v2 = (c1 * v1) / c2
                agua_a_agregar = v2 - v1
                st.success(f"**Volumen Final (V₂):** {v2:.2f} mL")
                st.info(f"👉 **Agua/Solvente a agregar:** {agua_a_agregar:.2f} mL")

# ---------------------------------------------------------
# MÓDULO 5: SIMULADOR DE TITULACIÓN
# ---------------------------------------------------------
elif menu == "5. Simulador de Curva de Titulación":
    st.header("5. Simulación de Titulación (Ácido Fuerte con Base Fuerte)")
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        va = st.number_input("Volumen de Ácido en Matraz (mL):", value=50.0)
        ca = st.number_input("Concentración del Ácido (M):", value=0.1)
        cb = st.number_input("Concentración de la Base en Bureta (M):", value=0.1)
        
    # Puntos de la curva
    v_buret = np.linspace(0, va * (ca/cb) * 2, 200)
    ph_list = []
    
    moles_a = (va / 1000.0) * ca
    
    for vb in v_buret:
        moles_b = (vb / 1000.0) * cb
        v_total = (va + vb) / 1000.0
        
        if moles_b < moles_a:
            # Exceso de ácido
            h_rem = (moles_a - moles_b) / v_total
            ph_val = -np.log10(h_rem)
        elif np.isclose(moles_b, moles_a):
            # Punto de equivalencia
            ph_val = 7.0
        else:
            # Exceso de base
            oh_rem = (moles_b - moles_a) / v_total
            poh_val = -np.log10(oh_rem)
            ph_val = 14.0 - poh_val
            
        ph_list.append(ph_val)

    with col_t2:
        fig, ax = plt.subplots()
        ax.plot(v_buret, ph_list, color='#1B365D', linewidth=2, label="Curva de pH")
        v_eq = va * (ca / cb)
        ax.axvline(v_eq, color='red', linestyle='--', label=f'Punto eq. ({v_eq:.1f} mL)')
        ax.set_xlabel("Volumen de Base Añadido (mL)")
        ax.set_ylabel("pH")
        ax.set_title("Curva de Titulación Ácido-Base")
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend()
        st.pyplot(fig)

# ---------------------------------------------------------
# MÓDULO 6: TABLA DE REFERENCIA
# ---------------------------------------------------------
elif menu == "6. Tabla de Referencia Ka/Kb":
    st.header("6. Ácidos y Bases Comunes")
    
    datos = [
        {"Sustancia": "Ácido Clorhídrico (HCl)", "Tipo": "Ácido Fuerte", "Ka": "Muy Grande", "pKa": "< 0"},
        {"Sustancia": "Ácido Nítrico (HNO₃)", "Tipo": "Ácido Fuerte", "Ka": "Muy Grande", "pKa": "< 0"},
        {"Sustancia": "Ácido Acético (CH₃COOH)", "Tipo": "Ácido Débil", "Ka": "1.8 × 10⁻⁵", "pKa": "4.74"},
        {"Sustancia": "Ácido Fórmico (HCOOH)", "Tipo": "Ácido Débil", "Ka": "1.8 × 10⁻⁴", "pKa": "3.75"},
        {"Sustancia": "Ácido Fluorhídrico (HF)", "Tipo": "Ácido Débil", "Ka": "6.8 × 10⁻⁴", "pKa": "3.17"},
        {"Sustancia": "Amoníaco (NH₃)", "Tipo": "Base Débil", "Kb": "1.8 × 10⁻⁵", "pKb": "4.75"},
        {"Sustancia": "Metilamina (CH₃NH₂)", "Tipo": "Base Débil", "Kb": "4.4 × 10⁻⁴", "pKb": "3.36"},
    ]
    
    st.table(datos)
