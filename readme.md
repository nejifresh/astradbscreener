This application demonstrates the use of ASTRADB as a vector store for matching a job description against a number of resumes. The hiring manager provides a job description and K matching results, then uploads multiple resumes and the application reviews and matches the best fit for the job position. The application also generates a summary for each resume and tries to justify why the particular resume was selected as a good match for the job position.
The application is written in Python. Streamlit is used for the front end. The application is currently deployed on the following URL - https://astradbscreener.onrender.com/

To run the application locally:
1. Pull the repo using Git
2. Open the project in an IDE of your choice
3. Create a .env file and add the following environent variables: ASTRA_DB_APPLICATION_TOKEN, ASTRA_DB_API_ENDPOINT, OPENAI_API_KEY
4. Run the following command - streamlit run main.py