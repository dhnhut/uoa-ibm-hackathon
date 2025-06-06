import re

def to_json(text: str) -> list[dict]:
  text = text[286:]
  # Regex to split the text into blocks.
  # A block starts with: “Quoted Term” [optional (sub-term)] (Categories)
  block_splitter_regex = r'(?=^“[^”]+”(?:\s*\([^)]+\))?\s*\([^)]+\))'
  blocks = re.split(block_splitter_regex, text.strip(), flags=re.MULTILINE)
  
  extracted_data = []

  # Regex to parse the first line of a block for the term, categories, and start of definition.
  first_line_regex = re.compile(
      r'^“(?P<term_part1>[^”]+)”'              # Main term part, e.g., “Bias”
      r'(?:\s*\((?P<term_part2>[^)]+)\))?\s*'   # Optional sub-term, e.g., (accelerometer)
      r'\((?P<categories_str>[^)]+)\)\s*'      # Categories, e.g., (7)
      r'(?P<def_start>.*)'                     # Rest of the line (start of definition)
  )

  for block in blocks:
      block = block.strip()
      if not block: # Skip empty blocks from split
          continue

      lines = block.splitlines()
      if not lines:
          continue

      first_line_match = first_line_regex.match(lines[0])
      if not first_line_match:
          # This block doesn't match the expected term definition start, skip.
          # print(f"Skipping block not matching first_line_regex: {lines[0][:100]}")
          continue

      # Construct the term string as per example: "“Bias” (accelerometer)"
      term_p1 = first_line_match.group('term_part1').strip()
      term_str = f'“{term_p1}”' # Start with the quoted part
      
      term_p2_val = first_line_match.group('term_part2')
      if term_p2_val: # If the optional parenthesized part exists, append it
          term_str += f" ({term_p2_val.strip()})"
      
      categories = first_line_match.group('categories_str').strip().split()
      
      definition_lines = []
      def_start_on_first_line = first_line_match.group('def_start').strip()
      if def_start_on_first_line:
          definition_lines.append(def_start_on_first_line)

      # All subsequent non-empty lines in the block are part of the definition
      for i in range(1, len(lines)):
          line_content = lines[i].strip()
          if line_content: 
              definition_lines.append(line_content)
      
      full_definition = " ".join(definition_lines).strip()
      
      # The regex ensures term_part1 and categories_str are non-empty if a match occurs.
      # No explicit check for empty term_str or categories needed here due to regex design.

      extracted_data.append({
          "term": term_str,
          "categories": categories,
          "definition": full_definition,
      })
      
  return extracted_data

def to_txt(data: list[dict]) -> str:
    lines = []
    for item in data:
        term = item['term']
        categories = " ".join(item['categories'])
        definition = item['definition']
        lines.append(f"{term}: {definition} (In Categories: {categories})")
    
    return "\n".join(lines)