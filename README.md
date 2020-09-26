# Detecting Potential Misinformation Spreaders during Disaster.
**This project was made during `ShellHacks2020` for `#HealthyConversations` challenge.**

##### Problem Statement:
Social media platforms are important and powerful means of communication. Twitter also provides a platform where information is exchanged every second through conversations. Unfortunately, spread of misinformation is demaging the reputaion of these platforms and could cause huge loss. The spread of misinformation is especially troublemsome in case of disasters.Natural Language Procesiing techniques can be applied to detect twitter users who are potential misinformation spreaders and their tweets could be analysed more closely in case of disaster to stop the spread of misinformation as effectively as possible.

##### Data:
Two datasets were used for this project.
1) Data for profiling Fake News spreaders is can be found [here.](https://pan.webis.de/clef20/pan20-web/author-profiling.html#data)
2) Dataset for detecting tweets about disaster is available [here.](https://www.kaggle.com/c/nlp-getting-started)

##### What's in notebooks ?
**01_data_loading_and_feature_selection** : This notebook contains script for data loading and preparation . For each user 100 tweets are avalible but not all of them are inoformative to classify the user. So Chi-Square is used to filter out the (30) most important tweets for each user.  
**02_model** : It contains models fitted to both datasets. Random Forest and SVM classifier (SVC) are used to build the model.

##### How to use this repo ? 
- **Step 1 (optional):** Instructions for making virtual environment could be found [here](https://docs.python.org/3/tutorial/venv.html "here")

- **Step 2:** Type the following command to install necessary libraries:

    ```
    pip install -r requirements.txt
    ```
- **Step 3:** `sample.json` contains some tweets from a user. Type following to check if it is a potential misinformation spreader or someone who tweets about disaster or both.
    ```
    python sample.py
    ```
**Output for sample**:
![output for sample.py](sample_output.png)

##### Evaluation: 
Accuracy was used as metric bacause the classes are balanced. 3 folds cross-validation was used to report the results.
- Misinsformation spreader or not ? `73 %`
- Disaster or not ? `84 %`

