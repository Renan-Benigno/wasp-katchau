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

def captar_param(tipo, section_num_warrior):
    st.write(f"### {tipo}")
    # Use a unique key for each widget
    is_random = st.radio(f"{tipo} randômico ou ordenado?", ("R", "O"), key=f"{tipo}_random_{section_num_warrior}")
    val_inicio = st.number_input(f"De quanto? ({tipo})", key=f"{tipo}_start_{section_num_warrior}")
    valor_fim = st.number_input(f"Pra quanto? ({tipo})", key=f"{tipo}_end_{section_num_warrior}")
    return [val_inicio, valor_fim, is_random]

def secao(section_num_warrior, num_lines):
    depth_gen = gerar_val(*captar_param("Depth", section_num_warrior), num_lines)
    speed_gen = gerar_val(*captar_param("Speed", section_num_warrior), num_lines)
    tension_gen = gerar_val(*captar_param("Tension", section_num_warrior), num_lines)
    ccl_gen = gerar_val(*captar_param("CCL", section_num_warrior), num_lines)
    voltage_gen = gerar_val(*captar_param("Voltage", section_num_warrior), num_lines)
    current_gen = gerar_val(*captar_param("Current", section_num_warrior), num_lines)

    lines = []
    for _ in range(num_lines):
        depth = next(depth_gen)
        speed = next(speed_gen)
        tension = next(tension_gen)
        ccl = next(ccl_gen)
        voltage = next(voltage_gen)
        current = next(current_gen)

        line = f"\"1000,{depth: .2f},{speed: .2f},{tension: .2f},{ccl: .2f},{voltage: .2f},{current: .2f},5,6,7\","
        lines.append(line + "\n")
        st.write(line)

    return lines

def criar_secaos_warrior():
    """
    Função para criar uma nova seção e atualizar o st.session_state.
    """
    if st.button("Nova seção?"):
        new_section_num = len(st.session_state["warrior_sections"]) + 1
        st.session_state["warrior_sections"].append({"section_num_warrior": new_section_num, "num_lines": 1})

def main():
    st.title("Warrior")

    # Define o caminho para salvar o arquivo
    path = os.path.join(os.path.expanduser("~"), "Desktop")
    if not os.path.exists(path):
        st.error(f"Diretório não encontrado: {path}")
        return

    # Nome do arquivo
    warrior_name = st.text_input("Qual o nome do arquivo?", "warrior") + ".ts"

    # Initialize session state to store sections
    if "warrior_sections" not in st.session_state:
        st.session_state["warrior_sections"] = []

    # Chama a função para criar a seção
    criar_secaos_warrior()

    # Display and configure each section
    all_lines = []
    for i, section in enumerate(st.session_state.warrior_sections):
        st.write(f"### Seção {section['section_num_warrior']}")
        # Usando st.text_input em vez de st.number_input
        num_lines_input_warrior = st.text_input(
            f"Quantas linhas da seção {section['section_num_warrior']}?", 
            value=str(section["num_lines"]),
            key=f"page_warrior_lines_{section['section_num_warrior']}"
        )

        # Validando se a entrada é um número
        if num_lines_input_warrior.isdigit():
            section["num_lines"] = int(num_lines_input_warrior)
        else:
            st.warning("Por favor, insira um número inteiro positivo válido.")

        section_lines = secao(section["section_num_warrior"], section["num_lines"])
        all_lines.extend(section_lines)

    # Add the opening and closing brackets for the array
    if all_lines:
        all_lines.insert(0, "export const warrior = [\n")
        all_lines.append("]")

    # Botão para gerar e baixar o arquivo
    if st.button("Gerar e Baixar Arquivo"):
        file_content = "".join(all_lines)
        st.download_button(
            label="Baixar Arquivo",
            data=file_content,
            file_name=warrior_name,
            mime="text/plain"
        )

if __name__ == "__main__":
    main()