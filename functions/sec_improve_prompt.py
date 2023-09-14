# sec_improve_prompt.py

import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

def improve_prompt():

    if 'improved_content' not in st.session_state:
        st.session_state.improved_content = ""
    
    if 'last_user_input' not in st.session_state:
        st.session_state.last_user_input = ""

    #template = """
    #You are an Expert Prompt Creator. Your goal is provide a revised prompt that is ready to be used. 
#
 #   1. Start with clear, precise instructions, placed at the beginning of the prompt. 
  #  2. Include specific details about the desired context, outcome, length, format, and style. 
   # 3. Provide examples of the desired output format, if possible. 
    #4. Use appropriate leading words or phrases to guide the desired output, especially if code generation is involved. 
#    5. Use direct and precise language. 
 #   6. Provide guidance on what should be done. 
  #  Remember to ensure the revised prompt remains true to the user's original intent. Provide only the revised prompt. 
#
        
  #  Below is the poorly worded prompt.
 #   PROMPT: {input}

   # YOUR RESPONSE:
   # """
    template = """
You are an Expert Prompt Creator. Your goal is to help me craft the best possible prompt for my needs. Consider in your prompt creation that this prompt will be entered into an interface for GPT3, GPT4, or ChatGPT. 

The prompt you are creating should be written from the perspective of a user making a request to ChatGPT. Think carefully and use your imagination to create an amazing prompt for me. 

Only respond with the improved prompt.

MY PROMPT: {input}
    
YOUR RESPONSE:
    """
    prompt = PromptTemplate(
        input_variables=["input"],
        template=template
        )

    def load_LLM():
        llm=OpenAI(temperature=.5)
        return llm

    llm=load_LLM()

    #st.subheader("🛠️ Improve")
    
    color_hex = "#288CFC"
    subheader_html_hex = f"""
    <h3 style="border-bottom: 2px solid {color_hex}; margin-bottom: 10px;">
    Improve
    </h3>
    """
    st.markdown(subheader_html_hex, unsafe_allow_html=True)
    
    st.write('Already have ideas but still not sure about the wording of your current prompt?')
    
    with st.chat_message("user", avatar="💬"):
        user_input = st.text_input("", label_visibility="collapsed")
        
        if user_input and user_input != st.session_state.get("last_user_input", ""):
            improved_input = llm(prompt.format(input=user_input))
            st.session_state.improved_content = improved_input
            st.session_state.last_user_input = user_input
 
        if 'improved_content' in st.session_state:
            st.write(st.session_state.improved_content)
        

if __name__ == "__main__":
    improve_prompt()

#    I want you to act as a ChatGPT prompt generator, I will send a topic, you have to generate a ChatGPT prompt based on the content of the topic, the prompt should start with "I want you to act as ", and guess what I might do, and expand the prompt accordingly.