def parser(text: str) -> list[dict]:
    text = text[179:]
    # Split the input text into lines and strip leading/trailing whitespace from each
    lines = [line.strip() for line in text.split('\n')]
    
    parsed_data = []
    index = 0
    num_lines = len(lines)

    while index < num_lines:
        current_line = lines[index]

        # Skip any other empty lines
        if not current_line:
            index += 1  # Move to the next line
            continue

        # Process acronym-meaning pairs
        # If we are here, current_line is non-empty and not part of the specific header.
        # It's considered an acronym. The next line should be its meaning.
        if index + 1 < num_lines:
            next_line = lines[index + 1]
            
            # Ensure the meaning line (next_line) is not empty.
            # If next_line is empty, it's an incomplete pair, so we skip current_line.
            if next_line: 
                parsed_data.append({
                    "acronym": current_line,
                    "meaning": next_line
                })
                index += 2  # Consumed two lines (acronym and meaning)
            else:
                # current_line is an acronym, but the next_line (supposed meaning) is empty.
                # This is an incomplete pair. We skip current_line.
                index += 1 # Move past current_line; the empty next_line will be handled in the next iteration.
        else:
            # This is the last line of the text and cannot form a pair.
            index += 1 # Move past this last line
            
    return parsed_data