import streamlit as st


def screen_home():
    st.title('Controle de Energia')

    # Creating two buttons side by side
    col1, col2 = st.columns(2)

    with col1:
        button_register = st.button('Cadastro')

    with col2:
        button_projection = st.button('Projeção')

    # Send to the page after clicking the button
    if button_register:
        st.session_state['screen'] = 'register'
        st.rerun()

    if button_projection:
        st.session_state['screen'] = 'projection'
        st.rerun()


def screen_register():
    st.title('Tela de Cadastro')
    st.write('Você está na tela de cadastro.')

    # Back to the home
    button_home = st.button('Voltar')
    if button_home:
        st.session_state['screen'] = 'home'
        st.rerun()


def screen_projection():
    st.title('Tela de Projeção')
    st.write('Você está na tela de projeção.')

    # Back to the home
    button_home = st.button('Voltar')
    if button_home:
        st.session_state['screen'] = 'home'
        st.rerun()


# Inicializando a tela padrão na sessão
if 'screen' not in st.session_state:
    st.session_state['screen'] = 'home'

# Exibindo a tela correta com base no estado da sessão
if st.session_state['screen'] == 'home':
    screen_home()
elif st.session_state['screen'] == 'register':
    screen_register()
elif st.session_state['screen'] == 'projection':
    screen_projection()
