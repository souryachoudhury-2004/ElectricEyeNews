from email_agent import mail
import streamlit as st
import requests


st.title("Electric Eye News")
st.subheader("A custom compilation of recent news, just for you!")

with st.form(key="editor"):
    receiver_email = st.text_input("Please enter your email address.")
    news_topic = st.text_input("Please enter any topic of your choice.")
    article_count = st.number_input("Please enter the maximum number of articles you want in your feed.", step=1)
    send_button = st.form_submit_button("Send!")

    url = f"https://newsapi.org/v2/everything?q={news_topic}" \
          "&sortBy=publishedAt&apiKey=44b9ab3b4632425681b6253ce70f7131"


    try:
        if send_button:
            if news_topic == "":
                st.info("Please enter a topic!")
            elif receiver_email == "":
                st.info("Please enter a valid email address!")
            elif article_count == 0:
                st.info("Please enter the number of articles you want.")
            else:
                request = requests.get(url)
                content = request.json()

                if len(content["articles"]) < article_count:
                    article_count = len(content["articles"])


                for article in content["articles"][: article_count]:
                    title = article["title"]
                    if title is None:
                        title = ""
                    description = article["description"]
                    link = article["url"]
                    message = f"Subject: {title} \n\n {description} \n\n {link}"
                    message = message.encode("utf-8")
                    mail(receiver_email, message)
                    st.info("Compilation Sent!")

    except:
        st.info("There was an error :(")


