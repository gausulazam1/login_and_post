from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

data = []
id_counter = 1

class StudentInput(BaseModel):
    name: str
    roll_no: str
    subject: str
    address: str
    phone_no: int

class Student(StudentInput):
    id: int

@router.post("/student")
def add_student(student_input: StudentInput):
    global id_counter
    student = Student(id=id_counter, **student_input.dict())
    id_counter += 1
    data.append(student.dict())
    return {"message": "Student added successfully", "student": student}

@router.get("/students")
def get_all_students():
    return data

@router.get("/student/{student_id}")
def get_student_by_id(student_id: int):
    for student in data:
        if student["id"] == student_id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")
