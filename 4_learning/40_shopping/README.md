# Problem Set 40: Shopping
The primary objective of this project is to predict whether a user visiting an online shopping website will make a purchase or not based on various features about their session and behavior. By successfully predicting this, the website can potentially make decisions about how to interact with the user, such as offering discounts if it predicts the user might not complete a purchase.

The problem is a *binary classification problem* where the goal is to classify users into one of two classes: those who will make a purchase (labelled as TRUE) and those who won't (labelled as FALSE).

This project uses a *nearest-neighbor classifier*. The idea behind nearest neighbors is that similar data points (in terms of features) will have similar outputs. So, for a given user session, the classifier would look for the most similar sessions in the training data and use their outcomes to make a prediction.

After training, the model's predictions on the test set are compared to the actual outcomes to evaluate its performance using sensitivity and specificity.

The project encapsulates the end-to-end process of machine learning, from understanding and processing the data to training a model and evaluating its performance.