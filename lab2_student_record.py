student={
  "id":"2025-001",
  "name":"Juan Dela Cruz",
  "grades":[88,90,85]
}

average=sum(student["grades"])/len(student["grades"])


# Show current student ID, updated grades & average
print("ID:", student["id"])
print("Student Name:", student["name"])
print("Updated Grades:", student["grades"])
print("Average:", average)

# Blank prints
print()

# Add Grade
ask_id=input("Enter student ID to update: ")

if ask_id==student["id"]:
    updated_grade=int(input("Enter new grade for student: "))
    student["grades"].append("updated_grade")
    print(grades)
