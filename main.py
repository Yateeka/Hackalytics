import streamlit as st

def main():
    st.title("Name Combiner")
    
    # Ask for the first name
    first_name = st.text_input("Enter the first name:")
    
    # Ask for the second name
    second_name = st.text_input("Enter the second name:")
    
    # Combine the names
    combined_name = first_name + " " + second_name
    # Generate cute or possible couple names
    couple_name = first_name[:len(first_name)//2] + second_name[len(second_name)//2:]
    
    # Display the combined name
    st.write("Combined Name:", combined_name)

if __name__ == "__main__":
    main()