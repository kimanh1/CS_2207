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
from sklearn.metrics import mean_squared_error
import numpy as np
from catboost import CatBoostRegressor
from sklearn.metrics import mean_absolute_error
import joblib
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
# loading train data set in dataframe from train_data.csv file

df1 = pd.read_csv("./processed_for_lease_data_with_target.csv")

df2 = pd.read_csv("./processed_for_sale_data_with_target.csv")
print()
target1 = np.array(df1["PRICE"])
target2 = np.array(df2["PRICE"])
train1=np.array(df1.drop(columns="PRICE"))
train2=np.array(df2.drop(columns="PRICE"))
print(df1["LAND_TYPE_vp"].dtype)
model1 = CatBoostRegressor(
    iterations=10000,  # Number of boosting iterations
    learning_rate=0.01,  # Step size
    depth=8,  # Tree depth
    verbose=100  # Show progress every 100 iterations
    )
model2 = CatBoostRegressor(
    iterations=10000,  # Number of boosting iterations
    learning_rate=0.01,  # Step size
    depth=8,  # Tree depth
    verbose=100  # Show progress every 100 iterations
    )

kf =KFold(n_splits=5, shuffle=True, random_state=42)

accuracies = []
medianRMSE=[]
medianMAE=[]

for i, (train_index, test_index) in enumerate(kf.split(train1)):
    X_train, X_test = train1[train_index], train1[test_index]
    y_train, y_test = target1[train_index], target1[test_index]
    print(f"Fold {i}:")
    print(f"  Train: index={train_index}")
    print(f"  Test:  index={test_index}")
    # Train the model
    model1.fit(X_train, y_train)
    
    y_pred = model1.predict(X_test)
    accuracy = model1.score(X_test, y_test) 
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    accuracies.append(accuracy)
    medianMAE.append(mae)
    medianRMSE.append(rmse)
average_accuracy = sum(accuracies) / len(accuracies)
average_MAE = sum(medianMAE) / len(medianMAE)
average_RMSE = sum(medianRMSE) / len(medianRMSE)
print(f"Average R^2: {average_accuracy}")
print(f"Average MAE: {average_MAE}")
print(f"Average RMSE: {average_RMSE}")


accuracies = []
medianRMSE=[]
medianMAE=[]
i=0
for i, (train_index, test_index) in enumerate(kf.split(train2)):
    X_train, X_test = train2[train_index], train2[test_index]
    y_train, y_test = target2[train_index], target2[test_index]
    print(f"Fold {i}:")
    print(f"  Train: index={train_index}")
    print(f"  Test:  index={test_index}")
    # Train the model
    model2.fit(X_train, y_train)
    
    y_pred = model2.predict(X_test)
    accuracy = model2.score(X_test, y_test) 
    mae = mean_absolute_error(y_test, y_pred)
    meanSquaredError = ((y_pred - y_test) ** 2).mean()
    rmse = np.sqrt(meanSquaredError)
    accuracies.append(accuracy)
    medianMAE.append(mae)
    medianRMSE.append(rmse)
average_accuracy = sum(accuracies) / len(accuracies)
average_MAE = sum(medianMAE) / len(medianMAE)
average_RMSE = sum(medianRMSE) / len(medianRMSE)
print(f"Average R^2: {average_accuracy}")
print(f"Average MAE: {average_MAE}")
print(f"Average RMSE: {average_RMSE}")


# ytesst=model.predict([[-0.964187343,-0.095079871,	113,	4,	1856.904762,	0,	29,	28,	0,	2]])
# print(ytesst)

# # Calculate residuals
# residuals = y_test - y_pred

# Plot residuals
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
# joblib.dump(model1, "cb_model_sale.sav")
# joblib.dump(model2, "cb_model_lease.sav")
## change na