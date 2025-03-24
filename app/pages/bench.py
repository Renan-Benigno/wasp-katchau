import random
import os
import streamlit as st

def gerar_val(first_val, second_val, is_random, lines):
    if is_random == "R":
        for _ in range(lines):
            yield random.uniform(first_val, second_val)
    elif is_random == "O":
        intervalo = (second_val - first_val) / (lines - 1)
        for i in range(lines):
            yield first_val + i * intervalo

def captar_param(tipo, section_num):
    st.write(f"### {tipo} Configuration")
    # Use a unique key for each widget
    is_random = st.radio(f"{tipo} randômico ou ordenado?", ("R", "O"), key=f"{tipo}_random_{section_num}")
    val_inicio = st.number_input(f"De quanto? ({tipo})", key=f"{tipo}_start_{section_num}")
    valor_fim = st.number_input(f"Pra quanto? ({tipo})", key=f"{tipo}_end_{section_num}")
    return [val_inicio, valor_fim, is_random]

def secao(section_num, num_lines):
    depth_gen = gerar_val(*captar_param("Depth", section_num), num_lines)
    ccl_gen = gerar_val(*captar_param("CCL", section_num), num_lines)

    lines = []
    for _ in range(num_lines):
        depth = next(depth_gen)
        ccl = next(ccl_gen)
        line = f"  {depth: .4f}    000.0000    000.00000      0.0000      0.0000     {ccl: .4f}    000.0000      0.0000"
        lines.append(line + "\n")
        st.write(line)

    return lines

def main():
    st.title("LAS File Generator")

    # Define o caminho para salvar o arquivo
    path = os.path.join(os.path.expanduser("~"), "Desktop")
    if not os.path.exists(path):
        st.error(f"Diretório não encontrado: {path}")
        return

    # Nome do arquivo
    baseline_name = st.text_input("Qual o nome do arquivo?", "baseline") + ".las"

    # Initialize session state to store sections
    if "sections" not in st.session_state:
        st.session_state.sections = []

    # Add a new section
    if st.button("Nova seção?"):
        st.session_state.sections.append({"section_num": len(st.session_state.sections) + 1, "num_lines": 1})

    # Display and configure each section
    all_lines = []
    for i, section in enumerate(st.session_state.sections):
        st.write(f"### Seção {section['section_num']}")
        section["num_lines"] = st.number_input(
            f"Quantas linhas da seção {section['section_num']}?", 
            min_value=1, 
            value=section["num_lines"], 
            key=f"lines_{section['section_num']}"
        )
        section_lines = secao(section["section_num"], section["num_lines"])
        all_lines.extend(section_lines)

    # Add the LAS file header
    if all_lines:
        header = (
            "~Version Information\n" +
            "VERS.                            2.0: CWLS Log ASCII STANDARD - VERSION 2.0\n" +
            "WRAP.                             NO: One line per depth step\n" +
            "~Well Information\n" +
            "STRT.M                     2841.4880: START DEPTH\n" +
            "STOP.M                     2783.9408: STOP DEPTH\n" +
            "STEP.M                       -0.0152: STEP\n" +
            "NULL.                      -999.2500: NULL VALUE\n" +
            "COMP.                               : COMPANY\n" +
            "WELL.                               : WELL\n" +
            "FLD.                                : FIELD\n" +
            "LOC.                                : LOCATION\n" +
            "SRVC.                 Liberty Energy: SERVICE COMPANY\n" +
            "DATE.                     2023 09 21: LOG DATE YYYY MM DD\n" +
            "UWI.                                : UNIQUE WELL ID\n" +
            "PROV.                               : PROVINCE\n" +
            "~Curve Information\n" +
            "DEPT.M                   0 000 00 00: Depth\n" +
            "LSPD.M/MIN                         0: Line Speed\n" +
            "LTEN.KG                            0: Surface Line Tension\n" +
            "MINMK.                             0: Minute Mark Ticks\n" +
            "HVOLTA.V                           0: Head Voltage Apparent\n" +
            "CCL.                               0: Casing Collar Locator\n" +
            "SRFTEMP.DEGC                       0: Surface Temperature\n" +
            "CASETHCK.MM                        0: Casing Thickness\n" +
            "~Parameter Information\n" +
            "~A  Depth       LSPD        LTEN       MINMK       HVOLTA       CCL       SRFTEMP     CASETHCK  \n"
        )
        all_lines.insert(0, header)

    # Botão para gerar e baixar o arquivo
    if st.button("Gerar e Baixar Arquivo"):
        file_content = "".join(all_lines)
        st.download_button(
            label="Baixar Arquivo",
            data=file_content,
            file_name=baseline_name,
            mime="text/plain"
        )

if __name__ == "__main__":
    main()