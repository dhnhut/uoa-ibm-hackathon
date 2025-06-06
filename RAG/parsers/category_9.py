import re

def to_json(text: str) -> list[dict]:
  text= text[44:]  # Remove the first three characters (e.g., "9A ")
  parsed_items = []
  current_id = None
  current_description_lines = []
  # Regex to identify lines that are item IDs (e.g., "9A", "9A001")
  # This pattern assumes IDs start with '9', followed by an uppercase letter,
  # and then optionally more uppercase letters or digits.
  id_pattern = re.compile(r"^9[A-Z][A-Z0-9]*$")

  lines = text.strip().splitlines() #.strip() on text to remove leading/trailing blank lines overall

  for line in lines:
      line = line.strip()  # Strip leading and trailing whitespace
      
      if id_pattern.match(line):
          # This line is an item ID line
          if current_id is not None:
              # Save the previous item
              parsed_items.append({
                  "id": current_id,
                  "description": "".join(current_description_lines)
              })
          
          current_id = line
          current_description_lines = []
      elif current_id is not None:
          # This line is part of the description for the current_id
          current_description_lines.append(line)

  # Add the last processed item
  if current_id is not None:
      parsed_items.append({
          "id": current_id,
          "description": "".join(current_description_lines)
      })
  return parsed_items

def to_txt(data: list[dict]) -> str:
    lines = []
    for item in data:
        # Join the description lines with a space, ensuring no leading/trailing spaces
        description = " ".join(item["description"].strip().split())
        lines.append(f"{item['id']}: {description}")
    return "\n".join(lines)