"""
Excel Multi-Table Analysis Helper
Reference implementation for the excel-analyzer subagent
"""

import pandas as pd
import numpy as np
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any
import unicodedata


def detect_tables_in_sheet(df: pd.DataFrame, sheet_name: str) -> List[Dict]:
    """
    Detect multiple tables within a single Excel sheet
    Returns list of table metadata with boundaries
    """
    tables = []
    
    # Find potential table starting points (rows with text that could be headers)
    potential_headers = []
    for idx, row in df.iterrows():
        # Check if row has mostly text values (potential headers)
        text_count = sum(1 for val in row if isinstance(val, str) and len(str(val).strip()) > 0)
        total_non_null = sum(1 for val in row if pd.notna(val))
        
        if total_non_null > 0 and text_count / total_non_null > 0.5:
            potential_headers.append(idx)
    
    # Group consecutive potential headers and find table boundaries
    if potential_headers:
        current_table_start = potential_headers[0]
        table_count = 1
        
        for i, header_row in enumerate(potential_headers):
            # Look for data after this header
            data_start = header_row + 1
            data_end = len(df)
            
            # Find where data ends (consecutive empty rows or next header)
            empty_row_count = 0
            for row_idx in range(data_start, len(df)):
                row_data = df.iloc[row_idx]
                if row_data.isna().all() or (row_data == '').all():
                    empty_row_count += 1
                    if empty_row_count >= 2:  # 2+ empty rows indicate table end
                        data_end = row_idx - empty_row_count
                        break
                else:
                    empty_row_count = 0
            
            # Find column boundaries (non-empty columns)
            table_data = df.iloc[header_row:data_end]
            non_empty_cols = []
            for col_idx, col in enumerate(table_data.columns):
                if not table_data[col].isna().all():
                    non_empty_cols.append(col_idx)
            
            if non_empty_cols and data_end > data_start:
                col_start = min(non_empty_cols)
                col_end = max(non_empty_cols)
                
                # Extract table data
                table_df = df.iloc[header_row:data_end, col_start:col_end+1]
                table_df = table_df.dropna(how='all').dropna(axis=1, how='all')
                
                if not table_df.empty and len(table_df) > 1:  # At least header + 1 data row
                    tables.append({
                        'table_id': f"table_{table_count}",
                        'sheet_name': sheet_name,
                        'location': f"{chr(65+col_start)}{header_row+1}:{chr(65+col_end)}{data_end}",
                        'headers': list(table_df.iloc[0].astype(str)),
                        'data': table_df.iloc[1:],
                        'rows': len(table_df) - 1,
                        'columns': len(table_df.columns)
                    })
                    table_count += 1
    
    return tables


def analyze_text_quality(series: pd.Series, column_name: str) -> Dict:
    """
    Analyze text data quality issues in a pandas Series
    """
    analysis = {
        'column': column_name,
        'missing_values': {
            'count': int(series.isna().sum()),
            'percentage': f"{(series.isna().sum() / len(series)) * 100:.1f}%"
        },
        'text_issues': {}
    }
    
    # Convert to string and filter non-null values
    text_data = series.dropna().astype(str)
    
    if len(text_data) == 0:
        return analysis
    
    # Check for accents and special characters
    accented_chars = []
    special_chars = set()
    
    for text in text_data:
        for char in text:
            if unicodedata.category(char).startswith('L') and char != unicodedata.normalize('NFD', char).encode('ascii', 'ignore').decode('ascii'):
                accented_chars.append(char)
            elif not char.isalnum() and not char.isspace() and char not in '.,!?':
                special_chars.add(char)
    
    if accented_chars:
        analysis['text_issues']['accents_found'] = list(set(accented_chars))
    
    if special_chars:
        analysis['text_issues']['special_chars'] = list(special_chars)
    
    # Check case consistency
    case_variations = set()
    normalized_texts = {}
    
    for text in text_data:
        normalized = text.lower().strip()
        if normalized in normalized_texts:
            case_variations.add(normalized)
            normalized_texts[normalized].append(text)
        else:
            normalized_texts[normalized] = [text]
    
    inconsistent_cases = {}
    for normalized, variations in normalized_texts.items():
        if len(set(variations)) > 1:
            inconsistent_cases[normalized] = list(set(variations))
    
    if inconsistent_cases:
        analysis['text_issues']['case_inconsistency'] = inconsistent_cases
    
    # Check for whitespace issues
    whitespace_issues = []
    for text in text_data:
        if text != text.strip():
            whitespace_issues.append('leading_trailing_spaces')
        if '  ' in text:
            whitespace_issues.append('multiple_spaces')
    
    if whitespace_issues:
        analysis['text_issues']['whitespace_issues'] = list(set(whitespace_issues))
    
    return analysis


