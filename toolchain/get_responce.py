import ollama

try:
    with open(".modelfiles/model", "r") as f:
        modelfile_content = f.read()

    ollama.create(model="llama2", modelfile=modelfile_content) #Use pull, not create
    print("Custom model added.")

except Exception as e:
    print(f"Error adding custom model: {e}")
