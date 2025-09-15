from fastapi import FastAPI,HTTPException,Path
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

