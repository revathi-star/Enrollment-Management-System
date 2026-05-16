from flask import Flask, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource,Api,fields,marshal_with,reqparse
from werkzeug import exceptions
import json

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.sqlite3'
db=SQLAlchemy()
db.init_app(app)
#app.app_context.push()
api=Api(app)

#Models

class Student(db.Model):
    __tablename__='student'
    student_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_number= db.Column(db.String, unique=True, nullable=False)
    first_name= db.Column(db.String, nullable=False)
    last_name= db.Column(db.String)
    courses= db.relationship('Course',backref='student',secondary='enrollment', cascade='all,delete')

class Course(db.Model):
    __tablename__='course'
    course_id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name= db.Column(db.String, nullable=False)
    course_code= db.Column(db.String, unique=True, nullable=False)
    course_description= db.Column(db.String)

class Enrollment(db.Model): #for python to understand 
    __tablename__='enrollment' #for sqlalchemy db to understand
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)

with app.app_context():
    db.create_all()

#exception handling
class NotFoundError(exceptions.HTTPException):
    def __init__(self,status_code,message=''):
        self.response=make_response(message,status_code)

class NotGivenError(exceptions.HTTPException):
    def __init__(self,status_code,error_code,error_message):
        message=f"('error_code':{error_code},'error_message':{error_message})"
        self.response=make_response(json.dumps(message),status_code)
    
#output fields
student_fields={
    'student_id':fields.Integer,
    'first_name':fields.String,
    'last_name':fields.String,
    'roll_number':fields.String
}
course_fields={
    'course_id':fields.Integer,
    'course_name':fields.String,
    'course_code':fields.String,
    'course_description':fields.String
}

#parsers
course_parse= reqparse.RequestParser()
course_parse.add_argument('course_name')
course_parse.add_argument('course_code')
course_parse.add_argument('course_description')

student_parse = reqparse.RequestParser()
student_parse.add_argument('first_name')
student_parse.add_argument('last_name')
student_parse.add_argument('roll_number')

enrollment_parse= reqparse.RequestParser()
enrollment_parse.add_argument('course_id')

#APIs
class CourseAPI(Resource):
    @marshal_with(course_fields)
    def get(self,course_id):
        course=Course.query.filter(Course.course_id==course_id).first()
        if course:
            return course
        else:
            raise NotFoundError(status_code=404,message='This course does not exists')
    
    @marshal_with(course_fields)
    def post(self):
        args=course_parse.parse_args()
        course_name=args.get('course_name',None)
        course_code=args.get('course_code',None)
        course_description=args.get('course_description',None)
        if course_name is None:
            raise NotGivenError(status_code=400,error_code='COURSE001',error_message='Course name is required')      
        elif course_code is None:
            raise NotGivenError(status_code=400,error_code='COURSE200',error_message='Course code is required')
        course=Course.query.filter(Course.course_code==course_code).first()
        if course is None:
            course=Course(course_name=course_name,course_code=course_code,course_description=course_description)
            db.session.add(course)
            db.session.commit()
            return course,201
        else:
            raise NotFoundError(status_code=409,message='This course already exists')
        
    @marshal_with(course_fields)
    def put(self,course_id):
        course=Course.query.filter(Course.course_id==course_id).first()
        if course is None:
            raise NotFoundError(status_code=404,message='Such a course does not exists.')
        args=course_parse.parse_args()
        course_name=args.get('course_name',None)
        course_code=args.get('course_code',None)
        course_description=args.get('course_description',None)
        if course_name is None:
            raise NotGivenError(status_code=400,error_code='COURSE001',error_message='Course Name is required. It was received as null')
        elif course_code is None:
            raise NotGivenError(status_code=400,error_code='COURSE002',error_message='Course Code is required')
        else:
            course.course_name=course_name
            course.course_code=course_code
            course.course_description=course_description
            db.session.add(course)
            db.session.commit()
            return course
    
    @marshal_with(course_fields)
    def delete(self,course_id):
        course=Course.query.filter(Course.course_id==course_id).scalar()
        if course is None:
            raise NotFoundError(status_code=404,message='This course is not found')
        db.session.delete(course)
        db.session.commit()
        return 200
    
