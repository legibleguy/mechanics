import pandas as pd
import subprocess
import json
import re

## This script is used to evaluate the time to implement for each mechanic.
## It uses a local LLM to generate estimates
## It then updates the mechanics_database_expanded.csv file with the new estimates.

def read_markdown_table(file_path):
    # Try different encodings
    encodings = ['utf-8', 'latin1', 'cp1252']
    
    for encoding in encodings:
        try:
            # Read the markdown file
            with open(file_path, 'r', encoding=encoding) as f:
                lines = f.readlines()
            
            # Find the table start (first line with |)
            table_start = 0
            for i, line in enumerate(lines):
                if '|' in line:
                    table_start = i
                    break
            
            # Extract headers from the first table line
            header_line = lines[table_start]
            headers = [col.strip() for col in header_line.split('|')[1:-1]]
            
            # Skip the separator line and start reading data
            data = []
            for line in lines[table_start + 2:]:  # Skip header and separator
                if '|' not in line:
                    continue
                row = [col.strip() for col in line.split('|')[1:-1]]
                if len(row) == len(headers):  # Only add rows that match header length
                    data.append(row)
            
            # Create DataFrame
            df = pd.DataFrame(data, columns=headers)
            return df
            
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error with {encoding} encoding: {str(e)}")
            continue
    
    raise ValueError("Could not read file with any of the attempted encodings")

def get_llm_estimate(mechanic_name, description, examples, solved_problems):
    prompt = f"""Given this game mechanic:
Name: {mechanic_name}
Description: {description}
Examples: {examples}
Solved Problems: {solved_problems}

Please provide:
1. Minimum time to implement (MUST specify either hours, days, or months)
2. Worst case scenario time to implement (MUST specify either hours, days, or months)
3. A detailed explanation of why these timeframes were chosen

Your response must be EXACTLY in this JSON format with no other text:
{{
    "min_time": "X hours/days/months",
    "max_time": "X hours/days/months",
    "explanation": "Detailed explanation"
}}

Rules for the response:
1. min_time and max_time MUST end with either "hours", "days", or "months"
2. Numbers should be integers (no decimals)
3. The explanation should be a single paragraph
4. No line breaks in the JSON
5. No markdown or special formatting"""

    # Call Ollama with the prompt
    cmd = [
        "ollama", "run", "deepseek-r1:14b",
        prompt
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        response = result.stdout.strip()
        
        # Try to find JSON in the response
        try:
            # First try direct JSON parsing
            return json.loads(response)
        except:
            # If that fails, try to extract JSON using regex
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except:
                    print(f"Failed to parse JSON from response: {response}")
            
        # If all parsing attempts fail, return error
        return {
            "min_time": "Error parsing response",
            "max_time": "Error parsing response",
            "explanation": "Failed to get valid JSON response from LLM"
        }
    except Exception as e:
        return {
            "min_time": "Error",
            "max_time": "Error",
            "explanation": f"Error running Ollama: {str(e)}"
        }

def process_all_entries():
    # Read the markdown file
    df = read_markdown_table('mechanics_database.md')
    
    # Add new columns to the DataFrame if they don't exist
    if 'Min Time' not in df.columns:
        df['Min Time'] = ''
    if 'Max Time' not in df.columns:
        df['Max Time'] = ''
    if 'Time to Implement (Explained)' not in df.columns:
        df['Time to Implement (Explained)'] = ''
    
    # Remove any rows that are just separators or empty
    df = df[df['Name'].notna() & (df['Name'] != '------') & ~df['Name'].str.startswith('--', na=False)]
    
    # Process each entry
    total_entries = len(df)
    for idx, row in df.iterrows():
        try:
            print(f"Processing entry {idx + 1}/{total_entries}: {row['Name']}")
            
            # Get LLM estimate
            estimate = get_llm_estimate(
                row['Name'],
                row['Long Description'],
                row['Examples'],
                row['Solved Problems']
            )
            
            # Check if we got a valid response
            if 'min_time' in estimate and 'max_time' in estimate and 'explanation' in estimate:
                # Update the entry
                df.at[idx, 'Min Time'] = estimate['min_time']
                df.at[idx, 'Max Time'] = estimate['max_time']
                df.at[idx, 'Time to Implement (Explained)'] = estimate['explanation']
                print(f"Saved estimates for {row['Name']}")
            else:
                print(f"Error: Invalid response format for {row['Name']}")
                print(f"Response: {estimate}")
                continue
                
            # Save progress after each successful entry
            df.to_csv('mechanics_database_expanded.csv', index=False, encoding='utf-8')
            
        except Exception as e:
            print(f"Error processing {row['Name']}: {str(e)}")
            continue

if __name__ == "__main__":
    process_all_entries() 