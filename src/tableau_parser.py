"""
Tableau Workbook Parser
Handles parsing of .twb and .twbx files to extract visualization structure and data
"""

import os
import zipfile
import xml.etree.ElementTree as ET
import json
import uuid
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class TableauParser:
    """Parser for Tableau workbook files (.twb, .twbx)"""
    
    def __init__(self):
        self.workbook_cache = {}
        self.ns = {'ts': 'http://www.tableausoftware.com/xml/user'}
    
    def parse_workbook(self, filepath: str) -> Dict[str, Any]:
        """Parse a Tableau workbook and extract visualization information"""
        try:
            workbook_id = str(uuid.uuid4())
            
            if filepath.endswith('.twbx'):
                # Extract .twb from .twbx archive
                xml_content = self._extract_twb_from_twbx(filepath)
            else:
                # Read .twb file directly
                with open(filepath, 'r', encoding='utf-8') as f:
                    xml_content = f.read()
            
            # Parse XML content
            root = ET.fromstring(xml_content)
            
            # Extract workbook information
            workbook_data = {
                'id': workbook_id,
                'filename': os.path.basename(filepath),
                'summary': self._extract_workbook_summary(root),
                'worksheets': self._extract_worksheets(root),
                'datasources': self._extract_datasources(root),
                'raw_xml': xml_content
            }
            
            # Cache the workbook data
            self.workbook_cache[workbook_id] = workbook_data
            
            logger.info(f"Successfully parsed workbook: {filepath}")
            return workbook_data
            
        except Exception as e:
            logger.error(f"Error parsing workbook {filepath}: {str(e)}")
            raise
    
    def get_workbook_data(self, workbook_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached workbook data by ID"""
        return self.workbook_cache.get(workbook_id)
    
    def _extract_twb_from_twbx(self, twbx_path: str) -> str:
        """Extract the .twb file content from a .twbx archive"""
        with zipfile.ZipFile(twbx_path, 'r') as zip_file:
            # Find the .twb file in the archive
            twb_files = [f for f in zip_file.namelist() if f.endswith('.twb')]
            if not twb_files:
                raise ValueError("No .twb file found in .twbx archive")
            
            # Read the first .twb file
            with zip_file.open(twb_files[0]) as twb_file:
                return twb_file.read().decode('utf-8')
    
    def _extract_workbook_summary(self, root: ET.Element) -> Dict[str, Any]:
        """Extract high-level workbook information"""
        summary = {
            'name': root.get('name', 'Untitled'),
            'version': root.get('version', 'Unknown'),
            'worksheet_count': 0,
            'dashboard_count': 0,
            'story_count': 0
        }
        
        # Count different types of sheets
        worksheets = root.findall('.//worksheet')
        dashboards = root.findall('.//dashboard')
        stories = root.findall('.//story')
        
        summary['worksheet_count'] = len(worksheets)
        summary['dashboard_count'] = len(dashboards)
        summary['story_count'] = len(stories)
        
        return summary
    
    def _extract_worksheets(self, root: ET.Element) -> List[Dict[str, Any]]:
        """Extract worksheet information and visualization specs"""
        worksheets = []
        
        for worksheet in root.findall('.//worksheet'):
            ws_data = {
                'name': worksheet.get('name', 'Unnamed'),
                'marks': self._extract_marks(worksheet),
                'shelves': self._extract_shelves(worksheet),
                'filters': self._extract_filters(worksheet),
                'viz_type': self._infer_viz_type(worksheet),
                'dimensions': [],
                'measures': []
            }
            
            # Extract field usage
            ws_data['dimensions'], ws_data['measures'] = self._extract_field_usage(worksheet)
            
            worksheets.append(ws_data)
        
        return worksheets
    
    def _extract_marks(self, worksheet: ET.Element) -> Dict[str, Any]:
        """Extract mark properties from worksheet"""
        marks = {
            'mark_type': 'automatic',
            'encoding': {}
        }
        
        # Find mark specifications
        mark_element = worksheet.find('.//mark')
        if mark_element is not None:
            marks['mark_type'] = mark_element.get('class', 'automatic')
        
        return marks
    
    def _extract_shelves(self, worksheet: ET.Element) -> Dict[str, List[str]]:
        """Extract field assignments to shelves (rows, columns, etc.)"""
        shelves = {
            'columns': [],
            'rows': [],
            'color': [],
            'size': [],
            'shape': [],
            'label': [],
            'detail': [],
            'tooltip': []
        }
        
        # Map Tableau shelf names to our structure
        shelf_mapping = {
            'columns-shelf': 'columns',
            'rows-shelf': 'rows',
            'color-shelf': 'color',
            'size-shelf': 'size',
            'shape-shelf': 'shape',
            'text-shelf': 'label',
            'detail-shelf': 'detail',
            'tooltip-shelf': 'tooltip'
        }
        
        # Try multiple approaches to find shelf information
        for shelf_name, shelf_key in shelf_mapping.items():
            # Method 1: Direct shelf attribute
            shelf_elements = worksheet.findall(f'.//*[@shelf="{shelf_name}"]')
            for element in shelf_elements:
                field_name = element.get('name', '')
                if field_name:
                    shelves[shelf_key].append(field_name)
        
        # Method 2: Look for pane elements with specific shelf names
        panes = worksheet.findall('.//pane')
        for pane in panes:
            pane_name = pane.get('name', '')
            if 'columns' in pane_name.lower():
                for field in pane.findall('.//field'):
                    field_name = field.get('name', '')
                    if field_name and field_name not in shelves['columns']:
                        shelves['columns'].append(field_name)
            elif 'rows' in pane_name.lower():
                for field in pane.findall('.//field'):
                    field_name = field.get('name', '')
                    if field_name and field_name not in shelves['rows']:
                        shelves['rows'].append(field_name)
        
        return shelves
    
    def _extract_filters(self, worksheet: ET.Element) -> List[Dict[str, Any]]:
        """Extract filter information"""
        filters = []
        
        filter_elements = worksheet.findall('.//filter')
        for filter_elem in filter_elements:
            filter_data = {
                'field': filter_elem.get('column', ''),
                'type': filter_elem.get('class', 'categorical'),
                'values': []
            }
            
            # Extract filter values
            for value_elem in filter_elem.findall('.//groupfilter'):
                member = value_elem.get('member')
                if member:
                    filter_data['values'].append(member)
            
            filters.append(filter_data)
        
        return filters
    
    def _extract_field_usage(self, worksheet: ET.Element) -> tuple:
        """Extract dimensions and measures used in the worksheet"""
        dimensions = []
        measures = []
        
        # This is a more robust extraction that also considers shelf info
        field_elements = worksheet.findall('.//datasource-dependencies/.//column')
        for field in field_elements:
            field_name = field.get('name')
            field_role = field.get('role')
            
            if field_name:
                if field_role == 'measure':
                    measures.append(field_name)
                elif field_role == 'dimension':
                    dimensions.append(field_name)
        
        # Fallback to shelf info if direct dependencies are not found
        if not dimensions and not measures:
            for shelf in self._extract_shelves(worksheet).values():
                for field_name in shelf:
                    # Simple heuristic: fields with aggregation are measures
                    if any(agg in field_name for agg in ['SUM', 'AVG', 'COUNT']):
                        measures.append(field_name)
                    else:
                        dimensions.append(field_name)
        
        return dimensions, measures
    
    def _infer_viz_type(self, worksheet: ET.Element) -> str:
        """Infer the visualization type based on marks and shelves"""
        # This is a simplified heuristic - real implementation would be more sophisticated
        mark_element = worksheet.find('.//mark')
        if mark_element is not None:
            mark_type = mark_element.get('class', 'automatic')
            
            if mark_type == 'Bar':
                return 'bar_chart'
            elif mark_type == 'Line':
                return 'line_chart'
            elif mark_type == 'Circle':
                return 'scatter_plot'
            elif mark_type == 'Square':
                return 'heatmap'
            elif mark_type == 'Pie':
                return 'pie_chart'
        
        return 'unknown'
    
    def _extract_datasources(self, root: ET.Element) -> List[Dict[str, Any]]:
        """Extract data source information"""
        datasources = []
        
        for datasource in root.findall('.//datasource'):
            ds_data = {
                'name': datasource.get('name', 'Unnamed'),
                'connection': self._extract_connection_info(datasource),
                'columns': self._extract_column_info(datasource)
            }
            datasources.append(ds_data)
        
        return datasources
    
    def _extract_connection_info(self, datasource: ET.Element) -> Dict[str, str]:
        """Extract connection information from datasource"""
        connection = datasource.find('.//connection')
        if connection is not None:
            return {
                'class': connection.get('class', ''),
                'dbname': connection.get('dbname', ''),
                'server': connection.get('server', ''),
                'username': connection.get('username', '')
            }
        return {}
    
    def _extract_column_info(self, datasource: ET.Element) -> List[Dict[str, str]]:
        """Extract column/field information from datasource"""
        columns = []
        
        for column in datasource.findall('.//column'):
            col_data = {
                'name': column.get('name', ''),
                'datatype': column.get('datatype', ''),
                'role': column.get('role', ''),
                'type': column.get('type', '')
            }
            columns.append(col_data)
        
        return columns
