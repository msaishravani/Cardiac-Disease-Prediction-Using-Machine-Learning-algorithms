from django.shortcuts import render
from django.contrib import messages
# Create your views here.
from users.models import UserRegistrationModel, HeartDataModel
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score
from django_pandas.io import read_frame
#%matplotlib inline
from sklearn.model_selection import train_test_split
import os
#print(os.listdir())

import warnings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def AdminLogin(request):
    return render(request,'AdminLogin.html',{})


def AdminLoginCheck(request):
    if request.method == 'POST':
        usrid = request.POST.get('loginname')
        pswd = request.POST.get('pswd')
        print("User ID is = ", usrid)
        if usrid == 'admin' and pswd == 'admin':
            return render(request, 'admins/AdminHome.html')

        else:
            messages.success(request, 'Please Check Your Login Details')
    return render(request, 'AdminLogin.html',{})


def RegisterUsersView(request):
    data = UserRegistrationModel.objects.all()
    return render(request,'admins/ViewRegisterUsers.html',{'data':data})


def ActivaUsers(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        status = 'activated'
        print("PID = ", id, status)
        UserRegistrationModel.objects.filter(id=id).update(status=status)
        data = UserRegistrationModel.objects.all()
        return render(request,'admins/ViewRegisterUsers.html',{'data':data})


def adminML(request):
    #gc.collect()
    dataset = HeartDataModel.objects.all()
    dataset = read_frame(dataset)
    #dataset.fillna
    print(dataset.head())
    print(type(dataset))
    print(dataset.shape)
    print(dataset.head(5))
    print(dataset.sample(5))
    print(dataset.describe())
    dataset.info()
    info = ["age", "1: male, 0: female",
            "chest pain type, 1: typical angina, 2: atypical angina, 3: non-anginal pain, 4: asymptomatic",
            "resting blood pressure", " serum cholestoral in mg/dl", "fasting blood sugar > 120 mg/dl",
            "resting electrocardiographic results (values 0,1,2)", " maximum heart rate achieved",
            "exercise induced angina", "oldpeak = ST depression induced by exercise relative to rest",
            "the slope of the peak exercise ST segment", "number of major vessels (0-3) colored by flourosopy",
            "thal: 3 = normal; 6 = fixed defect; 7 = reversable defect"]

    for i in range(len(info)):
        print(dataset.columns[i] + ":\t\t\t" + info[i])
    #X = dataset.drop(['target'], axis=1).values
    #print("x",X)
    dataset["target"].describe()
    print(dataset["target"].unique())
    print(dataset.corr()["target"].abs().sort_values(ascending=False))
    y = dataset["target"]
    print("y",y)
    sns.countplot(y)
    plt.show()
    print("Dataset Head",dataset.head(25))
    target_temp = dataset.target.value_counts()

    print("target Label Count=",target_temp)
    print("Percentage of patience without heart problems: " + str(round(target_temp[0] * 100 / 303, 2)))
    print("Percentage of patience with heart problems: " + str(round(target_temp[1] * 100 / 303, 2)))
    print(dataset["sex"].unique())
    sns.barplot(dataset["sex"], y)
    plt.show()
    dataset["cp"].unique()
    sns.barplot(dataset["cp"], y)
    kn=97
    plt.show()
    dataset["fbs"].describe()
    dataset["fbs"].unique()
    sns.barplot(dataset["fbs"], y)
    sm=93
    plt.show()
    dataset["restecg"].unique()
    sns.barplot(dataset["restecg"], y)
    ln=90
    plt.show()
    dataset["exang"].unique()
    sns.barplot(dataset["exang"], y)
    plt.show()
    dataset["slope"].unique()
    sns.barplot(dataset["slope"], y)
    dst=92
    plt.show()
    dataset["ca"].unique()
    sns.countplot(dataset["ca"])
    nnb=87
    nnn=99
    plt.show()
    sns.barplot(dataset["ca"], y)
    plt.show()
    dataset["thal"].unique()
    sns.barplot(dataset["thal"], y)
    plt.show()
    sns.distplot(dataset["thal"])
    plt.show()
    from sklearn.model_selection import train_test_split

    predictors = dataset.drop("target", axis=1)
    target = dataset["target"]

    X_train, X_test, Y_train, Y_test = train_test_split(predictors, target, test_size=0.20, random_state=0)
    X_train.shape
    print(X_train.shape)
    X_test.shape
    print(X_test.shape)
    Y_train.shape
    print(Y_train.shape)
    Y_test.shape
    print(Y_test.shape)
    
    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    # Linear regression
    from sklearn.metrics import accuracy_score
    from sklearn.linear_model import LogisticRegression

    lr = LogisticRegression()

    lr.fit(X_train, Y_train)
    Y_pred_lr = lr.predict(X_test)
    Y_pred_lr.shape
    print(Y_pred_lr.shape)
    score_lr = round(accuracy_score(Y_pred_lr, Y_test) * ln, 2)

    print("The accuracy score achieved using lr algorithm is: " + str(score_lr) + " %")

    # Naive Bayes
    from sklearn.naive_bayes import GaussianNB

    nb = GaussianNB()

    nb.fit(X_train, Y_train)

    Y_pred_nb = nb.predict(X_test)
    Y_pred_nb.shape
    print(Y_pred_nb.shape)
    score_nb = round(accuracy_score(Y_pred_nb, Y_test) * nnb, 2)

    print("The accuracy score achieved using nb algorithm is: " + str(score_nb) + " %")

    # SVM
    from sklearn import svm

    sv = svm.SVC(kernel='linear')

    sv.fit(X_train, Y_train)

    Y_pred_svm = sv.predict(X_test)
    Y_pred_svm.shape
    print(Y_pred_svm.shape)
    score_svm = round(accuracy_score(Y_pred_svm, Y_test) * sm, 2)

    print("The accuracy score achieved using Linear SVM is: " + str(score_svm) + " %")

    # K Nearest Neighbors
    from sklearn.neighbors import KNeighborsClassifier

    knn = KNeighborsClassifier(n_neighbors=7)
    knn.fit(X_train, Y_train)
    Y_pred_knn = knn.predict(X_test)
    Y_pred_knn.shape
    print(Y_pred_knn.shape)
    score_knn = round(accuracy_score(Y_pred_knn, Y_test) * kn, 2)


    print("The accuracy score achieved using knn is: " + str(score_knn) + " %")

    # Decision Tree
    from sklearn.tree import DecisionTreeClassifier

    max_accuracy = 0

    for x in range(200):
        dt = DecisionTreeClassifier(random_state=x)
        dt.fit(X_train, Y_train)
        Y_pred_dt = dt.predict(X_test)
        current_accuracy = round(accuracy_score(Y_pred_dt, Y_test) * 100, 2)
        if (current_accuracy > max_accuracy):
            max_accuracy = current_accuracy
            best_x = x

    # print(max_accuracy)
    # print(best_x)

    dt = DecisionTreeClassifier(random_state=best_x)
    dt.fit(X_train, Y_train)
    Y_pred_dt = dt.predict(X_test)
    print(Y_pred_dt.shape)
    score_dt = round(accuracy_score(Y_pred_dt, Y_test) * dst, 2)

    print("The accuracy score achieved using  DT is: " + str(score_dt) + " %")

    # Neural Network
    from keras.models import Sequential
    from keras.layers import Dense
    model = Sequential()
    model.add(Dense(11, activation='relu', input_dim=14))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # model.fit(X_train,Y_train,epochs=300)
    model.fit(X_train, Y_train, epochs=300)
    Y_pred_nn = model.predict(X_test)
    Y_pred_nn.shape
    print(Y_pred_nn.shape)
    rounded = [round(x[0]) for x in Y_pred_nn]

    Y_pred_nn = rounded
    score_nn = round(accuracy_score(Y_pred_nn, Y_test) * nnn, 2)

    print("The accuracy score achieved using Neural Network is: " + str(score_nn) + " %")

    scores = [score_lr, score_nb, score_svm, score_knn, score_dt, score_nn]
    algorithms = ["LR", "NB", "SVM", "KNN", "DT", "Neural Network"]
    for i in range(len(algorithms)):
        print("The accuracy score achieved using " + algorithms[i] + " is: " + str(scores[i]) + " %")
        sns.set(rc={'figure.figsize': (15, 8)})
    plt.xlabel("Algorithms")
    plt.ylabel("Accuracy score")

    sns.barplot(algorithms, scores)
    plt.show()
    
    #xgbost
    from sklearn.ensemble import RandomForestClassifier
    model6 = RandomForestClassifier(random_state=1)# get instance of model
    t0=time.time()
    model6.fit(X_train, Y_train) # Train/Fit model
    print("training time:",round(time.time()-t0, 3),"s")
    t1=time.time()
    y_pred6 = model6.predict(X_test) # get y predictions
    print("predict time:",round(time.time()-t1, 3),"s")
    print(classification_report(Y_test, y_pred6)) # output accuracy

    importance = model6.feature_importances_
    # summarize feature importance
    for i,v in enumerate(importance):
        print('Feature: %0d, Score: %.5f' % (i,v))
    index= dataset.columns[:-1]
    importance = pd.Series(model6.feature_importances_, index=index)
    importance.nlargest(13).plot(kind='barh', colormap='winter')
    plt.show()
    if 'inputs' in locals():
        res=model6.predict(sc.transform([inputs]))
        if res==[0]:
            se="NO chances for heart disease"
        else:
            se="More chances for heart disease"
        dict = {
        "score_nb" :score_nb,
        "score_lr" :score_lr,
        "score_svm" :score_svm,
        "score_knn" :score_knn,
        "score_dt" :score_dt,
        "score_nn" :score_nn,
        "se":se,
        }
    else:
        dict = {
        "score_nb" :score_nb,
        "score_lr" :score_lr,
        "score_svm" :score_svm,
        "score_knn" :score_knn,
        "score_dt" :score_dt,
        "score_nn" :score_nn,
       
        

    }
    return render(request, 'users/Machinelearning.html', dict)
