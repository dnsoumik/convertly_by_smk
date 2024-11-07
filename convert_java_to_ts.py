import os
import re

def java_type_to_typescript(java_type):
    """Map Java types to TypeScript types."""
    type_mappings = {
        "int": "number",
        "float": "number",
        "double": "number",
        "long": "number",
        "short": "number",
        "byte": "number",
        "boolean": "boolean",
        "char": "string",
        "String": "string",
        "List": "Array",  # assuming generic types like List<String> are used
        "Map": "Record",  # assuming Map<K, V> will map to Record<K, V>
    }
    return type_mappings.get(java_type, java_type)  # Default to the same type if not found

def convert_java_file_to_ts(java_file_path, ts_file_path):
    """Convert a single Java POJO file to a TypeScript class without underscores and without getters and setters."""
    with open(java_file_path, 'r') as java_file:
        java_content = java_file.read()
    
    # Extract the class name
    class_name_match = re.search(r'class\s+(\w+)', java_content)
    if not class_name_match:
        print(f"No class definition found in {java_file_path}. Skipping file.")
        return
    class_name = class_name_match.group(1)

    # Extract properties (assuming they are defined as private with basic types)
    properties = re.findall(r'private\s+(\w+)\s+(\w+);', java_content)

    # Create the TypeScript class content without getters, setters, or underscore-prefixed fields
    ts_content = f"export class {class_name} {{\n"
    
    # Property declarations with the same variable names
    for java_type, prop_name in properties:
        ts_type = java_type_to_typescript(java_type)
        ts_content += f"  private {prop_name}: {ts_type};\n"
    
    ts_content += "}\n"

    # Save to TypeScript file
    with open(ts_file_path, 'w') as ts_file:
        ts_file.write(ts_content)
    
    print(f"Converted {java_file_path} to {ts_file_path}")

def convert_all_java_to_ts(entity_dir, models_dir):
    """Convert all Java POJO files in the entity_dir to TypeScript classes in models_dir."""
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)  # Create the models directory if it doesn't exist

    for filename in os.listdir(entity_dir):
        if filename.endswith(".java"):
            java_file_path = os.path.join(entity_dir, filename)
            ts_file_name = filename.replace(".java", ".ts")
            ts_file_path = os.path.join(models_dir, ts_file_name)
            convert_java_file_to_ts(java_file_path, ts_file_path)

# Define directories
entity_dir = './entity'  # Directory containing Java files
models_dir = './models'  # Directory to save TypeScript files

# Convert all Java files in the entity directory to TypeScript files in the models directory
convert_all_java_to_ts(entity_dir, models_dir)
