from fastapi import FastAPI,HTTPException,Path,Query
import json

app=FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    return data

@app.get("/home")
def Home():
    return {"message":"Wellcome to our API website"}

@app.get("/view")
def view():
    data=load_data()
    return data

#creating path parameters
@app.get("/view/{patients_id}")
def fetch_patient_data(patients_id:str=Path(...,description="enter the patient ID",example="P001")):
    data=load_data()
    if patients_id in data:
        return data[patients_id]
    
    raise HTTPException(status_code=404,detail="value not found")

#create a query parameter
@app.get("/sort")
def sort_details(sort_by : str = Query(...,description="tell us in based on which you want to sort. "),order:str =Query(description="Tell us how you want to see the data means in asc or desc")):

    sort_params=['height','weight','bmi']
    order_params=['asc','desc']

    if sort_by not in sort_params:
        raise HTTPException(status_code=400,detail=f'Invaid entry. Value must be from {sort_params}')
    
    if order not in order_params:
        raise HTTPException(status_code=400,detail=f'Invaid entry. Value must be from {order_params}')
    
    data = load_data()

    sort_order = True if order=='desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data
    

