import random

total_students = 30
total_teams = 6

students = range(total_students)
print(students)

list_students = list(students)

random.shuffle(list_students)
print(list_students)

project_team = []
for i in range(total_teams):
    numofmember = int(total_students/total_teams)
    index = i * numofmember
    project_team.append(list_students[index:index+numofmember])
# index:~-> index부터 index+numofmember- 1 까지

for i in project_team:
    # 리스트타입의 리스트, i는 0부터 4
    print(i)
