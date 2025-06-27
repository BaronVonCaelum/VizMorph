"""
Visualization Generator
Generates D3.js configurations and exports for suggested visualizations
"""

import json
import logging
from typing import Dict, List, Any, Optional
from src.viz_recommender import VizSuggestion, VizType

logger = logging.getLogger(__name__)

class VizGenerator:
    """Generates D3.js visualizations from suggestions"""
    
    def __init__(self):
        self.d3_templates = self._initialize_d3_templates()
    
    def generate_d3_config(self, suggestion: VizSuggestion) -> Dict[str, Any]:
        """Generate D3.js configuration for a visualization suggestion"""
        try:
            viz_type = suggestion.viz_type
            data_mapping = suggestion.data_mapping
            
            if viz_type in self.d3_templates:
                config = self.d3_templates[viz_type].copy()
                config['data_mapping'] = data_mapping
                config['title'] = suggestion.title
                config['description'] = suggestion.description
                return config
            else:
                return self._generate_generic_config(suggestion)
                
        except Exception as e:
            logger.error(f"Error generating D3 config: {str(e)}")
            raise
    
    def export_visualization(self, suggestion: VizSuggestion, format_type: str = 'json') -> Dict[str, Any]:
        """Export visualization in various formats"""
        try:
            if format_type == 'json':
                return self._export_json(suggestion)
            elif format_type == 'd3':
                return self._export_d3_code(suggestion)
            elif format_type == 'vega-lite':
                return self._export_vega_lite(suggestion)
            else:
                raise ValueError(f"Unsupported export format: {format_type}")
                
        except Exception as e:
            logger.error(f"Error exporting visualization: {str(e)}")
            raise
    
    def _initialize_d3_templates(self) -> Dict[VizType, Dict[str, Any]]:
        """Initialize D3.js templates for different visualization types"""
        return {
            VizType.BAR_CHART: {
                'type': 'bar_chart',
                'width': 800,
                'height': 400,
                'margin': {'top': 20, 'right': 30, 'bottom': 40, 'left': 40},
                'scales': {
                    'x': {'type': 'band', 'padding': 0.1},
                    'y': {'type': 'linear'}
                },
                'axes': {
                    'x': {'orient': 'bottom'},
                    'y': {'orient': 'left'}
                },
                'marks': {
                    'type': 'rect',
                    'fill': '#4A90E2'
                },
                'd3_code': self._get_bar_chart_d3_code()
            },
            
            VizType.LINE_CHART: {
                'type': 'line_chart',
                'width': 800,
                'height': 400,
                'margin': {'top': 20, 'right': 30, 'bottom': 40, 'left': 40},
                'scales': {
                    'x': {'type': 'time'},
                    'y': {'type': 'linear'}
                },
                'axes': {
                    'x': {'orient': 'bottom'},
                    'y': {'orient': 'left'}
                },
                'marks': {
                    'type': 'line',
                    'stroke': '#4A90E2',
                    'stroke_width': 2
                },
                'd3_code': self._get_line_chart_d3_code()
            },
            
            VizType.SCATTER_PLOT: {
                'type': 'scatter_plot',
                'width': 800,
                'height': 400,
                'margin': {'top': 20, 'right': 30, 'bottom': 40, 'left': 40},
                'scales': {
                    'x': {'type': 'linear'},
                    'y': {'type': 'linear'},
                    'size': {'type': 'sqrt', 'range': [4, 20]},
                    'color': {'type': 'ordinal', 'scheme': 'category10'}
                },
                'axes': {
                    'x': {'orient': 'bottom'},
                    'y': {'orient': 'left'}
                },
                'marks': {
                    'type': 'circle',
                    'fill': '#4A90E2',
                    'opacity': 0.7
                },
                'd3_code': self._get_scatter_plot_d3_code()
            },
            
            VizType.PIE_CHART: {
                'type': 'pie_chart',
                'width': 400,
                'height': 400,
                'radius': 150,
                'inner_radius': 0,
                'scales': {
                    'color': {'type': 'ordinal', 'scheme': 'category10'}
                },
                'marks': {
                    'type': 'arc'
                },
                'd3_code': self._get_pie_chart_d3_code()
            },
            
            VizType.HEATMAP: {
                'type': 'heatmap',
                'width': 800,
                'height': 400,
                'margin': {'top': 20, 'right': 30, 'bottom': 40, 'left': 40},
                'scales': {
                    'x': {'type': 'band'},
                    'y': {'type': 'band'},
                    'color': {'type': 'sequential', 'scheme': 'Blues'}
                },
                'axes': {
                    'x': {'orient': 'bottom'},
                    'y': {'orient': 'left'}
                },
                'marks': {
                    'type': 'rect'
                },
                'd3_code': self._get_heatmap_d3_code()
            },
            
            VizType.TREEMAP: {
                'type': 'treemap',
                'width': 800,
                'height': 400,
                'scales': {
                    'color': {'type': 'ordinal', 'scheme': 'category10'}
                },
                'marks': {
                    'type': 'rect',
                    'stroke': '#fff',
                    'stroke_width': 1
                },
                'd3_code': self._get_treemap_d3_code()
            },
            
            VizType.BUBBLE_CHART: {
                'type': 'bubble_chart',
                'width': 800,
                'height': 400,
                'margin': {'top': 20, 'right': 30, 'bottom': 40, 'left': 40},
                'scales': {
                    'x': {'type': 'linear'},
                    'y': {'type': 'linear'},
                    'size': {'type': 'sqrt', 'range': [10, 50]},
                    'color': {'type': 'ordinal', 'scheme': 'category10'}
                },
                'axes': {
                    'x': {'orient': 'bottom'},
                    'y': {'orient': 'left'}
                },
                'marks': {
                    'type': 'circle',
                    'opacity': 0.7
                },
                'd3_code': self._get_bubble_chart_d3_code()
            }
        }
    
    def _generate_generic_config(self, suggestion: VizSuggestion) -> Dict[str, Any]:
        """Generate a generic configuration for unsupported chart types"""
        return {
            'type': suggestion.viz_type.value,
            'width': 800,
            'height': 400,
            'margin': {'top': 20, 'right': 30, 'bottom': 40, 'left': 40},
            'data_mapping': suggestion.data_mapping,
            'title': suggestion.title,
            'description': suggestion.description,
            'message': 'Template not yet implemented for this visualization type'
        }
    
    def _export_json(self, suggestion: VizSuggestion) -> Dict[str, Any]:
        """Export visualization as JSON configuration"""
        return {
            'suggestion': {
                'id': suggestion.id,
                'viz_type': suggestion.viz_type.value,
                'title': suggestion.title,
                'description': suggestion.description,
                'rationale': suggestion.rationale,
                'confidence': suggestion.confidence,
                'improvements': suggestion.improvements
            },
            'd3_config': self.generate_d3_config(suggestion)
        }
    
    def _export_d3_code(self, suggestion: VizSuggestion) -> Dict[str, Any]:
        """Export as executable D3.js code"""
        config = self.generate_d3_config(suggestion)
        d3_code = config.get('d3_code', '// Code template not available')
        
        return {
            'html': self._generate_html_wrapper(suggestion, d3_code),
            'javascript': d3_code,
            'config': config
        }
    
    def _export_vega_lite(self, suggestion: VizSuggestion) -> Dict[str, Any]:
        """Export as Vega-Lite specification"""
        # This is a simplified conversion - real implementation would be more comprehensive
        data_mapping = suggestion.data_mapping
        
        vega_spec = {
            '$schema': 'https://vega.github.io/schema/vega-lite/v5.json',
            'title': suggestion.title,
            'description': suggestion.description,
            'width': 800,
            'height': 400,
            'data': {'name': 'data'},
            'mark': self._get_vega_mark_type(suggestion.viz_type),
            'encoding': self._convert_to_vega_encoding(data_mapping)
        }
        
        return {
            'vega_lite_spec': vega_spec,
            'suggestion_meta': {
                'id': suggestion.id,
                'confidence': suggestion.confidence,
                'rationale': suggestion.rationale
            }
        }
    
    def _get_vega_mark_type(self, viz_type: VizType) -> str:
        """Convert VizType to Vega-Lite mark type"""
        mapping = {
            VizType.BAR_CHART: 'bar',
            VizType.LINE_CHART: 'line',
            VizType.SCATTER_PLOT: 'point',
            VizType.PIE_CHART: 'arc',
            VizType.HEATMAP: 'rect',
            VizType.AREA_CHART: 'area',
            VizType.HISTOGRAM: 'bar'
        }
        return mapping.get(viz_type, 'point')
    
    def _convert_to_vega_encoding(self, data_mapping: Dict[str, Any]) -> Dict[str, Any]:
        """Convert data mapping to Vega-Lite encoding"""
        encoding = {}
        
        if 'x' in data_mapping and data_mapping['x']:
            encoding['x'] = {'field': data_mapping['x'], 'type': 'nominal'}
        
        if 'y' in data_mapping and data_mapping['y']:
            encoding['y'] = {'field': data_mapping['y'], 'type': 'quantitative'}
        
        if 'color' in data_mapping and data_mapping['color']:
            encoding['color'] = {'field': data_mapping['color'], 'type': 'nominal'}
        
        if 'size' in data_mapping and data_mapping['size']:
            encoding['size'] = {'field': data_mapping['size'], 'type': 'quantitative'}
        
        return encoding
    
    def _generate_html_wrapper(self, suggestion: VizSuggestion, d3_code: str) -> str:
        """Generate HTML wrapper for D3.js visualization"""
        return f'''<!DOCTYPE html>
<html>
<head>
    <title>{suggestion.title}</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
        }}
        .chart-container {{
            margin: 20px 0;
        }}
        .chart-title {{
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .chart-description {{
            font-size: 14px;
            color: #666;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="chart-container">
        <div class="chart-title">{suggestion.title}</div>
        <div class="chart-description">{suggestion.description}</div>
        <div id="chart"></div>
    </div>
    
    <script>
        {d3_code}
    </script>
</body>
</html>'''
    
    # D3.js Code Templates
    def _get_bar_chart_d3_code(self) -> str:
        return '''
// Bar Chart D3.js Code
const margin = {top: 20, right: 30, bottom: 40, left: 40};
const width = 800 - margin.left - margin.right;
const height = 400 - margin.top - margin.bottom;

const svg = d3.select("#chart")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

// Sample data - replace with actual data
const data = [
    {category: "A", value: 30},
    {category: "B", value: 80},
    {category: "C", value: 45},
    {category: "D", value: 60},
    {category: "E", value: 20}
];

const x = d3.scaleBand()
    .domain(data.map(d => d.category))
    .range([0, width])
    .padding(0.1);

const y = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.value)])
    .nice()
    .range([height, 0]);

svg.append("g")
    .attr("transform", `translate(0,${height})`)
    .call(d3.axisBottom(x));

svg.append("g")
    .call(d3.axisLeft(y));

svg.selectAll(".bar")
    .data(data)
    .enter().append("rect")
    .attr("class", "bar")
    .attr("x", d => x(d.category))
    .attr("width", x.bandwidth())
    .attr("y", d => y(d.value))
    .attr("height", d => height - y(d.value))
    .attr("fill", "#4A90E2");
'''
    
    def _get_line_chart_d3_code(self) -> str:
        return '''
// Line Chart D3.js Code
const margin = {top: 20, right: 30, bottom: 40, left: 40};
const width = 800 - margin.left - margin.right;
const height = 400 - margin.top - margin.bottom;

const svg = d3.select("#chart")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

// Sample data - replace with actual data
const data = [
    {date: new Date("2023-01-01"), value: 30},
    {date: new Date("2023-02-01"), value: 80},
    {date: new Date("2023-03-01"), value: 45},
    {date: new Date("2023-04-01"), value: 60},
    {date: new Date("2023-05-01"), value: 20}
];

const x = d3.scaleTime()
    .domain(d3.extent(data, d => d.date))
    .range([0, width]);

const y = d3.scaleLinear()
    .domain(d3.extent(data, d => d.value))
    .nice()
    .range([height, 0]);

const line = d3.line()
    .x(d => x(d.date))
    .y(d => y(d.value));

svg.append("g")
    .attr("transform", `translate(0,${height})`)
    .call(d3.axisBottom(x));

svg.append("g")
    .call(d3.axisLeft(y));

svg.append("path")
    .datum(data)
    .attr("fill", "none")
    .attr("stroke", "#4A90E2")
    .attr("stroke-width", 2)
    .attr("d", line);
'''
    
    def _get_scatter_plot_d3_code(self) -> str:
        return '''
// Scatter Plot D3.js Code
const margin = {top: 20, right: 30, bottom: 40, left: 40};
const width = 800 - margin.left - margin.right;
const height = 400 - margin.top - margin.bottom;

const svg = d3.select("#chart")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

// Sample data - replace with actual data
const data = [
    {x: 30, y: 20, size: 10, category: "A"},
    {x: 80, y: 80, size: 15, category: "B"},
    {x: 45, y: 45, size: 8, category: "A"},
    {x: 60, y: 60, size: 12, category: "C"},
    {x: 20, y: 30, size: 6, category: "B"}
];

const x = d3.scaleLinear()
    .domain(d3.extent(data, d => d.x))
    .nice()
    .range([0, width]);

const y = d3.scaleLinear()
    .domain(d3.extent(data, d => d.y))
    .nice()
    .range([height, 0]);

const size = d3.scaleSqrt()
    .domain(d3.extent(data, d => d.size))
    .range([4, 20]);

const color = d3.scaleOrdinal(d3.schemeCategory10);

svg.append("g")
    .attr("transform", `translate(0,${height})`)
    .call(d3.axisBottom(x));

svg.append("g")
    .call(d3.axisLeft(y));

svg.selectAll(".dot")
    .data(data)
    .enter().append("circle")
    .attr("class", "dot")
    .attr("r", d => size(d.size))
    .attr("cx", d => x(d.x))
    .attr("cy", d => y(d.y))
    .style("fill", d => color(d.category))
    .style("opacity", 0.7);
'''
    
    def _get_pie_chart_d3_code(self) -> str:
        return '''
// Pie Chart D3.js Code
const width = 400;
const height = 400;
const radius = Math.min(width, height) / 2;

const svg = d3.select("#chart")
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", `translate(${width/2},${height/2})`);

// Sample data - replace with actual data
const data = [
    {category: "A", value: 30},
    {category: "B", value: 80},
    {category: "C", value: 45},
    {category: "D", value: 60},
    {category: "E", value: 20}
];

const pie = d3.pie()
    .value(d => d.value);

const arc = d3.arc()
    .innerRadius(0)
    .outerRadius(radius);

const color = d3.scaleOrdinal(d3.schemeCategory10);

const arcs = svg.selectAll(".arc")
    .data(pie(data))
    .enter().append("g")
    .attr("class", "arc");

arcs.append("path")
    .attr("d", arc)
    .attr("fill", d => color(d.data.category));

arcs.append("text")
    .attr("transform", d => `translate(${arc.centroid(d)})`)
    .attr("dy", "0.35em")
    .style("text-anchor", "middle")
    .text(d => d.data.category);
'''
    
    def _get_heatmap_d3_code(self) -> str:
        return '''
// Heatmap D3.js Code
const margin = {top: 20, right: 30, bottom: 40, left: 40};
const width = 800 - margin.left - margin.right;
const height = 400 - margin.top - margin.bottom;

const svg = d3.select("#chart")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

// Sample data - replace with actual data
const data = [
    {x: "A", y: "1", value: 30},
    {x: "B", y: "1", value: 80},
    {x: "C", y: "1", value: 45},
    {x: "A", y: "2", value: 60},
    {x: "B", y: "2", value: 20},
    {x: "C", y: "2", value: 90}
];

const xCategories = [...new Set(data.map(d => d.x))];
const yCategories = [...new Set(data.map(d => d.y))];

const x = d3.scaleBand()
    .domain(xCategories)
    .range([0, width])
    .padding(0.1);

const y = d3.scaleBand()
    .domain(yCategories)
    .range([0, height])
    .padding(0.1);

const color = d3.scaleSequential(d3.interpolateBlues)
    .domain(d3.extent(data, d => d.value));

svg.selectAll(".tile")
    .data(data)
    .enter().append("rect")
    .attr("class", "tile")
    .attr("x", d => x(d.x))
    .attr("y", d => y(d.y))
    .attr("width", x.bandwidth())
    .attr("height", y.bandwidth())
    .attr("fill", d => color(d.value));
'''
    
    def _get_treemap_d3_code(self) -> str:
        return '''
// Treemap D3.js Code
const width = 800;
const height = 400;

const svg = d3.select("#chart")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

// Sample hierarchical data - replace with actual data
const data = {
    name: "root",
    children: [
        {name: "A", value: 100},
        {name: "B", value: 200},
        {name: "C", value: 150},
        {name: "D", value: 80}
    ]
};

const root = d3.hierarchy(data)
    .sum(d => d.value)
    .sort((a, b) => b.value - a.value);

const treemap = d3.treemap()
    .size([width, height])
    .padding(1);

treemap(root);

const color = d3.scaleOrdinal(d3.schemeCategory10);

const leaf = svg.selectAll("g")
    .data(root.leaves())
    .enter().append("g")
    .attr("transform", d => `translate(${d.x0},${d.y0})`);

leaf.append("rect")
    .attr("fill", d => color(d.data.name))
    .attr("width", d => d.x1 - d.x0)
    .attr("height", d => d.y1 - d.y0);

leaf.append("text")
    .attr("x", 4)
    .attr("y", 14)
    .text(d => d.data.name);
'''
    
    def _get_bubble_chart_d3_code(self) -> str:
        return '''
// Bubble Chart D3.js Code
const margin = {top: 20, right: 30, bottom: 40, left: 40};
const width = 800 - margin.left - margin.right;
const height = 400 - margin.top - margin.bottom;

const svg = d3.select("#chart")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

// Sample data - replace with actual data
const data = [
    {x: 30, y: 20, size: 100, category: "A"},
    {x: 80, y: 80, size: 200, category: "B"},
    {x: 45, y: 45, size: 150, category: "A"},
    {x: 60, y: 60, size: 120, category: "C"},
    {x: 20, y: 30, size: 80, category: "B"}
];

const x = d3.scaleLinear()
    .domain(d3.extent(data, d => d.x))
    .nice()
    .range([0, width]);

const y = d3.scaleLinear()
    .domain(d3.extent(data, d => d.y))
    .nice()
    .range([height, 0]);

const size = d3.scaleSqrt()
    .domain(d3.extent(data, d => d.size))
    .range([10, 50]);

const color = d3.scaleOrdinal(d3.schemeCategory10);

svg.append("g")
    .attr("transform", `translate(0,${height})`)
    .call(d3.axisBottom(x));

svg.append("g")
    .call(d3.axisLeft(y));

svg.selectAll(".bubble")
    .data(data)
    .enter().append("circle")
    .attr("class", "bubble")
    .attr("r", d => size(d.size))
    .attr("cx", d => x(d.x))
    .attr("cy", d => y(d.y))
    .style("fill", d => color(d.category))
    .style("opacity", 0.7);
'''
