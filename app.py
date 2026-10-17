import streamlit as st
import time

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
                st.rerun()
        with b_col2:
            if st.button("Verificar", type="primary", use_container_width=True):
                marcados = [i for i, marcado in enumerate(escolhas) if marcado]
                acertos = len(set(marcados).intersection(set(quadrados_corretos)))
                
                if acertos >= 3: 
                    st.success("Captcha verificado! Avançando...")
                    time.sleep(1)
                    st.session_state.etapa += 1
                    st.rerun()
                else:
                    st.session_state.erro_captcha = True
                    st.rerun()

# --- FLUXO DO APLICATIVO ---
st.title("🎲 Desafio 🎲")

# ETAPA 0: DIGITAR O NOME
if st.session_state.etapa == 0:
    st.markdown("### Antes de começar, precisamos de uma informação...")
    
    # Formulário para evitar o "Press Enter to apply"
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

# ETAPA 1: CONFIRMAÇÃO COM SILVIO SANTOS
elif st.session_state.etapa == 1:
    col_img1, col_img2, col_img3 = st.columns([1, 4, 1])
    with col_img2:
        st.image("meme_silvio_1.png", use_container_width=True)
    
    st.markdown(f"#### Você digitou: **{st.session_state.nome_usuario}**")
    st.markdown("**Está certo disso? Posso perguntar?** 🤨")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sim, é esse mesmo. ✅", type="primary", use_container_width=True):
            st.session_state.etapa = 2 
            st.rerun()
    with col2:
        if st.button("Não, quero corrigir ✏️", use_container_width=True):
            st.session_state.nome_usuario = "" 
            st.session_state.input_key += 1 
            st.session_state.etapa = 0 
            st.rerun()

# ETAPA 2: "CERTA RESPOSTA" (Meme 2)
elif st.session_state.etapa == 2:
    col_img1, col_img2, col_img3 = st.columns([1, 4, 1])
    with col_img2:
        st.image("meme_silvio_2.png", use_container_width=True)
        
    st.success(f"**Certa resposta, {st.session_state.nome_usuario}!**")
    
    if st.button("Avançar para os desafios 🚀", type="primary", use_container_width=True):
        st.session_state.etapa = 3
        st.rerun()

# ETAPA 3: Captcha 1 (Café)
elif st.session_state.etapa == 3:
    titulo_captcha1 = "Selecione o líquido sagrado que ajuda a evitar um processo administrativo:"
    renderizar_captcha("captcha1_cafe.png", titulo_captcha1, [3, 4, 5, 6, 7])

# ETAPA 4: Captcha 2 (Rivotril)
elif st.session_state.etapa == 4:
    titulo_captcha2 = "Selecione o único item que impede o funcionário de surtar e não perder o réu primário:"
    renderizar_captcha("captcha2_rivotril.png", titulo_captcha2, [3, 4, 5, 6, 7])

# ETAPA 5: Mensagem Final
elif st.session_state.etapa == 5:
    st.balloons()
    st.success(f"Parabéns, {st.session_state.nome_usuario}! Você concluiu com êxito o desafio!")
    
    st.markdown("""
    ### 🚨 RECADO IMPORTANTÍSSIMO DE FÉRIAS! 🏖️
    
    *Uma mensagem especial de agradecimento:*
    
    Poderia ter feito um discurso presencial melhor do que eu fiz? Poderia! Mas, como não nasci com o dom da oratória nem com a sabedência da minha "irmã mais nova", Juliana, e considerando que a timidez também não colabora muito (sequelas da época em que eu fritava peixe olhando pro gato 🐈🐟) — resolvi inovar e deixar tudo preparado por aqui mesmo!
    
    Já que chegou até aqui, está oficialmente convocado(a) para receber meus sinceros agradecimentos. Afinal, curiosidade não mata só o gato… às vezes também garante acesso a um discurso de férias! 😂
    
    Brincadeiras à parte, estou entrando de férias, mas não poderia partir rumo ao meu merecido descanso sem agradecer de coração por todas as mensagens, abraços e presentes de aniversário. Cada gesto de carinho tornou meu dia ainda mais especial. Vocês são demais!
    
    Obrigado por lembrarem de mim, pelo carinho de sempre e, principalmente, por colaborarem com a minha autoestima, fingindo que eu não estou ficando mais velho! 🤣❤️
    
    ---
    #### 📊 BOLETIM OFICIAL DA IDADE DO ANDRÉ
    
    * 🎂 **4.5** no RG
    * 😎 **26** na aparência
    * 🔋 **53** na disposição
    * 🦴 **84** na coluna
    
    *Nota metodológica: Segundo dados do IBGE, os números apresentam margem de erro de 2 pontos percentuais para mais ou para menos. Contudo, a coluna do entrevistado já entrou com recurso solicitando revisão imediata dos dados.*
    
    ---
    #### 🏖️ PROGRAMAÇÃO OFICIAL DE FÉRIAS
    
    Após longos períodos de trabalho, compromissos e responsabilidades, informo que meu departamento de produtividade entrará em recesso por tempo indeterminado (ou até o despertador voltar a ser necessário).
    
    **😴 1. Sono sem Despertador**
    Acordar ao meio-dia, com cara de quem enfrentou três turnos de trabalho, roupa amarrotada e nenhuma preocupação com horários. O despertador está oficialmente desligado, e qualquer tentativa de contato antes do meio-dia será considerada uma ameaça à paz mundial!
    
    **📺 2. Sessão Maratona: O Sofá é Meu Escritório**
    Deitado na cama, assistindo Lagoa Azul, além de filmes e séries até a TV perguntar: “Você ainda está assistindo?”. Sim, minha filha! E, se depender de mim, vou assistir até o controle remoto pedir férias também!
    
    **🔴⚫ 3. Mengão no Sofá: Emoção, Raiva e Sofrimento**
    Torcer pelo Flamengo com energia máxima, sentado confortavelmente no sofá, porque passar raiva em pé é um esforço desnecessário. O coração descansa, mas o Mengão nem sempre colabora! 😂
    
    **🐔 4. Vida no quintal: Meu Novo Cargo é Cuidador de Galinhas**
    Cuidar das galinhas, ouvir cacarejos durante o dia inteiro e tentar entender se elas estão conversando, reclamando ou organizando uma reunião para falar mal de mim. Pelo menos, nesse setor, ninguém marca reunião no Teams!
    
    ---
    #### 🙏 UMA MENSAGEM DE CORAÇÃO
    
    Que Deus abençoe sua vida, sua família e seus caminhos. Que sua semana seja repleta de paz, saúde, alegria e das infinitas graças e bênçãos do Senhor!
    
    E lembre-se: se espirrar… saúde, Deus te cria 😂🙏
    
    Obrigado mais uma vez pelo carinho, pelos presentes e por fazerem parte de momentos tão especiais da minha vida.
    
    Agora, com o coração agradecido e o corpo (quase) pronto para o descanso, encerro este comunicado.
    
    **O servidor se despede e o cidadão de férias assume o controle! 🏖️😎**
    
    Um grande abraço a todos, fiquem com Deus e até a volta!
    
    **André ❤️**
    """)
    
    if st.button("Jogar Novamente", type="primary"):
        st.session_state.etapa = 0
        st.session_state.nome_usuario = ""
        st.session_state.erro_captcha = False
        st.session_state.input_key = 0
        st.rerun()
