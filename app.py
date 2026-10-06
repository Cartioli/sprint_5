import time
import pandas as pd
import scipy.stats
import streamlit as st

# 1. Inicialização de variáveis persistentes na sessão
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(
        columns=['no', 'iterations', 'mean']
    )

st.header('Jogando uma moeda')

# Espaço reservado para atualizar o gráfico dinamicamente no ecrã
chart_placeholder = st.empty()


def toss_coin(n):
    """Função que emula o lançamento de uma moeda n vezes e atualiza o gráfico em tempo real."""
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    means = [0.5]
    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        means.append(mean)

        # Atualiza o gráfico em tempo real no mesmo espaço reservado
        chart_placeholder.line_chart(means)
        time.sleep(0.05)

    return means[-1]


# Widgets de entrada
number_of_trials = st.slider('Número de tentativas?', 1, 1000, 10)
start_button = st.button('Executar')

# Lógica do experimento
if start_button:
    st.write(f'Executando o experimento de {number_of_trials} tentativas.')

    # Incrementa o contador de experimentos
    st.session_state['experiment_no'] += 1

    # Executa a simulação
    mean = toss_coin(number_of_trials)

    # Junta o novo resultado ao DataFrame persistente na sessão
    st.session_state['df_experiment_results'] = pd.concat(
        [
            st.session_state['df_experiment_results'],
            pd.DataFrame(
                data=[
                    [st.session_state['experiment_no'], number_of_trials, mean]
                ],
                columns=['no', 'iterations', 'mean'],
            ),
        ],
        axis=0,
    ).reset_index(drop=True)

# Exibe a tabela de resultados acumulados
st.write(st.session_state['df_experiment_results'])
