import pandas as pd
data=pd.read_csv('course_data_before.csv', encoding='unicode_escape')
data.drop_duplicates(keep='first',inplace=True)
data.to_csv('courseData.csv',index=False)