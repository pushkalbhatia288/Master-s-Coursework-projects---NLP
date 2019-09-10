data = open("data_to_train.txt", "w")
labels = open("data_labels.txt", "w")
with open("Questions.txt", "r+") as file:
    for line in file:
        line = line.split()
        line = " ".join(line[a] for a in range(1, len(line)))
        data.write(line + "\n")
        labels.write("1" + "\n")

with open("NotQuestions.txt", "r+") as file:
    for line in file:
        line = line.split()
        line = " ".join(line[a] for a in range(1, len(line)))
        data.write(line + "\n")
        labels.write("0" + "\n")
