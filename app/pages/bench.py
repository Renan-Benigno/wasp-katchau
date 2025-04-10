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
    st.write(f"### {tipo}")
    # Use a unique key for each widget
    is_random = st.radio(f"{tipo} randômico ou ordenado?", ("R", "O"), key=f"{tipo}_random_{section_num}")
    val_inicio = st.number_input(f"De quanto? ", key=f"{tipo}_start_{section_num}")
    valor_fim = st.number_input(f"Pra quanto? ", key=f"{tipo}_end_{section_num}")
    return [val_inicio, valor_fim, is_random]

def secao(section_num, num_lines):
    depth_gen = gerar_val(*captar_param("Depth", section_num), num_lines)
    speed_gen = gerar_val(*captar_param("Speed", section_num), num_lines)
    tension_gen = gerar_val(*captar_param("Tension", section_num), num_lines)
    pressure_gen = gerar_val(*captar_param("Pressure", section_num), num_lines)

    lines = []
    for _ in range(num_lines):
        depth = next(depth_gen)
        speed = next(speed_gen)
        tension = next(tension_gen)
        pressure = next(pressure_gen)

        line = f"\"F D{depth: .2f}{speed: .2f}{tension: .2f}{pressure: .2f}{pressure: .2f} 00 00000\","
        lines.append(line + "\n")

    all_lines = "".join(lines)  # Concatena todas as linhas em uma única string
    if num_lines < 18:
        st.code(all_lines, language="text") # Exibe a string em uma caixa de código
    else:
        st.code(all_lines, language="text", height = 400) # Exibe a string em uma caixa de código com limite de tamanho
    return lines

def main():
    st.title("Benchmark")

    # Define o caminho para salvar o arquivo
    path = os.path.join(os.path.expanduser("~"), "Desktop")
    if not os.path.exists(path):
        st.error(f"Diretório não encontrado: {path}")
        return

    # Nome do arquivo
    benchmark_name = st.text_input("Qual o nome do arquivo?", "benchmark") + ".ts"

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
        # Usando st.text_input em vez de st.number_input
        num_lines_input_benchmark = st.text_input(
            f"Quantas linhas da seção {section['section_num']}?", 
            value=str(section["num_lines"]),
            key=f"lines_{section['section_num']}"
        )

        # Validando se a entrada é um número
        if num_lines_input_benchmark.isdigit():
            section["num_lines"] = int(num_lines_input_benchmark)
        else:
            st.warning("Por favor, insira um número inteiro positivo válido.")

        section_lines = secao(section["section_num"], section["num_lines"])
        all_lines.extend(section_lines)

    # Add the Benchmark file header
    if all_lines:
        header = ("export const benchmark = [\n")
        all_lines.insert(0, header)
        all_lines.append("]")

    # Botão para gerar e baixar o arquivo
    if st.button("Gerar e Baixar Arquivo"):
        file_content = "".join(all_lines)
        st.download_button(
            label="Baixar Arquivo",
            data=file_content,
            file_name=benchmark_name,
            mime="text/plain"
        )

if __name__ == "__main__":
    main()