import pandas as pd
import numpy as np
import os

'''
We'll import the data from each user seperately, so we can do a train-test split before shuffling.
This way the model is tested on periods of time not yet seen.

features: list of features to be included in X_train and X_test
user_paths: list of filepaths to user data
split_prop: proportion of data to be included in training data
shuffle_train: boolean value on whether to shuffle the training data
'''
def custom_train_test_split(features, user_paths, split_prop, label='SLEEP', shuffle_train=True, dropna=False):
    
    train_dfs = []
    test_dfs = []
    for path in user_paths:
        # read csv file to df
        df = pd.read_csv(path, index_col=0, parse_dates=['DATE'])
        if dropna: df.dropna(inplace=True)

        # split data to train and test dfs
        split = int(df.shape[0] * split_prop)
        train_dfs.append(df[:split])
        test_dfs.append(df[split:])

    # concatenate all train dfs into X an y ndarrays
    X_train = np.concatenate(tuple([df[features].to_numpy() for df in train_dfs]))
    y_train = np.concatenate(tuple([df[label].to_numpy() for df in train_dfs]))

    # shuffle X_train and y_train keeping features and labels aligned
    if shuffle_train:
        shuffle = np.array(list(range(X_train.shape[0])))
        np.random.shuffle(shuffle)
        X_train = X_train[shuffle]
        y_train = y_train[shuffle]

    X_test = np.concatenate(tuple([df[features].to_numpy() for df in test_dfs]))
    y_test = np.concatenate(tuple([df[label].to_numpy() for df in test_dfs]))



    return X_train, y_train, X_test, y_test

def get_user_predictions(model, features, data_path, save_dir_path, label):
    fps = os.listdir(data_path)
    fps.remove('combined')
    fps.remove('validation')

    for f in fps:
        df = pd.read_csv(data_path + f, index_col=0)
        df.dropna(inplace=True)
        X = df[features].to_numpy()
        y = df[label].to_numpy()

        preds = model.predict(X)

        df['PRED'] = preds

        df.to_csv(save_dir_path + f[4:-13] + '_preds.csv')


def combine_user_csvs(clean_path):
    dfs = []
    for i in os.listdir(clean_path):
        dfs.append(pd.read_csv(clean_path + '/' + i)[['USER', 'DATE', 'SLEEP', 'HEART', 'STEP']])
    df_all = pd.concat(dfs, axis=0)
    df_all.to_csv(clean_path + '/all_clean.csv')

def main():
    combine_user_csvs('Data Analysis/Dataset/clean')

if __name__ == '__main__':
    main()