import streamlit as st

st.title("Script faturamento")
st.write("Faça o upload do arquivo txt e escreva o nome com a extensão .csv, o arquivo será salvo na pasta de origem do txt.")

def takeSecond(elem):
    return elem[1]

def read_data_fin (file):

    data = [line.split() for line in file]
    return data

def write_data_fin (file_path_out, data):

    with open(file_path_out, 'w') as file:
        file.write("Contrato;Valor\n")
        for item in data:
            # Substitua o ponto pela vírgula
            valor = str(item[1]/100).replace('.', ',')
            file.write(f"{item[0]};{valor}\n")
    return 1

def main (uploaded_file, FILE_PATH_OUT):

    # Create a progress bar
    progress_bar = st.progress(0)

    try:
        data = read_data_fin(uploaded_file)
    except:
        st.write("Erro ao ler o arquivo")
    progress_bar.progress(25)

    data.sort(key=takeSecond)
    data_proc = list()
    for i in range(len(data)):
        ins = list(map(int, [data[i][1], data[i][3]]))
        data_proc.append(ins)
    del(data)
    i = 0
    while i < len(data_proc)-1:
        if data_proc[i][0] == data_proc[i+1][0]:
            data_proc[i][1] += data_proc[i+1][1]
            del(data_proc[i+1])
        else:
            i+=1
    progress_bar.progress(50)

    try:
        write_data_fin(FILE_PATH_OUT, data_proc)
        progress_bar.progress(100)
    except:
        st.write("Erro ao escrever dados no arquivo")

if __name__ == '__main__':
    uploaded_file = st.file_uploader("Escolha um arquivo")
    if uploaded_file is not None:
        FILE_PATH_OUT = st.text_input('Escreve o nome do arquivo de saída:')
        if st.button('Processar'):
            main(uploaded_file, FILE_PATH_OUT)
