# DOTA 2 Match Result Prediction

## Datasets 

<ul>
<li><a href="https://www.kaggle.com/devinanzelmo/dota-2-matches">Dota 2 Matches from Kaggle</a></li>
<li>Public match data fetched using the Opendota API</li>
</ul>

## Analysis

It is a known fact that predicting a Dota 2 match's outcome at any given point of time during the match is very hard even with all related data such as net worth advantage, team kills, creep scores, hero levels, heroes and tower scores. Valve's Dota Plus win prediction during a pro game is an excellent example of this. The heavy fluctuation around the halfway probability mark throughout the game creates uncertainty in the calculated outcome even with a state-of-the-art-model.

For a lower ranked public game, there are more trends that models can pick up on. This is reflected in the hero winrates during a specific major patch on a source like Dotabuff.

However, lower rank means lower skill and the countering ability of a hero is sometimes lost due to lower mechanical skill and subpar/ineffective item builds.

This would mean that the played heroes alone would not suffice to give an accurate prediction of the result. We would need to add items purchased by the players into our feature set for more accurate predictions on a test set.

To show the difference in performance between features of heroes and features of heroes and items, the same models were trained on both datasets to benchmark them.

I decided to use two separate sources to verify that the inference holds irrespective of source. The kaggle dataset contains older matches from 2019 in a wide skill bracket while the opendota dataset only contains matches skilled above average and are more recent.

## Training

The features were one hot encoded with each hero having a radiant and dire slot to account for side bias and team separation.

The kaggle-heroes dataset contains 50000 rows and 222 features while the heroes&items data contains 50000 rows and 612 features with a test split of 10% for both.

The opendota dataset contains 50000 rows and 242 features (more heroes due to it being more recent) with a test split of 5%.

All machine learning algorithms were trained after using scikit-learn's GridSearchCV for hyperparameter tuning

### Machine Learning and Deep Learning Algorithms


<ul>
<strong>
<li>Decision Tree Classifier</li>
<li>Logistic Regression</li>
<li>Stochastic Gradient Descent Classifier</li>
<li>Linear Support Vector Machine</li>
<li>Gaussian Naive Bayes</li>
<li>XGBClassifier</li>
<li>Random Forest Classifier</li>
<li>Multi-Layer Perceptron</li>
<li>Soft-Voting Ensemble (LR, GNB, XGB, RFC)</li>
</strong>
</ul>

## Results

### Heroes Only

<table>
<tr>
<th>Algorithm</th>
<th>Accuracy</th>
<th>Precision</th>
<th>Recall</th>
</tr>
<tr>
<td>Decision Tree</td>
<td>55%</td>
<td>57%</td>
<td>67%</td>
</tr>
<tr>
<td>Logistic Regression</td>
<td>59%</td>
<td>61%</td>
<td>65%</td>
</tr>
<tr>
<td>Stochastic Gradient Descent SVM</td>
<td>59%</td>
<td>62%</td>
<td>62%</td>
</tr>
<tr>
<td>Linear SVM</td>
<td>59%</td>
<td>61%</td>
<td>64%</td>
</tr>
<tr>
<td>Gaussian Naive Bytes</td>
<td>60%</td>
<td>60%</td>
<td>70%</td>
</tr>
<tr>
<td>XGB Classifier</td>
<td>59%</td>
<td>61%</td>
<td>64%</td>
</tr>
<tr>
<td>Random Forest</td>
<td>59%</td>
<td>60%</td>
<td>69%</td>
</tr>
<tr>
<td>Multi-layer Perceptron</td>
<td>59-60%</td>
<td> - </td>
<td> - </td>
</tr>
<tr>
<td>Soft-Voting Ensemble</td>
<td>62%</td>
<td> - </td>
<td> - </td>
</tr>

</table>

### Heroes+Items

<table>
<tr>
<th>Algorithm</th>
<th>Accuracy</th>
<th>Precision</th>
<th>Recall</th>
</tr>
<tr>
<td>Decision Tree</td>
<td>83%</td>
<td>85%</td>
<td>84%</td>
</tr>
<tr>
<td>Logistic Regression</td>
<td>97%</td>
<td>97%</td>
<td>97%</td>
</tr>
<tr>
<td>Stochastic Gradient Descent SVM</td>
<td>97%</td>
<td>98%</td>
<td>96%</td>
</tr>
<tr>
<td>Linear SVM</td>
<td>97%</td>
<td>97%</td>
<td>97%</td>
</tr>
<tr>
<td>Gaussian Naive Bytes</td>
<td>86%</td>
<td>86%</td>
<td>88%</td>
</tr>
<tr>
<td>XGB Classifier</td>
<td>95%</td>
<td>96%</td>
<td>94%</td>
</tr>
<tr>
<td>Random Forest</td>
<td>95%</td>
<td>96%</td>
<td>94%</td>
</tr>
<tr>
<td>Multi-layer Perceptron</td>
<td>97-99%</td>
<td> - </td>
<td> - </td>
</tr>

</table>

## Conclusion 

From the results, it is pretty obvious that heroes alone is not enough to reliably predict the outcome of a match as the factors that come into play during the match have an extremely large role in deciding the outcome. One of these factors are the items purchased which provided us with a much better model across the board. The best classification model from the heroes dataset was the voting classifier ensemble of Logistic Regression, Gaussian Naive Bytes, XGBClassifier and The Random Forest which gave an accuracy of 62% on the test set which is quite good considering the lack of strongly deciding factors. Meanwhile, the models trained on heroes and items resulted in a worst performance of 83% and a best of ~99% accuracy on the test set using a deep neural network!
