# FederatedLearningHealthcare

Applied project investigating Federated Learning in the Healthcare industry. For full details on project, please read blog found here.  

Other projects on my work in federated learning:
* Introduction to federated learning:
* Text Summarization and Federated Learning:

## Summary
Patient and data privacy is a core tenant of working with healthcare data, which can make data sharing very difficult. This causes data to be siloed across multiple data owners, each making their own AI algorithms.  Federated learning provides a framework that enables collaborative without sharing data or violating patient privacy.

This project explores the capability of using federated learning within healthcare. I run an experiment that evaluates model results at varying levels of model complexity between traditional learning methods and federated learning. I demonstrate that through utilizing federated learning, we can gather additional signal and employ more complex models.  All without violating patient privacy. 

The selected experiment is simple because the project doubles as a sort of learning material (providing code walkthroughs)

## Model Flow
I simulate a real world scenario where three healthcare institutions wish to participate in a shared data consortium to enable collaborative training for their hospital readmission models. 

1. Data Prep
  * Extract [UCI Diabetes Hospital Readmission data](https://archive.ics.uci.edu/ml/datasets/Diabetes+130-US+hospitals+for+years+1999-2008#)
  * Split into various parties: Single provider and Shared Data Consortium
    * Single provider is focused on diseases related to the circulatory systems (30% of the data)
      * test data is derived from single provider's data
    * Shared data consortium is the two other parties (35% of data each)
  * Prep data for ID3 algorithm
  
2. Baseline model
  * Create baseline model using single provider data only
  * traditional training method at varying maximum depths
  
3. Federated Learning
  * Collaboratively train using all data to create super-readmission model at varying maximum depths
  * I cannot share Federated learning code, but I can share the inputs which are found in generate_configs.py and hospital_data_handler.py
  
4. Compare Results
  * Compare the results of all models 

## Experiment overview and results
I generate two ID3 decision tree models (baseline and federated learning).  Each model is run with varying level of max tree depths (two through six).  I compare the results the models at each depth.

Metric Results:
![alt_text](https://github.com/austnbell/FederatedLearningHealthcare/blob/master/Pics/Metrics.png)

We see a very similar story occurring in each graph. For low max depth ranges, our baseline model appears to perform better than our federated learning model. However, as we increase the maximum depth, the federated learning model performs better.  Finally, as maximum depth increases even further, both models appear to perform worse, yet the federated learning model continues to perform better than our baseline model. 

Given that our test data is a subset of the single provider’s data, we expect that the data trained in our baseline model to be much very similar to the test data, whereas the additional data included in the federated learning model would be different to the test data.   For this reason, we observe that the baseline model actually performs better than federated learning level at low depths, despite our federated learning model being trained on more data. However, as model complexity increases, our federated learning model gathers additional signal from the inclusion of the slightly out-of-domain  data resulting in better model results. 

In the graph below, I display the percent difference between metric scores, which is defined as the difference in score between the federated learning model and the baseline model.  We observe across all metrics that once model depth reaches a certain level (four) then the federated learning model starts to significantly outperform the baseline model and continues to do so for all further depths. 

![alt_text](https://github.com/austnbell/FederatedLearningHealthcare/blob/master/Pics/Percent_difference.png)

## Conclusion

The federated learning framework enables the data scientist to train on additional data, which results in better performing models. Within our experiment, we demonstrate that this effect occurs even when third party local models are trained using slightly out-of-domain data (i.e., patients with a primary diagnosis unrelated to the circulatory system).  The additional signal gathered from the new local models prevents overfitting at higher levels of model complexity. The result of which is a model with higher level pattern recognition and stronger performance. 
