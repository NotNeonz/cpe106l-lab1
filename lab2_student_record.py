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
print()

# Change Grade
ask_id=input("Enter student ID to update: ")
