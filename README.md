# Java to TypeScript Class Converter

This project contains a Python script to automatically convert Java Plain Old Java Object (POJO) files into TypeScript classes. The script processes Java files within a specified directory, extracts class and variable definitions, and generates corresponding TypeScript classes with optional or public properties. 

## Features

- Converts Java POJOs to TypeScript classes.
- Handles `public` and `private` classes:
  - `public` classes are converted to TypeScript.
  - `private` classes are skipped.
- Supports common Java types like `String`, `int`, `BigDecimal`, and `byte[]` with appropriate TypeScript mappings.
- Renames classes ending with `VO` to end with `Model` in TypeScript.
- Generates TypeScript files in kebab-case (e.g., `UserDataVO.java` -> `user-data.model.ts`).
- Marks `public` variables as non-optional in TypeScript and `private` variables as optional.

## Type Mappings

| Java Type       | TypeScript Type       |
| --------------- | --------------------- |
| `int`, `Integer`| `number`              |
| `BigDecimal`    | `number`              |
| `String`        | `string`              |
| `byte[]`        | `Uint8Array`          |
| `List<T>`, `Array<T>` | `Array<T>`    |

## Setup

1. Make sure you have Python installed.
2. Clone or download this project.

## Usage

1. Place your Java files in a directory named `./entity` within the project root.
2. Run the script:

    ```bash
    python convert_java_to_ts.py or convert_with_constructure_java_to_ts.py
    ```

3. Converted TypeScript files will be generated in the `./models` directory.

## Script Overview

- **`convert_all_java_to_ts.py`**: This Python script reads all `.java` files in the `./entity` directory, processes them, and outputs TypeScript files in `./models`.

### How the Script Works

1. **File Conversion**: 
   - Reads Java files in the `./entity` directory.
   - Checks each file for a `public` or `private` class.
   - Converts `public` classes to TypeScript and skips `private` classes.
2. **Class Renaming**:
   - If a class name ends with `VO`, it is converted to end with `Model` in TypeScript.
   - Converts Java files to kebab-case `.model.ts` files.
3. **Property Conversion**:
   - Extracts `public` and `private` fields, mapping Java types to TypeScript equivalents.
   - Public fields are converted to non-optional properties in TypeScript, while private fields are made optional.

## Example


java

```
public class UserDataVO {
    public String userName = null;
    private BigDecimal balance;
    public byte[] profileImage = null;
}
```
The script generates a TypeScript file user-data.model.ts:

typescript
```
export class UserDataModel {
  userName: string;
  balance?: number;
  profileImage: Uint8Array;
}
```

License
This project is open-source and available under the Apache License 2.0
