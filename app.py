import streamlit as st
import time
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Desafio", layout="centered")

# --- ESTADO DA SESSÃO ---
if 'etapa' not in st.session_state:
    st.session_state.etapa = 0
if 'nome_usuario' not in st.session_state:
    st.session_state.nome_usuario = ""
if 'erro_captcha' not in st.session_state:
    st.session_state.erro_captcha = False
if 'input_key' not in st.session_state:
    st.session_state.input_key = 0 
if 'limpar_tela' not in st.session_state:
    st.session_state.limpar_tela = False

# --- FUNÇÃO PARA CRIAR O CAPTCHA INTERATIVO ---
def renderizar_captcha(caminho_imagem, titulo, quadrados_corretos):
    st.markdown(f"<h3 style='text-align: center; color: #1E88E5;'>{titulo}</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.image(caminho_imagem, use_container_width=True)
        st.write("**Selecione os quadros corretos:**")
        
        cols = st.columns(3)
        escolhas = []
        
        for i in range(9):
            with cols[i % 3]:
                escolha = st.checkbox(f"Quadro {i+1}", key=f"check_{st.session_state.etapa}_{i}")
                escolhas.append(escolha)
        
        st.divider()
        
        if st.session_state.erro_captcha:
            st.error("Ops! Parece que você precisa de férias também... 🤪 Tente de novo!")
            st.session_state.erro_captcha = False 
        
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            if st.button("Pular", use_container_width=True):
                st.session_state.etapa += 1
                st.session_state.limpar_tela = True
                st.rerun()
        with b_col2:
            if st.button("Verificar", type="primary", use_container_width=True):
                marcados = [i for i, marcado in enumerate(escolhas) if marcado]
                acertos = len(set(marcados).intersection(set(quadrados_corretos)))
                
                if acertos >= 3: 
                    st.success("Captcha verificado! Avançando...")
                    time.sleep(1)
                    st.session_state.etapa += 1
                    st.session_state.limpar_tela = True
                    st.rerun()
                else:
                    st.session_state.erro_captcha = True
                    st.rerun()

# --- FLUXO DO APLICATIVO ---

# Limpa a tela para não deixar rastros (botões fantasmas)
if st.session_state.limpar_tela:
    st.empty() 
    st.session_state.limpar_tela = False 
else:
    st.title("🎲 Desafio 🎲")

# ETAPA 0: DIGITAR O NOME
if st.session_state.etapa == 0:
    st.markdown("### Antes de começar, precisamos de uma informação...")
    
    with st.form(key=f"form_nome_{st.session_state.input_key}"):
        nome_input = st.text_input("Qual é o seu nome?", placeholder="Digite seu nome aqui...")
        submit_nome = st.form_submit_button("Pressione para prosseguir", type="primary", use_container_width=True)
    
    if submit_nome:
        if nome_input.strip() == "":
            st.warning("Ei, você precisa digitar um nome! Não vale deixar em branco. 😉")
        else:
            st.session_state.nome_usuario = nome_input
            st.session_state.etapa = 1 
            st.rerun()

# ETAPA 1: CONFIRMAÇÃO COM SILVIO SANTOS 1
elif st.session_state.etapa == 1:
    st.markdown("<h3 style='text-align: center;'>🕵️ Oh criatura, esse é o seu nome mesmo?</h3>", unsafe_allow_html=True)
    
    col_img1, col_img2, col_img3 = st.columns([1, 4, 1])
    with col_img2:
        st.image("meme_silvio_1.png", use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sim, é esse mesmo. ✅", type="primary", use_container_width=True):
            st.session_state.etapa = 2 
            st.session_state.limpar_tela = True 
            st.rerun()
    with col2:
        if st.button("Não, quero corrigir ✏️", use_container_width=True):
            st.session_state.nome_usuario = "" 
            st.session_state.input_key += 1 
            st.session_state.etapa = 0 
            st.session_state.limpar_tela = True
            st.rerun()

# ETAPA 2: CONTAGEM REGRESSIVA (SUSPENSE COM LIMPEZA FORÇADA)
elif st.session_state.etapa == 2:
    # 1. Injeção de CSS para esconder o menu e pintar o fundo de branco (mata o botão fantasma)
    st.markdown("""
        <style>
            [data-testid="stSidebar"] { display: none; }
            #MainMenu { visibility: hidden; }
            header { visibility: hidden; }
            .stApp { background-color: #FFFFFF; }
        </style>
    """, unsafe_allow_html=True)
    
    # 2. Pequena pausa de segurança para o navegador processar a limpeza
    placeholder_limpo = st.empty()
    time.sleep(0.3) 
    placeholder_limpo.empty()
    
    # 3. Exibição do título e do vídeo
    st.title("🎲 Desafio 🎲")
    st.markdown("### Preparando a resposta... 🥁")
    
    caminho_video = "contagem.mp4"
    
    if os.path.exists(caminho_video):
        col_vid1, col_vid2, col_vid3 = st.columns([1, 4, 1])
        with col_vid2:
            # CSS para esconder os controles de play/pause do player de vídeo
            st.markdown(
                """
                <style>
                    video::-webkit-media-controls { display:none !important; }
                    video::-webkit-media-controls-enclosure { display:none !important; }
                </style>
                """,
                unsafe_allow_html=True
            )
            
            st.video(caminho_video, autoplay=True, loop=False)
        
        # Tempo de espera para o vídeo rodar (ajustado para 11s para garantir o término)
        time.sleep(11) 
        
        st.session_state.etapa = 3 
        st.session_state.limpar_tela = True 
        st.rerun()
    else:
        st.error("Arquivo contagem.mp4 não encontrado.")

# ETAPA 3: "CERTA RESPOSTA" (Meme 2)
elif st.session_state.etapa == 3:
    st.title("🎲 Desafio 🎲")
    
    col_img1, col_img2, col_img3 = st.columns([1, 4, 1])
    with col_img2:
        st.image("meme_silvio_2.png", use_container_width=True)
        
    if st.button("Avançar para os desafios 🚀", type="primary", use_container_width=True):
        st.session_state.etapa = 4
        st.session_state.limpar_tela = True
        st.rerun()

# ETAPA 4: Captcha 1 (Café)
elif st.session_state.etapa == 4:
    st.title("🎲 Desafio 🎲")
    titulo_captcha1 = "Selecione o líquido sagrado que ajuda a evitar um processo administrativo:"
    renderizar_captcha("captcha1_cafe.png", titulo_captcha1, [3, 4, 5, 6, 7])

# ETAPA 5: Captcha 2 (Rivotril)
elif st.session_state.etapa == 5:
    st.title("🎲 Desafio 🎲")
    titulo_captcha2 = "Selecione o único item que impede o funcionário de surtar e não perder o réu primário:"
    renderizar_captcha("captcha2_rivotril.png", titulo_captcha2, [3, 4, 5, 6, 7])

# ETAPA 6: Mensagem Final (COM O GIF DO CACO)
elif st.session_state.etapa == 6:
    st.title("🎲 Desafio 🎲")
    st.balloons()
    st.success(f"Parabéns, {st.session_state.nome_usuario}! Você concluiu com êxito o desafio!")
    
    # --- GIF DO CACO NO INÍCIO ---
    col_gif1, col_gif2, col_gif3 = st.columns([1, 3, 1])
    with col_gif2:
        # Tenta carregar o GIF ou JPG do Caco
        if os.path.exists("caco_ferias.gif"):
            st.image("caco_ferias.gif", use_container_width=True)
        elif os.path.exists("caco_ferias.jpg"):
            st.image("caco_ferias.jpg", use_container_width=True)
        else:
            st.warning("GIF do Caco não encontrado. Verifique o arquivo.")
    
    # --- TEXTO FINAL ---
    st.markdown("""
    <div style="text-align: justify;">
    
    ### 🚨 RECADO IMPORTANTÍSSIMO DE FÉRIAS! 🏖️
    
    Poderia ter feito um discurso presencial melhor ao receber os presentes na sexta-feira? Poderia! 😂 Mas, como a oratória não é meu forte e a timidez ainda atrapalha (sequelas da época em que eu fritava peixe olhando pro gato 🐈🐟), resolvi inovar e deixar meu agradecimento registrado por aqui mesmo!
    
    Quero agradecer de coração pelas mensagens, pelos abraços e pelos presentes de aniversário. Cada gesto de carinho tornou meu dia ainda mais especial. Vocês são demais! ❤️
    
    ---
    #### 📊 BOLETIM OFICIAL DA IDADE DO ANDRÉ
    
    * 🎂 **4.5** no RG
    * 😎 **26** na aparência
    * 🔋 **53** na disposição
    * 🦴 **84** na coluna
    
    *Dados com margem de erro de 2 pontos, segundo o IBGE da minha imaginação. A coluna já entrou com recurso! 😂*
    
    ---
    #### 🙏 UM AGRADECIMENTO DE CORAÇÃO 🙏
    
    Que Deus abençoe cada um de vocês, suas famílias e seus caminhos, com muita saúde, paz, alegria e infinitas bênçãos!
    
    Agora, com o coração agradecido e o corpo (quase) pronto para descansar, encerro este comunicado:
    
    **O servidor se despede, e o cidadão de férias assume o controle! 🏖️😎**
    
    Um grande abraço a todos, fiquem com Deus e até a volta!
    
    **🤘 André ✌️**
    
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Jogar Novamente", type="primary"):
        st.session_state.etapa = 0
        st.session_state.nome_usuario = ""
        st.session_state.erro_captcha = False
        st.session_state.input_key = 0
        st.session_state.limpar_tela = True
        st.rerun()
