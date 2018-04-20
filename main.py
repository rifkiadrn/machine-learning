from cart import DecisionTreeCART
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
    cleaned_df.to_csv('data/loan_cleaned.csv')
    cleaned_df.head()

    train_df = cleaned_df.sample(1000)
    train_np = np.array(train_df.values)
    test_np = np.array(cleaned_df.sample(100).values)

    X_train = train_np[:, :-1]
    y_train = train_np[:, len(train_np[0]) - 1]

    X_test = test_np[:, :-1]
    y_test = test_np[:, len(train_np[0]) - 1]

    clf = DecisionTreeCART()
    clf.fit(X_train, y_train)

    predicted = clf.predict(X_test)

    pred_true = 0
    for i in range(len(predicted)):
        if predicted[i] == y_test[i]:
            pred_true += 1

    print(pred_true)
