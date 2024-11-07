import os
import re

def java_type_to_typescript(java_type):
    """Map Java types to TypeScript types, including handling of generics, VO-to-Model conversion, BigDecimal, and byte[]."""
    type_mappings = {
        "int": "number",
        "Integer": "number",
        "float": "number",
        "Float": "number",
        "double": "number",
        "Double": "number",
        "long": "number",
        "Long": "number",
        "short": "number",
        "Short": "number",
        "byte": "number",
        "Byte": "number",
        "boolean": "boolean",
        "Boolean": "boolean",
        "char": "string",
        "String": "string",
        "BigDecimal": "number",  # BigDecimal mapped to number
        "byte[]": "Uint8Array"  # byte[] mapped to Uint8Array for binary data
    }

    # Check for generic types like List<AnimalVO> or Array<AnimalVO>
    generic_match = re.match(r"(List|Array)<(\w+)>", java_type)
    if generic_match:
        # Get the generic element type (e.g., AnimalVO)
        element_type = generic_match.group(2)
        # If the element type ends with VO, convert it to Model
        if element_type.endswith("VO"):
            element_type = element_type[:-2] + "Model"
        # Return as Array<ModifiedType>
        ts_type = f"Array<{element_type}>"
        return ts_type

    # If the type is a standalone VO (not in a generic), convert to Model
    if java_type.endswith("VO"):
        java_type = java_type[:-2] + "Model"

    # Return the mapped type or default to the same name if not found in mappings
    return type_mappings.get(java_type, java_type)

def to_kebab_case(name):
    """Convert PascalCase or camelCase to kebab-case."""
    return re.sub(r'(?<!^)(?=[A-Z])', '-', name).lower()

def convert_java_file_to_ts(java_file_path, ts_file_path):
    """Convert a single Java POJO file to a TypeScript class with optional fields, without a constructor."""
    with open(java_file_path, 'r') as java_file:
        java_content = java_file.read()
    
    # Extract the class name and access modifier
    class_match = re.search(r'(public|private)?\s*class\s+(\w+)', java_content)
    if not class_match:
        print(f"No class definition found in {java_file_path}. Skipping file.")
        return

    # Check if the class is private and skip if it is
    class_modifier = class_match.group(1)
    class_name = class_match.group(2)
    if class_modifier == "private":
        print(f"Skipping private class {class_name} in {java_file_path}.")
        return

    # Rename class if it ends with VO (e.g., GoatVO -> GoatModel)
    if class_name.endswith("VO"):
        class_name = class_name[:-2] + "Model"

    # Extract properties (support both public and private access modifiers, and handle optional initializations)
    properties = re.findall(r'(public|private)\s+([\w\[\]<>]+)\s+(\w+)(?:\s*=\s*[^;]+)?;', java_content)

    # Create the TypeScript class content with optional fields and public modifiers
    ts_content = f"export class {class_name} {{\n"
    
    # Property declarations with access modifiers (public or optional)
    for access_modifier, java_type, prop_name in properties:
        ts_type = java_type_to_typescript(java_type)
        if access_modifier == "public":
            ts_content += f"  {prop_name}: {ts_type};\n"  # public in TypeScript
        else:
            ts_content += f"  {prop_name}?: {ts_type};\n"  # private in TypeScript (optional)

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
            # Remove VO suffix from filename if it exists, then convert to kebab-case and add .model.ts
            base_name = filename.replace(".java", "")
            if base_name.endswith("VO"):
                base_name = base_name[:-2]  # Remove "VO" suffix
            ts_file_name = to_kebab_case(base_name) + ".model.ts"
            ts_file_path = os.path.join(models_dir, ts_file_name)
            convert_java_file_to_ts(java_file_path, ts_file_path)

# Define directories
entity_dir = './entity'  # Directory containing Java files
models_dir = './models'  # Directory to save TypeScript files

# Convert all Java files in the entity directory to TypeScript files in the models directory
convert_all_java_to_ts(entity_dir, models_dir)
