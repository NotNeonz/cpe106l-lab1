student={
  "id":"2025-001",
  "name":"Juan Dela Cruz",
  "grades":[88,90,85]
}

average=sum(student["grades"])/len(student["grades"])


# Show current student ID, updated grades & average
print("ID:", student["id"])
print("Student Name:", student["name"])
print("Grades:", student["grades"])
print("Average:", average)

# Blank prints
print()

# Choice for user to (1)add grade, (2)update student info, or (3)terminate program
print("(1) Add student grade")
print("(2) Update student information")
print("(Any Number) Terminate program")

choice=input("Select option from 1-2 or any number: ")

# Add grade, and new average
if choice == "1":
    print()
    ask_id=input("Enter student ID to update: ")
    if ask_id==student["id"]:
        updated_grade=int(input("Enter new grade for student: "))
        student["grades"].append(updated_grade)
        print()
        print("Updated grades:",student["grades"])
        average=sum(student["grades"])/len(student["grades"])
        print("Updated average:",average)
    
    else:
        print()
        print("No student was found with the input ID")

else:
    print()
    print("Program Terminated... Goodbye! - Ignacio, Juan Carlos Miguel")
