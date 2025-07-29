# Program to check grade based on marks

def check_grade(marks:int)->str:
    if marks >= 90:
        return "Grade: A"
    elif marks >= 75:
        return "Grade: B"
    elif marks >= 60:
        return "Grade: C"
    elif marks >= 40:
        return "Grade: D"
    else:
        return "Grade: F (Fail)"

student_marks = int(input("Enter student's marks: "))
print(check_grade(student_marks))