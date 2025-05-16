import streamlit as st


st.title("generteur_rapport")


if st.button("Clique-moi !"):
    st.success("Tu as cliqué sur le bouton 🎉")
else:
    st.info("Clique sur le bouton ci-dessus.")
