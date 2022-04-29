import time
import streamlit as st

from format import get_correct
from Summarize import get_correct_sum
def main():
    st.title("Spelling Correction")
    st.markdown("AI web app to correct error")
    
    text = st.text_area("Enter Text to Correct", height=275)
    number = st.number_input('Insert a number')
    # if st.button("Generator Error"):
    #     error_text = error_generator.add_noise(text, percent_error=0.3)
    #     st.write(error_text)

    if st.button("Correct"):
        with st.spinner(text="This may take a moment..."):
            x = time.time()
            text = get_correct(text)
            y = time.time()
            st.write(f"Time to prediction: {y-x} seconds")
        st.write(text)
    if st.button("Summarize"):
        with st.spinner(text="This may take a moment..."):
            x = time.time()
            text = get_correct_sum(text,number)
            y = time.time()
            st.write(f"Time to prediction: {y-x} seconds")
        st.write(text)

if __name__ == "__main__":
    main()
