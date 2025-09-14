def get(word, language):
    
    line_found = []

    with open(f"lpak/{language}.lpak", "r") as file:        
        for line in file:
                parts = line.split("|", 1)              
                
                key, value = parts[0].strip(), parts[1].strip()                
              
                if key == word:
                    return str(value)                
    return None