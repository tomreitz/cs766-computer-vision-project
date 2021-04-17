import os
import matplotlib.pyplot as plt

files = os.listdir("../../datasets/UTKFace-curated/") # -curated
print("Total files: "+str(len(files)))

gender_count = [0, 0]
ethnicity_count = [0, 0, 0, 0, 0]
age_count = [0 for col in range(120)]
for f in files:
	tmp = f.split("_")
	if len(tmp)!=4: continue
	age_count[int(tmp[0])] += 1
	gender_count[int(tmp[1])] += 1
	ethnicity_count[int(tmp[2])] += 1

print(gender_count)
print(ethnicity_count)
plt.bar(range(120), age_count)
plt.show()
