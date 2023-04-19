import pandas as pd
import requests
import os

# scroll down to the bottom to implement your solution

if __name__ == '__main__':

    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable
    if ('A_office_data.xml' not in os.listdir('../Data') and
        'B_office_data.xml' not in os.listdir('../Data') and
        'hr_data.xml' not in os.listdir('../Data')):
        print('A_office_data loading.')
        url = "https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/A_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('B_office_data loading.')
        url = "https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/B_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('hr_data loading.')
        url = "https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/hr_data.xml', 'wb').write(r.content)
        print('Loaded.')

        # All data in now loaded to the Data folder.

    # write your code here

    # read data

    office_a_df = pd.read_xml('../Data/A_office_data.xml')
    office_b_df = pd.read_xml('../Data/B_office_data.xml')
    hr_df = pd.read_xml('../Data/hr_data.xml')

    # get the axes, shape and check for null values

    def explore_data(data):
        axes = data.axes
        shape = data.shape
        info = data.info

    explore_data(office_a_df)
    explore_data(office_b_df)
    explore_data(hr_df)

    # combine the datasets

    office_a_df['employee_office_id'] = 'A' + office_a_df['employee_office_id'].astype(str)
    office_b_df['employee_office_id'] = 'B' + office_b_df['employee_office_id'].astype(str)
    office_a_df.set_index('employee_office_id', inplace=True)
    office_b_df.set_index('employee_office_id', inplace=True)
    hr_df.set_index('employee_id', inplace=True)

    uni_office_df = pd.concat([office_a_df, office_b_df])

    together_df = uni_office_df.merge(hr_df, left_index=True, right_index=True, indicator=True)
    together_df.drop(columns=['_merge'], inplace=True)
    together_df.sort_index(inplace=True)

    print(together_df.sort_values('average_monthly_hours', ascending=False).head(10)['Department'].tolist())
    print(together_df.query("Department == 'IT' & salary == 'low'").number_project.sum())
    print(together_df.loc[['A4', 'B7064', 'A3033'], ['last_evaluation', 'satisfaction_level']].values.tolist())
