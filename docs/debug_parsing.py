#!/usr/bin/env python3
"""
Debug script to analyze what's being extracted from real Tableau workbooks
"""

import sys
import os
import json
from pprint import pprint

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tableau_parser import TableauParser
from viz_recommender import VizRecommender

def debug_workbook_parsing():
    """Debug the parsing of uploaded workbooks"""
    parser = TableauParser()
    recommender = VizRecommender()
    
    # Check uploaded files
    uploads_dir = 'uploads'
    tableau_files = [f for f in os.listdir(uploads_dir) if f.endswith(('.twb', '.twbx'))]
    
    if not tableau_files:
        print("No Tableau files found in uploads directory")
        return
    
    print(f"Found {len(tableau_files)} Tableau files:")
    for f in tableau_files:
        print(f"  - {f}")
    
    # Analyze each file
    for filename in tableau_files:
        filepath = os.path.join(uploads_dir, filename)
        print(f"\n{'='*60}")
        print(f"ANALYZING: {filename}")
        print(f"{'='*60}")
        
        try:
            # Parse the workbook
            workbook_data = parser.parse_workbook(filepath)
            
            print(f"\n📊 WORKBOOK SUMMARY:")
            print(f"  Name: {workbook_data['summary']['name']}")
            print(f"  Version: {workbook_data['summary']['version']}")
            print(f"  Worksheets: {workbook_data['summary']['worksheet_count']}")
            print(f"  Dashboards: {workbook_data['summary']['dashboard_count']}")
            print(f"  Stories: {workbook_data['summary']['story_count']}")
            
            print(f"\n📋 WORKSHEETS DETAIL:")
            for i, worksheet in enumerate(workbook_data['worksheets'], 1):
                print(f"\n  Worksheet {i}: {worksheet['name']}")
                print(f"    Viz Type: {worksheet['viz_type']}")
                print(f"    Dimensions: {worksheet['dimensions']}")
                print(f"    Measures: {worksheet['measures']}")
                print(f"    Shelves: {json.dumps(worksheet['shelves'], indent=6)}")
                print(f"    Filters: {len(worksheet['filters'])} filters")
            
            print(f"\n💡 GENERATING SUGGESTIONS...")
            suggestions = recommender.generate_suggestions(workbook_data)
            
            print(f"\n🎯 SUGGESTIONS RESULT:")
            print(f"  Total suggestions: {len(suggestions)}")
            
            if suggestions:
                for i, suggestion in enumerate(suggestions, 1):
                    print(f"\n  Suggestion {i}:")
                    print(f"    Title: {suggestion['title']}")
                    print(f"    Type: {suggestion['viz_type']}")
                    print(f"    Confidence: {suggestion['confidence']:.2f}")
                    print(f"    Rationale: {suggestion['rationale']}")
            else:
                print("  ❌ NO SUGGESTIONS GENERATED")
                print("\n🔍 DEBUGGING WHY NO SUGGESTIONS:")
                
                # Check each worksheet against each rule
                for worksheet in workbook_data['worksheets']:
                    print(f"\n  Worksheet '{worksheet['name']}':")
                    print(f"    Current viz type: {worksheet['viz_type']}")
                    print(f"    Dimensions: {worksheet['dimensions']} (count: {len(worksheet['dimensions'])})")
                    print(f"    Measures: {worksheet['measures']} (count: {len(worksheet['measures'])})")
                    
                    # Check specific rule conditions
                    print(f"    Rule checks:")
                    
                    # Time series check
                    temporal_fields = [d for d in worksheet.get('dimensions', []) if any(keyword in d.lower() 
                                      for keyword in ['date', 'time', 'year', 'month', 'day', 'quarter'])]
                    print(f"      - Temporal fields found: {temporal_fields}")
                    
                    # Performance measures check
                    performance_patterns = ['sales', 'revenue', 'profit', 'performance', 'score', 'rating']
                    performance_measures = [m for m in worksheet.get('measures', []) if any(pattern in m.lower() for pattern in performance_patterns)]
                    print(f"      - Performance measures: {performance_measures}")
                    
                    # Category check
                    category_dims = [d for d in worksheet.get('dimensions', []) if any(keyword in d.lower() for keyword in ['id', 'name', 'code', 'product'])]
                    print(f"      - Category dimensions: {category_dims}")
                    
                    # Geographic check
                    geo_patterns = ['country', 'state', 'city', 'region', 'latitude', 'longitude', 'zip', 'postal']
                    geo_dims = [d for d in worksheet.get('dimensions', []) if any(pattern in d.lower() for pattern in geo_patterns)]
                    print(f"      - Geographic dimensions: {geo_dims}")
            
        except Exception as e:
            print(f"❌ ERROR parsing {filename}: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    debug_workbook_parsing()
