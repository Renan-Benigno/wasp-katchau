import random
import os
import streamlit as st

def gerar_val(first_val, second_val, is_random, lines):
    if is_random == "R":
        for _ in range(lines):
            yield random.uniform(first_val, second_val)
    elif is_random == "O":
        if lines > 1:
            intervalo = (second_val - first_val) / (lines - 1)
            for i in range(lines):
                yield first_val + i * intervalo
        else:
            intervalo = (second_val - first_val) / lines
            for i in range(lines):
                yield first_val + i * intervalo

def captar_param(tipo, section_num):
    st.write(f"### {tipo}")
    # Use a unique key for each widget
    is_random = st.radio(f"{tipo} randômico ou ordenado?", ("R", "O"), key=f"{tipo}_random_{section_num}")
    val_inicio = st.number_input(f"De quanto? ", key=f"{tipo}_start_{section_num}")
    valor_fim = st.number_input(f"Pra quanto? ", key=f"{tipo}_end_{section_num}")
    return [val_inicio, valor_fim, is_random]

def captar_param_depth(section_num, prev_depth=None):
    global direction
    st.write(f"### Depth")
    if prev_depth is None:
        val_inicio = st.number_input(f"De quanto? ", key=f"Depth_start_{section_num}")
    else:
        if direction == "Up":
            val_inicio = prev_depth - 0.0001
        else:
            val_inicio = prev_depth + 0.0001
    valor_fim = st.number_input(f"Pra quanto? ", key=f"Depth_end_{section_num}")
    if direction == "Up" and val_inicio < valor_fim :
        st.write(f"Valores dados não condizem com a direção. Se a direction desejada é realmente 'Up', deixe o primeiro valor maior que o segundo valor ")
        return
    elif direction == "Down" and val_inicio > valor_fim :
        st.write(f"Valores dados não condizem com a direção. Se a direction desejada é realmente 'Down', deixe o primeiro valor menor que o segundo valor ")
        return
    return [val_inicio, valor_fim]

def secao(section_num, num_lines):
    global previous
    if section_num == 1:
        ini_depth, fim_depth = captar_param_depth(section_num)
        depth_gen = gerar_val(ini_depth, fim_depth, "O", num_lines)
        previous = fim_depth
    else:
        depth_gen = gerar_val(*captar_param_depth(section_num, previous), "O", num_lines)

    ccl_gen = gerar_val(*captar_param("CCL", section_num), num_lines)

    lines = []
    for _ in range(num_lines):
        depth = next(depth_gen)
        ccl = next(ccl_gen)
        line = f"  {depth: .4f}    000.0000    000.00000      0.0000      0.0000     {ccl: .4f}    000.0000      0.0000"

        lines.append(line + "\n")

    all_lines = "".join(lines)  # Concatena todas as linhas em uma única string
    if num_lines < 18:
        st.code(all_lines, language="text") # Exibe a string em uma caixa de código
    else:
        st.code(all_lines, language="text", height = 400) # Exibe a string em uma caixa de código com limite de tamanho
    return lines

direction = None
previous = None

def main():
    global direction
    st.title("Baseline")

    # Define o caminho para salvar o arquivo
    #path = os.path.join(os.path.expanduser("~"), "Desktop")
    #if not os.path.exists(path):
    #    st.error(f"Diretório não encontrado: {path}")
    #    return
    
    # Nome do arquivo
    baseline_name = st.text_input("Qual o nome do arquivo?", "baseline") + ".las"

    # Initialize session state to store sections
    if "sections" not in st.session_state:
        st.session_state.sections = []

    direction = st.radio(f"Qual a direção do pass?", ("Up", "Down"))

    # Add a new section
    if st.button("Nova seção?"):
        st.session_state.sections.append({"section_num": len(st.session_state.sections) + 1, "num_lines": 1})

    # Display and configure each section
    all_lines = []
    for i, section in enumerate(st.session_state.sections):
        st.write(f"### Seção {section['section_num']}")
        # Usando st.text_input em vez de st.number_input
        num_lines_input_baseline = st.text_input(
            f"Quantas linhas da seção {section['section_num']}?", 
            value=str(section["num_lines"]),
            key=f"lines_{section['section_num']}"
        )

        # Validando se a entrada é um número
        if num_lines_input_baseline.isdigit():
            section["num_lines"] = int(num_lines_input_baseline)
        else:
            st.warning("Por favor, insira um número inteiro positivo válido.")
            
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