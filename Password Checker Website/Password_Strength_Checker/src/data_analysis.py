import pandas as pd
import matplotlib.pyplot as plt
import os

# Set static directory for saving images
static_dir = "static"
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

# Load datasets and deduplicate
df_10_million = pd.read_csv(
    "data/10-million-password-list-top-1000000.txt", header=None, names=["password"]
)
df_500_worst = pd.read_csv(
    "data/500-worst-passwords.txt", header=None, names=["password"]
)
df_common_corporate = pd.read_csv(
    "data/common_corporate_passwords.lst", header=None, names=["password"]
)
df_probable = pd.read_csv(
    "data/probable-v2-top12000.txt", header=None, names=["password"]
)
all_passwords = pd.concat(
    [df_10_million, df_500_worst, df_common_corporate, df_probable]
).drop_duplicates()
all_passwords["password"] = all_passwords["password"].astype(str).str.strip()

# Feature engineering
all_passwords["length"] = all_passwords["password"].apply(len)
all_passwords["has_number"] = all_passwords["password"].apply(
    lambda x: any(char.isdigit() for char in x)
)
all_passwords["has_uppercase"] = all_passwords["password"].apply(
    lambda x: any(char.isupper() for char in x)
)
all_passwords["has_lowercase"] = all_passwords["password"].apply(
    lambda x: any(char.islower() for char in x)
)
all_passwords["has_special"] = all_passwords["password"].apply(
    lambda x: any(not char.isalnum() for char in x)
)


# Strength categorization
def categorize_strength(row):
    if (
        row["length"] >= 12
        and row["has_number"]
        and row["has_uppercase"]
        and row["has_lowercase"]
        and row["has_special"]
    ):
        return "strong"
    elif (
        row["length"] >= 8
        and row["has_number"]
        and (row["has_uppercase"] or row["has_special"])
    ):
        return "moderate"
    else:
        return "weak"


all_passwords["strength"] = all_passwords.apply(categorize_strength, axis=1)
strength_counts = all_passwords["strength"].value_counts()

# Save strength distribution plot
strength_counts.plot(kind="bar", color=["#FF4B5C", "#FFA500", "#28A745"])
plt.title("Password Strength Distribution")
plt.xlabel("Strength Category")
plt.ylabel("Number of Passwords")
plt.savefig(os.path.join(static_dir, "password_strength_distribution.png"))
plt.show()

# Save length distribution plot
all_passwords["length"].plot(kind="hist", bins=20, color="#4b8cff", edgecolor="black")
plt.title("Password Length Distribution")
plt.xlabel("Password Length")
plt.ylabel("Frequency")
plt.savefig(os.path.join(static_dir, "password_length_distribution.png"))
plt.show()
