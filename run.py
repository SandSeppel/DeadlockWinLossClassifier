import configparser as cp #Maybe this short form is a bit controverse maybe change :I
import ast
import torch 

def is_array(string : str):
    try:
        return isinstance(ast.literal_eval(string), list)
    except ValueError:
        return False


conf = cp.ConfigParser()
conf.read("config.cfg")

model_path = (
    conf.get("MODEL", "model_folder_path") + 
    conf.get("MODEL", "model_file")
)

print(f"Loading model: {model_path}...")

model = torch.load(model_path, weights_only=False)
model.eval()

print(model)

arr = []

while True:
    arr = input("Enter an Array (with brackets) containing the 12 hero IDs in order (amber hand first -> saphire flame, left to right):\n")

    if not is_array(arr):
        print("Your input is not a valid Array, please try again.\n")
    else:
        arr = ast.literal_eval(arr)
        if not len(arr) == 12:
            print(f"Your Array is not 12 entries long. Your Array length: {len(arr)}")
        else:
            break

preds = model(torch.IntTensor(arr).unsqueeze(0))

print(f"Probability predictions: {torch.sigmoid(preds.squeeze(0))}")
print("These are the win probabilties for each lane, 1 = 100%, 0 = 0%")

input()