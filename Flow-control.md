As we talked about just before, there are two solutions to this data upload default situation. We can provide a default file to use until the user interacts with the application, or we can stop the app until a file is uploaded. Let’s start with the first option. The following code uses the st.file_uploader() function from within an if statement. If the user uploads a file, then the app uses that; if they do not, then we default to the file we have used before:

<img width="567" alt="Screenshot 2024-04-30 at 10 14 19 AM" src="https://github.com/andysingal/DataScience-Streamlit/assets/20493493/45444cfc-9eee-4518-a492-da0b25bddbff">


Our second option is to stop the application entirely unless the user has uploaded a file. For that option, we’re going to use a new Streamlit function called stop(), which (predictably) stops the flow whenever it is called. It is best practice to use this to find errors in the app and to encourage the user to make some changes or describe the error that is happening. This is not necessary for us but is a good thing to know for future applications. The following code uses an if-else statement with st.stop() in the else statement to prevent the entire app from running when st.file_uploader() is unused 

<img width="568" alt="Screenshot 2024-04-30 at 10 16 39 AM" src="https://github.com/andysingal/DataScience-Streamlit/assets/20493493/7462d4cc-cbfc-4f93-921a-90ebef7896a4">