class StudentAPI(Resource):
    @marshal_with(student_fields)
    def get(self,student_id):
        student=Student.query.filter(Student.student_id==student_id).first()
        if student:
            return student,200
        else:
            raise NotFoundError(status_code=404,message='Such a student does not exist')
        
    @marshal_with(student_fields)
    def post(self):
        args=student_parse.parse_args()
        first_name=args.get('first_name',None)
        last_name=args.get('last_name',None)
        roll_number=args.get('roll_number',None)
        if roll_number is None:
            raise NotGivenError(status_code=400,error_code='STUDENT001',error_message='Roll NUmber is required')
        elif first_name is None:
            raise NotGivenError(status_code=400,error_code='STUDENT002',error_message='First Name is required')
        student=Student.query.filter(Student.roll_number==roll_number).first()
        if student is None:
            student=Student(first_name=first_name,last_name=last_name,roll_number=roll_number)
            db.session.add(student)
            db.session.commit()
            return student,200
        raise NotFoundError(status_code=400,message='Student already exist')
    
    @marshal_with(student_fields)
    def put(self,student_id):
        student=Student.query.filter(Student.student_id==student_id).first()
        if student is None:
            raise NotFoundError(status_code=404,message='Student does not exist')
        args=student_parse.parse_args()
        first_name=args.get('first_name',None)
        last_name=args.get('last_name',None)
        roll_number=args.get('roll_number',None)
        if roll_number is None:
            raise NotGivenError(status_code=400,error_code='STUDENT001',error_message='Roll_Number is required')
        elif first_name is None:
            raise NotGivenError(status_code=400,error_code='STUDENT002',error_message='First Name is required')
        student.first_name=first_name
        student.last_name=last_name
        student.roll_number=roll_number
        db.session.add(student)
        db.session.commit()
        return student,200
    
    @marshal_with(student_fields)
    def delete(self,student_id):
        student=Student.query.filter(Student.student_id==student_id).scalar()
        if student is None:
            raise NotFoundError(status_code=404,message='Student Not Found')
        db.session.delete(student)
        db.session.commit()
        return 200
    
class EnrollmentAPI(Resource):

    def get(self,student_id):
        student=Student.query.filter(Student.student_id==student_id).first()
        if student is None:
            raise NotGivenError(status_code=400,error_code='ENROLLMENT002',error_message='Student_id does not exist')
        enrollments=Enrollment.query.filter(Enrollment.student_id==student_id).all()
        if enrollments:
            enrolls=[]
            for enrollment in enrollments:
                enrolls.append({'enrollment_id':enrollment.enrollment_id,'student_id':enrollment.student_id,'course_id':enrollment.course_id})
            return enrolls
        raise NotFoundError(status_code=404,message='No enrollments available')
    
    def post(self,student_id):
        student=Student.query.filter(Student.student_id==student_id).first()
        if student:
            args=enrollment_parse.parse_args()
            course_id=args.get('course_id',None)
            course=Course.query.filter(Course.course_id==course_id).first()
            if course:
                enroll=Enrollment(student_id=student_id,course_id=course_id)
                db.session.add(enroll)
                db.session.commit()
            else:
                raise NotGivenError(status_code=400,error_code='ENROLLMENT001',error_message='Course does not exist')
            return [{'enrollment_id':enroll.enrollment_id,'student_id':enroll.student_id,'course_id':enroll.course_id}]
        else:
            raise NotFoundError(status_code=404,message='Student not found')

    def delete(self,student_id,course_id):
        course=Course.query.filter(Course.course_id==course_id).first()
        if course is None:
            return NotGivenError(status_code=400,error_code='ENROLLMENT001',error_message='Course does not exist')
        student=Student.query.filter(Student.student_id==student_id).first()
        if student is None:
            raise NotGivenError(status_code=400,error_code='ENROLLMENT002',error_message='Student does not exist')
        enrollments=Enrollment.query.filter(Enrollment.student_id==student_id).all()
        if enrollments is None:
            raise NotFoundError(status_code=404,message='No enrollments exist of this combination of student and course')
        else:
            for enroll in enrollments:
                if enroll.course_id==course_id:
                    db.session.delete(enroll)
            db.session.commit()
            return '',200

# adding_resources
api.add_resource(CourseAPI,'/api/course/<int:course_id>','/api/course')
api.add_resource(StudentAPI,'/api/student/<int:student_id>','/api/student')
api.add_resource(EnrollmentAPI,'/api/student/<int:student_id>/course','/api/student/<int:student_id>/course/<int:course_id>')

if __name__=='__main__':
    app.run(debug=True,port=5000)