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
    "inscriptions",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id")),
    Column("course_id", Integer, ForeignKey("courses.id")),
)


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    # tenemos que unir teachers a courses
    # paso 2.2
    courses = relationship("Course", back_populates="teacher")


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




## Draw from SQLAlchemy base
render_er(Base, "diagram.png")
