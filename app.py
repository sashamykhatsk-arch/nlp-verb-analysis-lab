import streamlit as st
import logic
import pandas as pd

st.set_page_config(page_title="Lab NLP: Verbs", page_icon="📝")

st.title("Лабораторна робота: Аналіз дієслів (Варіант 14)")
st.markdown("**Завдання:** Виділення дієслів, морфологічний аналіз та POS-тегінг.")

if 'analyzed_doc' not in st.session_state:
    st.session_state['analyzed_doc'] = None

test_texts = {
    "Власний текст": "",
    "Текст 1 (Класика)": "Сонце заходить, гори чорніють, пташки тихнуть, поле німіє. Вітер не дише, ніде не шелесне.",
    "Текст 2 (Новини)": "Студент написав програму і отримав високу оцінку. Він виконав всі завдання вчасно.",
    "Текст 3 (Розмовний)": "Я хочу піти гуляти, але маю робити лабораторну роботу. Сподіваюся, що встигну все зробити."
}

st.sidebar.header("Налаштування вводу")
selected_option = st.sidebar.selectbox("Оберіть джерело тексту:", list(test_texts.keys()))

if selected_option == "Власний текст":
    text_input = st.text_area("Введіть ваш текст українською:", height=150)
else:
    text_input = st.text_area("Текст для аналізу:", value=test_texts[selected_option], height=150)

if st.button("Аналізувати текст"):
    if not text_input.strip():
        st.error("Будь ласка, введіть текст для аналізу!")
    else:
        st.session_state['analyzed_doc'] = logic.analyze_text(text_input)

if st.session_state['analyzed_doc'] is not None:
    doc = st.session_state['analyzed_doc']
    
    st.header("1. Знайдені дієслова")
    verbs = logic.get_verbs(doc)
    
    if verbs:
        df_verbs = pd.DataFrame(verbs)
        st.dataframe(df_verbs[["word", "lemma"]].rename(columns={"word": "Слово", "lemma": "Початкова форма"}))
        st.success(f"Знайдено дієслів: {len(verbs)}")
    else:
        st.info("Дієслів у тексті не знайдено.")

    st.divider()

    st.header("2. Морфологічний аналіз дієслова")
    if verbs:
        verb_options = [f"{v['word']} (індекс: {v['index']})" for v in verbs]
        
        selected_verb_str = st.selectbox(
            "Оберіть дієслово для детального аналізу:", 
            verb_options
        )
        
        if selected_verb_str:
            selected_index = int(selected_verb_str.split("індекс: ")[1][:-1])
            token = doc[selected_index] 
            
            morph_info = logic.get_verb_morphology(token)
            st.json(morph_info) 
    else:
        st.write("Немає дієслів для аналізу.")

    st.divider()

    st.header("3. Трансформація речення (POS-тегінг)")
    sentences = list(doc.sents)
    if len(sentences) > 0:
        sent_idx = st.slider("Оберіть номер речення:", 1, len(sentences), 1) - 1
        
        orig, transformed = logic.sentence_to_pos(doc, sent_idx)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Оригінал")
            st.info(orig)
        with col2:
            st.subheader("Частини мови")
            st.warning(transformed)
            st.caption("NOUN - іменник, VERB - дієслово, ADJ - прикметник і т.д.")