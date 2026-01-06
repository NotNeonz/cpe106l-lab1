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

# Add grade, and new average
ask_id=input("Enter student ID to update: ")

if ask_id==student["id"]:
    updated_grade=int(input("Enter new grade for student: "))
    student["grades"].append(updated_grade)
    print("Updated Grade:",student["grades"])
    average=sum(student["grades"])/len(student["grades"])
    print("Updated average:",average)
    
else:
    print("No student was found with the input ID")
