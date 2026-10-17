import streamlit as st
import time

# Configuração da página
st.set_page_config(page_title="Presente de Aniversário", layout="centered")

# --- ESTADO DA SESSÃO (Controle de fluxo) ---
if 'etapa' not in st.session_state:
    st.session_state.etapa = 0
if 'nome_usuario' not in st.session_state:
    st.session_state.nome_usuario = ""
if 'erro_captcha' not in st.session_state:
    st.session_state.erro_captcha = False

# --- FUNÇÃO PARA CRIAR O CAPTCHA INTERATIVO ---
def renderizar_captcha(caminho_imagem, titulo, quadrados_corretos):
    st.markdown(f"<h3 style='text-align: center; color: #1E88E5;'>{titulo}</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.image(caminho_imagem, use_column_width=True)
        st.write("**Selecione os quadros corretos:**")
        
        cols = st.columns(3)
        escolhas = []
        
        for i in range(9):
            with cols[i % 3]:
                # O checkbox fica marcado se o usuário clicou ou se já estava marcado (para não perder a seleção no erro)
                escolha = st.checkbox(f"Quadro {i+1}", key=f"check_{st.session_state.etapa}_{i}")
                escolhas.append(escolha)
        
        st.divider()
        
        # Mensagem de erro engraçada (se houver)
        if st.session_state.erro_captcha:
            st.error("Ops! Parece que você precisa de férias também... 🤪 Tente de novo!")
            st.session_state.erro_captcha = False # Reseta o erro após mostrar
        
        # Botões de ação
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            if st.button("Pular", use_container_width=True):
                st.session_state.etapa += 1
                st.rerun()
        with b_col2:
            if st.button("Verificar", type="primary", use_container_width=True):
                # Pega os índices dos quadrados marcados (0 a 8)
                marcados = [i for i, marcado in enumerate(escolhas) if marcado]
                
                # Lógica de verificação: O usuário precisa marcar pelo menos 3 dos quadrados corretos
                # e não pode marcar os quadrados errados (opcional, mas deixa mais realista)
                acertos = len(set(marcados).intersection(set(quadrados_corretos)))
                erros = len(set(marcados) - set(quadrados_corretos))
                
                if acertos >= 3 and erros == 0: # Se acertou pelo menos 3 e não errou nenhum
                    st.success("Captcha verificado! Avançando...")
                    time.sleep(1)
                    st.session_state.etapa += 1
                    st.rerun()
                else:
                    # Ativa a mensagem de erro e recarrega para mostrar
                    st.session_state.erro_captcha = True
                    st.rerun()

# --- FLUXO DO APLICATIVO ---
st.title("🎁 Presente de Aniversário do André")

# ETAPA 0: TELA DE BOAS-VINDAS (NOME + CONFIRMAÇÃO)
if st.session_state.etapa == 0:
    st.markdown("### Antes de começar, precisamos de uma informação...")
    
    nome_input = st.text_input("Qual é o seu nome?", placeholder="Digite seu nome aqui...")
    
    if nome_input.strip() != "":
        st.markdown(f"#### Olá, **{nome_input}**!")
        st.markdown("**Tem certeza que é esse o seu nome?** 🤔")
        st.info("Parece um nome suspeito... Se errar, pode dar problema no RH e o agradecimento vai para outra pessoa! 😂")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sim, é esse mesmo! ✅", type="primary", use_container_width=True):
                st.session_state.nome_usuario = nome_input
                st.session_state.etapa = 1
                st.rerun()
        with col2:
            if st.button("Não, quero corrigir ✏️", use_container_width=True):
                st.session_state.nome_usuario = ""
                st.rerun()
    else:
        st.warning("Ei, você precisa digitar um nome! Não vale deixar em branco. 😉")

# ETAPA 1: Captcha 1 (Café)
elif st.session_state.etapa == 1:
    # Quadrados corretos: 4, 5, 6, 7, 8 (índices 3, 4, 5, 6, 7)
    titulo_captcha1 = "Selecione o líquido sagrado que ajuda a evitar um processo administrativo:"
    renderizar_captcha("captcha1_cafe.png", titulo_captcha1, [3, 4, 5, 6, 7])

# ETAPA 2: Captcha 2 (Rivotril)
elif st.session_state.etapa == 2:
    # Quadrados corretos: 4, 5, 6, 7, 8 (índices 3, 4, 5, 6, 7)
    titulo_captcha2 = "Selecione o único item que impede o funcionário de surtar e não perder o réu primário:"
    renderizar_captcha("captcha2_rivotril.png", titulo_captcha2, [3, 4, 5, 6, 7])

# ETAPA 3: Mensagem Final (PDF do André)
elif st.session_state.etapa == 3:
    st.balloons()
    st.success(f"Parabéns, {st.session_state.nome_usuario}! Você é oficialmente uma pessoa curiosa!")
    
    st.markdown("""
    ### Recado Importante de Férias!
    
    *Uma mensagem especial de agradecimento do André.*
    
    Poderia ter feito um discurso presencial, mas... como não tenho o dom da oratória da minha parceira de trabalho e a timidez também não ajuda (consequência da época que eu fritava peixe olhando pro gato), resolvi inovar e deixar tudo preparado por aqui!
    
    **Parabéns! Você é oficialmente uma pessoa curiosa!** De qualquer forma, está convocado(a) para receber o meu muito obrigado!
    
    Estou saindo de férias, mas não poderia ir embora sem agradecer pelas mensagens, abraços e presentes de aniversário. Vocês são demais! Obrigado por fingirem que eu não estou ficando mais velho!
    
    ---
    **4.5 NO RG | 26 NA APARÊNCIA | 53 NA DISPOSIÇÃO | 84 NA COLUNA**
    ---
    
    ### Programação Oficial de Férias
    
    *   **Sono sem Despertador:** Acordando ao meio-dia, com cara de sono, roupa toda amarrotada e despertador oficialmente desligado!
    *   **Sessão Maratona:** Relaxando na cama, assistindo Lagoa Azul, além de muitos filmes e séries, até a TV perguntar se eu ainda estou assistindo!
    *   **Mengão no Sofá:** Torcendo com energia máxima no sofá de casa e passando raiva com o Flamengo!
    *   **Vida na Roça:** Cuidando das galinhas e ouvindo elas cacarejarem o dia inteiro...
    
    Tenham uma semana abençoada, repleta das graças e bênçãos de Deus! E, se espirrarem... saúde! Deus te cria!
    
    **Abraços, André**
    """)
    
    if st.button("Jogar Novamente"):
        st.session_state.etapa = 0
        st.session_state.nome_usuario = ""
        st.session_state.erro_captcha = False
        st.rerun()
