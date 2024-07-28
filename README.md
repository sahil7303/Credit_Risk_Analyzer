# Credit_Risk_Analyzer

<div>
  
  <a href="">[![Go to App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://creditriskanalyzer-sapf6khmekgqcydmmdnrkk.streamlit.app/)</a>    

</div>

## Project Description

The Credit Risk Analyzer App is a Streamlit-based web application designed to predict an individual's credit score based on various financial and demographic factors. This app helps users understand their creditworthiness and provides a visual representation of their credit score category (Good, Regular, Poor).


## Usage

1. Open the app using the link given above.

2. Fill out the form on the sidebar with your financial and demographic information.

3. Click the "ANALYZE" button to see your predicted credit score.

4. Optionally, click the "Generate Random Profile" button to see a randomly generated profile and its credit score prediction.

## File Structure

```bash
credit-score-classification-app/      
├── data
│   ├── external       # Data from third party sources.
│   ├── interim        # Intermediate data that has been transformed.
│   └── processed      # The final, canonical data sets for modeling.
│
├── app                # Streamlit App.
│
├── models             # Trained and serialized models.
│
├── notebooks          # Jupyter notebooks
│
├── references         # Data dictionary.
│
├── README.md  
└── requirements.txt   # List of required packages
```