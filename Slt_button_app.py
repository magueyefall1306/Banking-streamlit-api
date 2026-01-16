import streamlit as st
st.header('streamlit button example')

if st.button('say hello'):
    st.write('why hello?')
else:
    st.write('bvandi')
