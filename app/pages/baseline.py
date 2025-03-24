import random
import os
import streamlit as st

def gerar_ccl(first_val, second_val, is_random, lines):
    if is_random == "R":
        for _ in range(lines):
            yield random.uniform(first_val, second_val)
    elif is_random == "O":
        intervalo = (second_val - first_val) / (lines - 1)
        for i in range(lines):
            yield first_val + i * intervalo

def gerar_depth(start_depth, final_depth, lines):
    intervalo = (final_depth - start_depth) / (lines - 1)
    for i in range(lines):
        yield start_depth + i * intervalo

def validate_direction(start_depth, final_depth, direction):
    if direction == "U" and start_depth <= final_depth:
        st.error("Erro: Depth inicial deve ser maior que o final para direção 'U' (Up).")
        return False
    elif direction == "D" and start_depth >= final_depth:
        st.error("Erro: Depth inicial deve ser menor que o final para direção 'D' (Down).")
        return False
    return True

def write_section(file_object, depth_gen, ccl_gen, num_lines):
    for _ in range(num_lines):
        depth = next(depth_gen)
        ccl = next(ccl_gen)
        line = f"  {depth: .4f}    000.0000    000.00000      0.0000      0.0000     {ccl: .4f}    000.0000      0.0000"
        file_object.write(line + "\n")
        st.write(line)

def secao(file_path, start_depth, direction):
    final_depth = st.number_input("Qual é o Depth final?", value=start_depth)
    num