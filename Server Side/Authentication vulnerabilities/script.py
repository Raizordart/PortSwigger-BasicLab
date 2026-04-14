<<<<<<< HEAD
with open("password.txt", "r") as f:
    data = f.read().split()

with open("password_modified.txt", "w") as m:
    for i,dat in enumerate(data):
        if(i%2 == 0):
            m.write("peter\n")
        m.write(f"{dat}\n")
=======
with open("password.txt", "r") as f:
    data = f.read().split()

with open("password_modified.txt", "w") as m:
    for i,dat in enumerate(data):
        if(i%2 == 0):
            m.write("peter\n")
        m.write(f"{dat}\n")
>>>>>>> ae5bd4f (init commit)
