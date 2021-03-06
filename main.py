from cart import DecisionTreeCART
from sklearn.metrics import (
    confusion_matrix,
    f1_score,
)
import numpy as np
import pandas as pd


if __name__ == "__main__":
    borrower_df = pd.read_csv('data/Borrower.csv')
    loan_df = pd.read_csv('data/Loan.csv')

    loan_feature = loan_df[['loanId', 'memberId', 'isJointApplication',
                            'loanAmount', 'term', 'interestRate',
                            'monthlyPayment', 'grade', 'loanStatus']]
    loan_feature.set_index('loanId')

    borrower_feature = borrower_df[['memberId', 'yearsEmployment',
                                    'homeOwnership', 'annualIncome',
                                    'dtiRatio', 'lengthCreditHistory',
                                    'numTotalCreditLines',
                                    'numOpenCreditLines',
                                    'numOpenCreditLines1Year',
                                    'revolvingBalance',
                                    'revolvingUtilizationRate',
                                    'numDerogatoryRec',
                                    'numDelinquency2Years',
                                    'numChargeoff1year',
                                    'numInquiries6Mon']]
    borrower_feature.set_index('memberId')

    merged_df = pd.merge(borrower_feature, loan_feature, on='memberId')
    merged_df.sort_values(['memberId', 'loanId'], ascending=True)
    merged_df = merged_df.set_index(['loanId', 'memberId'])

    mode_jointapp = merged_df.isJointApplication.mode()[0]
    mean_loan = round(merged_df.loanAmount.mean())
    mode_term = merged_df.term.mode()[0]
    mean_numopen = round(merged_df.numOpenCreditLines.mean())

    merged_df[["isJointApplication"]] = merged_df[[
        "isJointApplication"]].fillna(value=mode_jointapp)
    merged_df[["loanAmount"]] = merged_df[[
        "loanAmount"]].fillna(value=mean_loan)
    merged_df[["term"]] = merged_df[["term"]].fillna(value=mode_term)
    merged_df[["numOpenCreditLines"]] = merged_df[[
        "numOpenCreditLines"]].fillna(value=mean_numopen)

    replace_dict = {
        'yearsEmployment': {
            '< 1 year': 0.5,
            '1 year': 1,
            '2-5 years': 3,
            '6-9 years': 8,
            '10+ years': 12,
        },
        'homeOwnership': {
            'rent': 0,
            'mortgage': 1,
            'own': 2,
        },
        'loanStatus': {
            'Default': 0,
            'Current': 1,
        },
        'term': {
            '60 months': 60,
            '48 months': 48,
            '36 months': 36,
        }
    }

    cleaned_df = merged_df.replace(replace_dict)

    class_yes = cleaned_df[cleaned_df['loanStatus'] == 1]
    class_no = cleaned_df[cleaned_df['loanStatus'] == 0]

    n = round(len(class_no) * 1.5)
    balanced_df = class_no.append(class_yes.sample(n))
    balanced_df.to_csv('data/loan_cleaned.csv')

    dataset_np = cleaned_df.sample(1110).values
    train_size = round(0.9 * len(dataset_np))
    np.random.shuffle(dataset_np)
    train_np = np.array(dataset_np[:train_size,:])
    test_np = np.array(dataset_np[train_size:,:])

    X_train = train_np[:, :-1]
    y_train = train_np[:, len(train_np[0]) - 1]

    X_test = test_np[:, :-1]
    y_test = test_np[:, len(train_np[0]) - 1]

    clf = DecisionTreeCART()
    clf.fit(X_train, y_train)

    predicted = clf.predict(X_test)

    pred_true = 0
    tn = 0
    tp = 0
    fn = 0
    fp = 0
    for i in range(len(predicted)):
        if predicted[i] == y_test[i]:
            pred_true += 1
            if y_test[i] == 0:
                tn += 1
            else:
                tp += 1
        else:
            if y_test[i] == 1:
                fn += 1
            else:
                fp += 1
    
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 * (precision * recall) / (precision + recall)

    print('Predicted True = ' + str(pred_true) + ' out of ' + str(len(y_test)))
    print('Precision      = ', precision)
    print('Recall         = ', recall)
    print('True Positive  = ', tp)
    print('True Negative  = ', tn)
    print('False Positive = ', fp)
    print('False Negative = ', fn)
    print('F1 Score       = ', f1)
