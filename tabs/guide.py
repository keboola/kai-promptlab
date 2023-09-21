import streamlit as st 

def app_guide():
    st.markdown(""" 

Welcome to Keboola PromptLab! Before you start experimenting, here's your quick step-by-step guide:

                
- 🔄 __Connect your data__ – Start by connecting to the Keboola storage, you'll need your API token to do this. Just go to _Settings_ in your Keboola account and find the _API Tokens_ tab (see the [documentation](https://help.keboola.com/management/project/tokens/) for more information).
Once connected, you'll be able to select the bucket and table you want to work with.

- 📊 __Preview your data__ – After connecting to the selected table, you should see a preview of your data. Make sure you're working with the right table, and let's do some prompt magic!
                
- 🛠️ __Improve your prompt__ – Already have ideas but still unsure about the wording of your current prompt? No worries! Enter your idea, hit the __'Improve'__ button and voilà! You'll get an improved version that follows prompt engineering best practices.

- 🤹 __Test your prompts__ – This is your playground. You can fill in 1-3 prompts to run with your data. Each prompt comes with its own settings, allowing you to tweak parameters or even compare results across different models. For example, you can test how a prompt performs with a higher temperature setting vs. a lower one. 🌡️ Additionally, you have the flexibility to select the portion of your dataset you'd like to work with.

- 🎢 __Ready, set, go!__ – Once you're happy with your prompts and settings, hit that __'OKaaaAAAaaAYYYy LETS GO'__ button. The app will then work its magic, running all the prompts and return the responses.

- 🔍 __Analyze the responses__ – The moment of truth! Review the responses and see which prompt fits your data best. Check the responses similarity score to pinpoint areas where prompts might seem contradictory. This is a great way to refine your prompts and understand potential model challenges.

_Last but not least: To run the experiments, you'll need an OpenAI API key. If you don't have one, you can get it [here](https://platform.openai.com/account/api-keys)._
                       """)
if __name__ == "__main__":
    app_guide()