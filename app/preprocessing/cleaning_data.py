import pandas as pd
from fastapi import FastAPI, HTTPException

def preprocess(request):
    request_dict = request.__dict__
    data = pd.DataFrame(request_dict, index=[0])
    df_code = pd.read_excel('./preprocessing/data/zipcode_be.xlsx')
    data['code'] = data['zip_code']
    df_code['code']=df_code['code'].astype(int)
    data['code']=data['code'].astype(int)
    data = data.merge(df_code, on='code', how='left')
    data = data.drop_duplicates(subset="full_address")
    data.drop(['full_address','name','province' ,'proprety_type'], axis=1, inplace=True)
    data['building_state'] = (data['building_state']).replace({'NEW': '1', 'TO_RENOVATE': '0', 'JUST RENOVATED': '1', 'TO REBUILD': '0'})
    data = data.convert_dtypes(infer_objects=True, \
                                convert_string=True, \
                                convert_integer=True, \
                                convert_boolean=True, \
                                convert_floating=True)

    important_data = data[['area','rooms_number','zip_code','building_state']]
    if important_data.isnull().any().any():
        raise HTTPException(status_code=409, detail=f'error, not all neccesery data are complete( area,rooms-number,zip-code or building-state)')
    else:
        
        for name in data:
            if data[name].isnull().any():
                data.loc[0,name] = 0

        
        data = data*1
    return data
