import streamlit as st
import string

def caesar_decoder(text, shift):
    """
    Decode text using Caesar cipher with the given shift
    """
    result = ""
    
    for char in text:
        if char.isupper():
            # Handle uppercase letters
            result += chr((ord(char) - shift - 65) % 26 + 65)
        elif char.islower():
            # Handle lowercase letters
            result += chr((ord(char) - shift - 97) % 26 + 97)
        else:
            # Keep non-alphabet characters as they are
            result += char
    
    return result

def brute_force_decoder(text):
    """
    Try all possible shifts (1-25) and return all results
    """
    results = []
    for shift in range(1, 26):
        decoded = caesar_decoder(text, shift)
        results.append((shift, decoded))
    return results

def main():
    st.set_page_config(
        page_title="Caesar Cipher Decoder",
        page_icon="🔐",
        layout="wide"
    )
    
    # Header
    st.title("🔐 Caesar Cipher Decoder")
    st.markdown("---")
    
    # Sidebar with information
    with st.sidebar:
        st.header("About Caesar Cipher")
        st.write("""
        The Caesar cipher is one of the simplest encryption techniques.
        It works by shifting each letter in the plaintext by a fixed number
        of positions down the alphabet.
        
        **Example:**
        - Shift 3: A → D, B → E, C → F, etc.
        - To decode, shift letters backward by the same amount.
        """)
        
        st.header("How to Use")
        st.write("""
        1. Enter your encoded text
        2. Choose decoding method:
           - **Known Shift**: If you know the shift value
           - **Brute Force**: Try all possible shifts (1-25)
        3. View the decoded results
        """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Text input
        encoded_text = st.text_area(
            "Enter encoded text:",
            height=150,
            placeholder="Enter the text you want to decode here...",
            help="Paste or type the encoded Caesar cipher text"
        )
        
        # Decoding method selection
        decoding_method = st.radio(
            "Select decoding method:",
            ["Known Shift", "Brute Force"],
            horizontal=True
        )
    
    with col2:
        if decoding_method == "Known Shift":
            # Shift input for known shift method
            shift = st.slider(
                "Select shift value:",
                min_value=1,
                max_value=25,
                value=3,
                help="The number of positions each letter was shifted during encoding"
            )
        else:
            # Information for brute force method
            st.info("Brute force will try all 25 possible shifts and show all results.")
    
    # Decode button and results
    if st.button("Decode Text", type="primary"):
        if not encoded_text.strip():
            st.warning("Please enter some text to decode.")
            return
        
        if decoding_method == "Known Shift":
            # Known shift decoding
            decoded_text = caesar_decoder(encoded_text, shift)
            
            st.subheader("Decoded Result")
            st.code(decoded_text, language="text")
            
            # Display shift information
            st.info(f"Applied backward shift of {shift} positions")
            
        else:
            # Brute force decoding
            st.subheader("Brute Force Results")
            st.write("Trying all possible shifts (1-25):")
            
            results = brute_force_decoder(encoded_text)
            
            # Create tabs for better organization
            tab1, tab2 = st.tabs(["All Results", "Most Likely"])
            
            with tab1:
                # Display all results in an expandable format
                for shift_val, decoded in results:
                    with st.expander(f"Shift {shift_val}: {decoded[:50]}..." if len(decoded) > 50 else f"Shift {shift_val}: {decoded}"):
                        st.write(f"**Shift:** {shift_val}")
                        st.code(decoded, language="text")
                        st.write(f"**Length:** {len(decoded)} characters")
            
            with tab2:
                # Try to identify the most likely result
                st.write("**Most likely candidates (common English patterns):**")
                
                # Simple heuristic: look for common English words
                common_words = ['the', 'and', 'you', 'that', 'was', 'for', 'are', 'with', 'his', 'they']
                
                likely_results = []
                for shift_val, decoded in results:
                    # Count occurrences of common words
                    score = 0
                    decoded_lower = decoded.lower()
                    for word in common_words:
                        score += decoded_lower.count(f" {word} ") + decoded_lower.count(f" {word}.") + decoded_lower.count(f" {word},")
                    
                    if score > 0:
                        likely_results.append((score, shift_val, decoded))
                
                # Sort by score (highest first)
                likely_results.sort(reverse=True)
                
                if likely_results:
                    for score, shift_val, decoded in likely_results[:3]:  # Show top 3
                        st.write(f"**Shift {shift_val}** (Score: {score})")
                        st.code(decoded, language="text")
                        st.markdown("---")
                else:
                    st.write("No obvious English patterns detected. Check all results in the 'All Results' tab.")
    
    # Example section
    st.markdown("---")
    st.subheader("Example")
    
    example_col1, example_col2 = st.columns(2)
    
    with example_col1:
        st.write("**Encoded text (Shift 3):**")
        st.code("WKH HDVW HUJLQ ZLOO ULVH DJDLQ")
    
    with example_col2:
        st.write("**Decoded text:**")
        st.code("THE EAST ENGINE WILL RISE AGAIN")
    
    # Footer
    st.markdown("---")
    st.caption("Caesar Cipher Decoder | Made with Streamlit")

if __name__ == "__main__":
    main()