from typing import Tuple,Dict,DefaultDict,List
from collections import defaultdict
from prettytable import PrettyTable
from HW08_Amisha_Patel import file_reader
import sys
import os
# from statistics import mean
class Students:
    """This class reprentens information about a single student with all of the relevant information including"""
    def __init__(self, cwid: str, name: str, major: str, required:List, elective:List) -> None:
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._courses: Dict[str, str] = dict() 
        self.stud_course: List = []
        self.stud_grades: List = []
        self.pass_gpa: Dict = {'A': 4.0, 'A-': 3.75, 'B+': 3.25, 'B': 3.0, 'B-': 2.75, 'C+': 2.25, 'C': 2.0, 'D+': 0, 'D': 0, 'D-': 0, 'F': 0}
        self.required: List[str] = required
        self.elective: List[str] = elective
    def store_course_grade(self, course: str, grade: str) -> None:
        """This function reprentese student took course and earned grades"""
        if grade in self.pass_gpa:
            self._courses[course] = grade
            self.stud_course.append(course)
            self.stud_grades.append(self.pass_gpa[grade])
    def info(self):
        gpa: float = 0
        if len(self.stud_grades) > 0:
            gpa = round(sum(self.stud_grades)/len(self.stud_grades), 2)
        else:
            gpa = 0.0
        self.required = set(self.required) - set(self._courses)
        if set(self._courses).intersection(set(self.elective)):
            self.elective = []
        return[self._cwid, self._name, sorted(self.stud_course), sorted(self.required), sorted(self.elective), gpa]
class Instructors:
    """This class reperents information for Instructor with including:cwid,name,department and also courses and the number of students in each course"""
    def __init__(self, cwid: str, name: str, dept: str) -> None:
        self.cwid: str = cwid
        self.name: str = name
        self.dept: str = dept
        self.courses: DefaultDict[str, int] = defaultdict(int) 
        self.stud_course: dict = {}
    def store_course_student(self, course: str):
        self.courses[course] += 1
class Majors:
    """ This class reperents information for a Major with including:major,flag for required and elective courses"""
    def __init__(self, major: str) -> None:
        self._major: str = major
        self._req_courses: List = []
        self._elec_courses: List = []
        self._courses: Dict[str, Dict] = dict()
    def add_course(self, major: str, flag: str, course: str) -> None:
        if flag == 'R':
            self._req_courses.append(course)
            self._courses[flag] = self._req_courses
        if flag == 'E':
            self._elec_courses.append(course)
            self._courses[flag] = self._elec_courses
    def req_course(self):
        return list(self._req_courses)
    def elec_course(self): 
        return list(self._elec_courses)
    def info(self):
        return[self._major, Majors.req_course(self), Majors.elec_course(self)]
class Repository:
    """This class reprents all students, instructors for a print pretty tables"""
    def __init__(self, path: str) -> None:
        self._path: str = path
        self._students: Dict[str, Students] = dict()
        self._instructors: Dict[str, Instructors] = dict()
        self._majors: Dict[str, Majors] = dict()
        self.major_info(self._path)
        self.instructors_info(self._path)
        self.students_info(self._path)
        self.grades_info(self._path)
        self.student_pretty_table()
        self.instructor_pretty_table()
        self.major_pretty_table()
    def major_info(self, path: str) -> None:
        """This function reperents each line from file majors.txt and create instance of class Major"""
        try:
            for major, flag, course in file_reader(os.path.join(self._path, 'majors.txt'), 3, "\t", True):
                if major not in self._majors.keys():
                    self._majors[major] = Majors(major)
                self._majors[major].add_course(major, flag, course)
        except (FileNotFoundError, ValueError) as e:
            print(e)
    def students_info(self, path: str) -> None:
        """This function reperents each line from students.txt and create instance of class student"""
        try:
            for cwid, name, major in file_reader(os.path.join(self._path, 'students.txt'), 3, ";", True):
                if major in self._majors[major]._major:
                    required = self._majors[major].req_course()
                    elective = self._majors[major].elec_course()
                    self._students[cwid] = Students(cwid, name, major, required, elective)
        except (FileNotFoundError, ValueError) as e:
            print(e)
    def instructors_info(self, path: str) -> None:
        """This function reperents each line from file instructors.txt and create instance of class instructor"""
        try:
            for cwid, name, department in file_reader(os.path.join(self._path, 'instructors.txt'), 3, "|", True):
                self._instructors[cwid] = Instructors(cwid, name, department)
        except (FileNotFoundError, ValueError) as e:
            print(e)
    def grades_info(self, path: str) -> None:
        """ This function reperents student_cwid, course, grade, instructor"""
        try:
            for student_cwid, course, grades, instructor_cwid in file_reader(os.path.join(self._path, 'grades.txt'), 4, "|", True):
                if student_cwid in self._students.keys():
                    stu: Students = self._students[student_cwid]
                    stu.store_course_grade(course, grades)
                else:
                    print(f"The Student with CWID : {student_cwid} is unknown.")
                if instructor_cwid in self._instructors.keys():
                    inst: Instructors = self._instructors[instructor_cwid]
                    inst.store_course_student(course)
                else:
                    print(f"The Instructor with CWID : {instructor_cwid} is unknown.")
        except (FileNotFoundError, ValueError) as e:
            if FileNotFoundError:
                print(e)
    def student_pretty_table(self) -> None:
        """This function reprents print pretty table for student's information"""
        prettyTab = PrettyTable(field_names= ['CWID', 'Name', 'Completed Courses', 'Remaining Reuired', 'Remaining Elective', 'GPA'])
        for stu in self._students.values():
            prettyTab.add_row(stu.info())
        print("Student Summary Information Table")
        print(prettyTab, "\n")
    def instructor_pretty_table(self) -> None:
        """This function reperents print pretty table for instructor data"""
        lst1: List = []
        prettyTab = PrettyTable(field_names= ['CWID', 'Name', 'Dept', 'Courses', 'Number of Students'])
        for inst in self._instructors.values():
            for k, v in inst.courses.items():
                prettyTab.add_row([inst.cwid, inst.name, inst.dept, k, v])
                lst1.append([inst.cwid, inst.name, inst.dept, k, v])
        print("Instructor Summary Information Table")
        print(prettyTab)
        return lst1
    def major_pretty_table(self) -> None:
        """Print pretty table for instructor data"""
        prettyTab = PrettyTable(field_names=['Major', 'Required Courses', 'Elective Courses'])
        for inst in self._majors.values():
            prettyTab.add_row(inst.info())
        print("Majors Summary Information Table")
        print(prettyTab)
        return prettyTab
def main() -> None:  
    Stevens: Repository = Repository("R:/Steven Institute/SSW -810-B/HW10")
if __name__ == '__main__':
    main()