def create_table_preview(table_data: pd.DataFrame, headers: List[str]) -> str:
    """
    Create a concise preview of table data (headers + first 2 rows)
    """
    preview_lines = []
    
    # Headers
    preview_lines.append("HEADERS: " + " | ".join(headers))
    
    # Sample rows (first 2)
    for idx, (_, row) in enumerate(table_data.head(2).iterrows()):
        row_data = " | ".join(str(val)[:50] if pd.notna(val) else "" for val in row)
        preview_lines.append(f"Row {idx+1}: {row_data}")
    
    return "\n".join(preview_lines)


def convert_tables_to_csv(tables: List[Dict], excel_file_path: Path, output_dir: Path) -> List[str]:
    """
    Convert detected tables to individual CSV files
    """
    csv_files = []
    
    for table in tables:
        # Create filename: original_name_sheet_table.csv
        base_name = excel_file_path.stem
        sheet_name = table['sheet_name'].replace(' ', '_')
        table_id = table['table_id']
        csv_filename = f"{base_name}_{sheet_name}_{table_id}.csv"
        csv_path = output_dir / csv_filename
        
        # Prepare data with headers
        table_df = table['data'].copy()
        table_df.columns = table['headers']
        
        # Save to CSV
        table_df.to_csv(csv_path, index=False, encoding='utf-8')
        csv_files.append(str(csv_path))
        
        # Update table info with CSV path
        table['csv_file'] = csv_filename
    
    return csv_files


def analyze_excel_file(excel_path: str) -> Dict[str, Any]:
    """
    Complete Excel analysis pipeline
    """
    excel_file = Path(excel_path)
    output_dir = excel_file.parent
    
    # Read Excel file and get sheet information
    excel_data = pd.read_excel(excel_path, sheet_name=None, header=None)
    
    analysis_result = {
        'file_info': {
            'excel_file': str(excel_file),
            'sheets': len(excel_data),
            'total_tables_detected': 0
        },
        'table_structure': {},
        'csv_files_created': [],
        'data_quality_per_table': {}
    }
    
    all_tables = []
    
    # Process each sheet
    for sheet_name, df in excel_data.items():
        tables = detect_tables_in_sheet(df, sheet_name)
        
        if tables:
            analysis_result['table_structure'][sheet_name] = {}
            
            for table in tables:
                table_id = table['table_id']
                
                # Create table info
                analysis_result['table_structure'][sheet_name][table_id] = {
                    'location': table['location'],
                    'headers': table['headers'],
                    'rows': table['rows'],
                    'columns': table['columns'],
                    'preview': create_table_preview(table['data'], table['headers'])
                }
                
                # Analyze data quality for each column
                quality_analysis = {}
                for col_idx, header in enumerate(table['headers']):
                    if col_idx < len(table['data'].columns):
                        col_data = table['data'].iloc[:, col_idx]
                        quality_analysis[header] = analyze_text_quality(col_data, header)
                
                analysis_result['data_quality_per_table'][f"{sheet_name}_{table_id}"] = quality_analysis
                all_tables.append(table)
    
    # Convert tables to CSV
    if all_tables:
        csv_files = convert_tables_to_csv(all_tables, excel_file, output_dir)
        analysis_result['csv_files_created'] = csv_files
        analysis_result['file_info']['total_tables_detected'] = len(all_tables)
        
        # Update table structure with CSV file paths
        for table in all_tables:
            sheet_name = table['sheet_name']
            table_id = table['table_id']
            if sheet_name in analysis_result['table_structure']:
                if table_id in analysis_result['table_structure'][sheet_name]:
                    analysis_result['table_structure'][sheet_name][table_id]['csv_file'] = table['csv_file']
    
    return analysis_result


if __name__ == "__main__":
    # Example usage
    excel_file = "sample.xlsx"  # Replace with actual Excel file path
    result = analyze_excel_file(excel_file)
    print(json.dumps(result, indent=2, ensure_ascii=False))