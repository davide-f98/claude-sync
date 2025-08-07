"""
Test script to demonstrate the Excel analyzer functionality
This simulates what the excel-analyzer subagent would do
"""

import os
import sys
sys.path.append(os.path.dirname(__file__))

from excel_analysis_helper import analyze_excel_file
import json

def test_excel_analyzer():
    """Test the Excel analyzer with a sample file"""
    
    # Available test file
    excel_file = r"C:\Users\cg14849\Desktop\merged_small_medium_companies.xlsx"
    
    print(f"🔍 Analyzing Excel file: {excel_file}")
    print("=" * 60)
    
    try:
        # Run the analysis
        result = analyze_excel_file(excel_file)
        
        # Display results in a user-friendly format
        print(f"📊 FILE ANALYSIS RESULTS")
        print(f"File: {result['file_info']['excel_file']}")
        print(f"Sheets: {result['file_info']['sheets']}")
        print(f"Tables detected: {result['file_info']['total_tables_detected']}")
        print()
        
        print("📋 TABLE STRUCTURE:")
        for sheet_name, tables in result['table_structure'].items():
            print(f"\nSheet: {sheet_name}")
            for table_id, table_info in tables.items():
                print(f"  {table_id.upper()}:")
                print(f"    Location: {table_info['location']}")
                print(f"    Size: {table_info['rows']} rows × {table_info['columns']} columns")
                print(f"    CSV file: {table_info.get('csv_file', 'Not created')}")
                print(f"    Preview:")
                for line in table_info['preview'].split('\n'):
                    print(f"      {line}")
                print()
        
        print("🔍 DATA QUALITY ISSUES:")
        for table_name, quality_data in result['data_quality_per_table'].items():
            print(f"\n{table_name.upper()}:")
            for column, analysis in quality_data.items():
                missing = analysis['missing_values']
                print(f"  {column}:")
                print(f"    Missing values: {missing['count']} ({missing['percentage']})")
                
                if 'text_issues' in analysis and analysis['text_issues']:
                    issues = analysis['text_issues']
                    if 'accents_found' in issues:
                        print(f"    Accents found: {issues['accents_found']}")
                    if 'special_chars' in issues:
                        print(f"    Special chars: {issues['special_chars']}")
                    if 'case_inconsistency' in issues:
                        print(f"    Case inconsistencies: {len(issues['case_inconsistency'])} found")
                        for normalized, variations in issues['case_inconsistency'].items():
                            print(f"      '{normalized}': {variations}")
                    if 'whitespace_issues' in issues:
                        print(f"    Whitespace issues: {issues['whitespace_issues']}")
        
        print(f"\n📁 CSV FILES CREATED:")
        for csv_file in result['csv_files_created']:
            print(f"  ✓ {csv_file}")
        
        print("\n✅ Analysis completed successfully!")
        return result
        
    except Exception as e:
        print(f"❌ Error analyzing Excel file: {str(e)}")
        return None

if __name__ == "__main__":
    test_excel_analyzer()