from sklearn.metrics import mean_absolute_error
import pandas as pd
# from sklearn.ensemble import StackingRegressor
from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
import numpy as np
# from itertools import combinations
# import xgboost as xgb
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.ensemble import HistGradientBoostingClassifier
# from sklearn.svm import SVR
# import matplotlib.pyplot as plt
# from sklearn.metrics import mean_squared_error
import numpy as np
from catboost import CatBoostRegressor
# from sklearn.metrics import mean_absolute_error
# import joblib
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
# loading train data set in dataframe from train_data.csv file

df = pd.read_csv("./processed_for_sale_data_with_target.csv")
target = np.array(df["PRICE"])
train=np.array(df.drop(columns="PRICE"))

model = CatBoostRegressor(
    iterations=10000,  # Number of boosting iterations
    learning_rate=0.01,  # Step size
    depth=8,  # Tree depth
    verbose=100  # Show progress every 100 iterations
    )

kf =KFold(n_splits=5, shuffle=True, random_state=42)
print(kf)
accuracies = []
for i, (train_index, test_index) in enumerate(kf.split(train)):
    X_train, X_test = train[train_index], train[test_index]
    y_train, y_test = target[train_index], target[test_index]
    print(f"Fold {i}:")
    print(f"  Train: index={train_index}")
    print(f"  Test:  index={test_index}")
    # Train the model
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = model.score(X_test, y_test) 
    print(accuracy)
     # Calculate accuracy
    accuracies.append(accuracy)
    

average_accuracy = sum(accuracies) / len(accuracies)
print(f"Average Accuracy: {average_accuracy}")
# ytesst=model.predict([[-0.964187343,-0.095079871,	113,	4,	1856.904762,	0,	29,	28,	0,	2]])
# print(ytesst)

# # Calculate residuals
# residuals = y_test - y_pred

# # Plot residuals
# plt.scatter(y_pred, residuals)
# plt.axhline(y=0, color='r', linestyle='--')
# plt.xlabel("Predicted Prices")
# plt.ylabel("Residuals")
# plt.title("Residuals vs Predicted Prices")
# plt.show()
# mse = mean_squared_error(y_test, y_pred)
# print("mse:",mse)
# rmse = np.sqrt(mse)
# print("rmse",rmse)
# mae = mean_absolute_error(y_test, y_pred)
# print("mae:",mae)

# print('-----------------------')
# joblib.dump(model, "cb_model.sav")