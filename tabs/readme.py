import streamlit as st

def page1():

    st.markdown("""

        #### Heyo 👋 Welcome to Keboola PromptLab!
                

        This app was created as a playground where you can try out different variations of your prompts and find the best one for your dataset.
                
        ---
        ### Where to:
                
        🤹‍♂️ __Playground__ – Try up to 3 different prompts on a sample of your dataset, have an improved version of your prompt generated or look at the output quality rating /n
                
        🐙 __Improve your prompt__ – Some might call it advanced prompting – rephrase your prompt to be more specific and contextual, see how it changes with different parameters
                
        📚 __Docs__ – Useful links that might come in handy
                
        Your data should be uploaded from Keboola, if not you can also upload it in the left sidebar. Also fill in your OpenAI API key there, be sure to do that before you start testing your prompts

      
""")
   
if __name__ == "__main__":
    page1()