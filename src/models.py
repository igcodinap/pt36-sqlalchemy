import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()
# Muchos a Muchos
# Paso 1 ---> Crear tabla intermedia
inscription_table = Table(
    "inscriptions", # __tablename__
    Base.metadata, # metadata
    Column("student_id", Integer, ForeignKey("students.id")), # student_id = Column(Integer, ForeignKey("students.id"))
    Column("course_id", Integer, ForeignKey("courses.id")), # course_id = Column(Integer, ForeignKey("courses.id"))
)


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    # tenemos que unir teachers a courses
    # paso 2.2
    courses = relationship("Course", back_populates="teacher")

    teacher = Teacher().get(id=1)
    courses = Course().get(teacher_id=1) # no es necesario
    teacher = {
        "id": 1,
        "first_name": "John",
        "last_name": "Salas",
        "courses": [
            {
                "id": 1,
                "name": "Matematicas",
                "duration_weeks": 10,
                "teacher_id": 1,
            },
            {
                "id": 5,
                "name": "Biologia",
                "duration_weeks": 10,
                "teacher_id": 1,
            },
        ]
    }

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    duration_weeks = Column(Integer)
    # hacer relacion de uno a muchos
    # paso 1
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    # paso 2.1
    teacher = relationship("Teacher", back_populates="courses")
    # paso 2.2 MtoM
    students = relationship(
        "Student",
        secondary=inscription_table,
        back_populates="courses"
    )

    course = Course().get(id=1)
    teacher = Teacher().get(id=1) # no es necesario
    course = {
        "id": 1,
        "name": "Matematicas",
        "duration_weeks": 10,
        "teacher_id": 1,
        "teacher": {
            "id": 1,
            "first_name": "John",
            "last_name": "Salas",
        },
        "students": [
            {
                "id": 1,
                "first_name": "Mario",
                "last_name": "Smith",
                "age": 15,
                "grade": "5",
            },
            {
                "id": 2,
                "first_name": "Fernanda",
                "last_name": "Rogers",
                "age": 15,
                "grade": "5",
            },
                        {
                "id": 3,
                "first_name": "Juan",
                "last_name": "Black",
                "age": 15,
                "grade": "5",
            },
            {
                "id": 4,
                "first_name": "Jose",
                "last_name": "White",
                "age": 15,
                "grade": "5",
            },
            { # course.students.append(student)
                "id": 5,
                "first_name": "Maria",
                "last_name": "Brown",
                "age": 15,
                "grade": "5",
            }
        ]

    }


# course1 = {id: 1, name: 'algebra, duration_weeks: 3, teacher_id = 5, teacher = {id: 5, first_name: 'carlos', last_name: 'robles'}}

# teacher1 = {id: 5, first_name: 'carlos', last_name: 'robles', courses = [{id: 1, name: 'algebra, duration_weeks: 3}, ....., ]}

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    grade = Column(String)
    # paso 2.1
    courses = relationship(
        "Course",
        secondary=inscription_table,
        back_populates="students"
    )

    student = Student().get(id=1)
    course = Course().get(id=3)
    course = {
        "id": 3,
        "name": "Historia",
        "duration_weeks": 10,
        "teacher_id": 2,
        "teacher": {
            "id": 2,
            "first_name": "Mike",
            "last_name": "Gonzalez",
        },
        "students": []
    }


    student = {
        "id": 1,
        "first_name": "Mario",
        "last_name": "Smith",
        "age": 15,
        "grade": "5",
        "courses": [
            {
                "id": 1,
                "name": "Matematicas",
                "duration_weeks": 10,
                "teacher_id": 1,
            },
            {
                "id": 5,
                "name": "Biologia",
                "duration_weeks": 10,
                "teacher_id": 1,
            },
        ]
    }

    ### modo 1
    course.students.append(student)
    db.session.commit()
    ########
    ### modo 2
    student.courses.append(course)
    db.session.commit()







## Draw from SQLAlchemy base
render_er(Base, "diagram.png")
