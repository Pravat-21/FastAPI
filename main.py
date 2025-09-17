from fastapi import FastAPI,HTTPException,Path,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field,computed_field
from typing import Dict,Literal,List,Optional,Annotated
import json

app=FastAPI()

class PatientSchema(BaseModel):
    id:Annotated[str,Field(...,description="Give the new patient ID")]
    name:Annotated[str,Field(...,description="Give the patient name")]
    city:Annotated[str,Field(...,description="Give the patient city")]
    age:Annotated[int,Field(...,gt=0,lt=100,description="Give the patient age")]
    gender:Annotated[Literal['Male','Female','Others'],Field(...,description="Give the patient gender")]
    height:Annotated[float,Field(...,gt=0,description="Give the patient hieght in meters")]
    weight:Annotated[float,Field(...,gt=0,description="Give the patient weight in Kg")]

    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi>=18.5 and self.bmi < 30:
            return 'Normal'
        elif self.bmi >= 30:
            return 'overweight'

class UpdateSchema(BaseModel):
    id:Annotated[Optional[str],Field(default=None,description="Give the new patient ID")]
    name:Annotated[Optional[str],Field(default=None,description="Give the patient name")]
    city:Annotated[Optional[str],Field(default=None,description="Give the patient city")]
    age:Annotated[Optional[int],Field(default=None,gt=0,lt=100,description="Give the patient age")]
    gender:Annotated[Optional[Literal['Male','Female','Others']],Field(default=None,description="Give the patient gender")]
    height:Annotated[Optional[float],Field(default=None,gt=0,description="Give the patient hieght in meters")]
    weight:Annotated[Optional[float],Field(default=None,gt=0,description="Give the patient weight in Kg")]

#---------------------------------UTILITY FUNCTION----------------------------------------------------------
def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)

#---------------------------------Routers------------------------------------------------------------------
@app.get("/")
def intro():
    return {'message':"Hello, How are you. Wanna try our API?"}

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


@app.post("/create")
def create_patient(patient:PatientSchema):

    data=load_data()
    if patient.id  in data:
        raise HTTPException(status_code=404, detail="Patient already exists")
    data[patient.id]=patient.model_dump(exclude=['id'])
    save_data(data)

    return JSONResponse(status_code=201,content={'message':'Patient data create successfully'})

@app.put("/edit{patient_id}")
def update_patient_details(patient_id:str,update_details:UpdateSchema):

    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=400,detail="Patient does not exits")
    
    update_schema=update_details.model_dump(exclude_unset=True)
    temp_data=data[patient_id]

    for key,value in update_schema.items():
        temp_data[key]=value
    temp_data['id']=patient_id

    pydantic_obj=PatientSchema(**temp_data)
    final_data=pydantic_obj.model_dump(exclude=['id'])
    data[patient_id]=final_data

    save_data(data)

    return JSONResponse(status_code=201,content={'message':'Patient data successfully updated.'})

@app.delete("/{patient_id}")
def delete_data(patient_id):

    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient ID doesn't exist")
    
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=201,content={'message':'Patient details successfully deleted'})







    

