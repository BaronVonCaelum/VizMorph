"""
Visualization Recommendation Engine
Uses heuristics to suggest alternative visualizations based on data characteristics
"""

import uuid
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class VizType(Enum):
    """Supported visualization types"""
    BAR_CHART = "bar_chart"
    LINE_CHART = "line_chart"
    SCATTER_PLOT = "scatter_plot"
    HEATMAP = "heatmap"
    PIE_CHART = "pie_chart"
    AREA_CHART = "area_chart"
    HISTOGRAM = "histogram"
    BOX_PLOT = "box_plot"
    TREEMAP = "treemap"
    BUBBLE_CHART = "bubble_chart"

@dataclass
class VizSuggestion:
    """Data class for visualization suggestions"""
    id: str
    viz_type: VizType
    title: str
    description: str
    rationale: str
    confidence: float
    data_mapping: Dict[str, Any]
    original_worksheet: str
    improvements: List[str]

class VizRecommender:
    """Generates visualization suggestions using heuristic rules"""
    
    def __init__(self):
        self.suggestion_cache = {}
        self.rules = self._initialize_rules()
    
    def generate_suggestions(self, workbook_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate visualization suggestions for a workbook"""
        suggestions = []
        
        for worksheet in workbook_data['worksheets']:
            ws_suggestions = self._analyze_worksheet(worksheet, workbook_data)
            suggestions.extend(ws_suggestions)
        
        # Sort suggestions by confidence score
        suggestions.sort(key=lambda x: x.confidence, reverse=True)
        
        return [self._serialize_suggestion(s) for s in suggestions]
    
    def get_suggestion(self, suggestion_id: str) -> Optional[VizSuggestion]:
        """Retrieve a specific suggestion by ID"""
        return self.suggestion_cache.get(suggestion_id)
    
    def _analyze_worksheet(self, worksheet: Dict[str, Any], workbook_data: Dict[str, Any]) -> List[VizSuggestion]:
        """Analyze a single worksheet and generate suggestions"""
        suggestions = []
        
        # Extract key characteristics
        dimensions = worksheet.get('dimensions', [])
        measures = worksheet.get('measures', [])
        current_viz_type = worksheet.get('viz_type', 'unknown')
        shelves = worksheet.get('shelves', {})
        
        # Apply heuristic rules
        for rule in self.rules:
            rule_suggestions = rule(worksheet, workbook_data)
            suggestions.extend(rule_suggestions)
        
        # Cache suggestions
        for suggestion in suggestions:
            self.suggestion_cache[suggestion.id] = suggestion
        
        return suggestions
    
    def _initialize_rules(self) -> List:
        """Initialize heuristic rules for visualization recommendations"""
        return [
            self._rule_too_many_categories,
            self._rule_time_series_opportunity,
            self._rule_correlation_opportunity,
            self._rule_distribution_analysis,
            self._rule_part_to_whole,
            self._rule_hierarchical_data,
            self._rule_multiple_measures,
            self._rule_geographic_data,
            self._rule_performance_comparison
        ]
    
    def _rule_too_many_categories(self, worksheet: Dict[str, Any], workbook_data: Dict[str, Any]) -> List[VizSuggestion]:
        """Suggest alternatives when there are too many categories in bar charts"""
        suggestions = []
        
        if worksheet['viz_type'] == 'bar_chart':
            dimensions = worksheet.get('dimensions', [])
            
            # Heuristic: if likely many categories, suggest alternatives
            for dim in dimensions:
                if any(keyword in dim.lower() for keyword in ['id', 'name', 'code', 'product']):
                    suggestions.append(VizSuggestion(
                        id=str(uuid.uuid4()),
                        viz_type=VizType.TREEMAP,
                        title=f"Treemap for {worksheet['name']}",
                        description="Use a treemap to better handle large numbers of categories",
                        rationale="Bar charts become cluttered with many categories. Treemaps use space more efficiently.",
                        confidence=0.75,
                        data_mapping={
                            'size': worksheet.get('measures', [])[0] if worksheet.get('measures') else None,
                            'color': dimensions[0] if dimensions else None
                        },
                        original_worksheet=worksheet['name'],
                        improvements=["Better space utilization", "Easier to compare relative sizes", "Supports hierarchical grouping"]
                    ))
                    
                    suggestions.append(VizSuggestion(
                        id=str(uuid.uuid4()),
                        viz_type=VizType.BUBBLE_CHART,
                        title=f"Bubble Chart for {worksheet['name']}",
                        description="Use a bubble chart to show relationships between multiple dimensions",
                        rationale="Bubble charts can encode more information than bar charts and handle many data points well.",
                        confidence=0.65,
                        data_mapping={
                            'x': dimensions[0] if dimensions else None,
                            'y': worksheet.get('measures', [])[0] if worksheet.get('measures') else None,
                            'size': worksheet.get('measures', [])[1] if len(worksheet.get('measures', [])) > 1 else None
                        },
                        original_worksheet=worksheet['name'],
                        improvements=["Shows relationships between variables", "Handles large datasets", "Multiple encoding channels"]
                    ))
        
        return suggestions
    
    def _rule_time_series_opportunity(self, worksheet: Dict[str, Any], workbook_data: Dict[str, Any]) -> List[VizSuggestion]:
        """Suggest time series visualizations when temporal data is detected"""
        suggestions = []
        
        dimensions = worksheet.get('dimensions', [])
        measures = worksheet.get('measures', [])
        
        # Look for temporal dimensions
        temporal_fields = [d for d in dimensions if any(keyword in d.lower() 
                          for keyword in ['date', 'time', 'year', 'month', 'day', 'quarter'])]
        
        if temporal_fields and measures:
            if worksheet['viz_type'] != 'line_chart':
                suggestions.append(VizSuggestion(
                    id=str(uuid.uuid4()),
                    viz_type=VizType.LINE_CHART,
                    title=f"Time Series Line Chart for {worksheet['name']}",
                    description="Use a line chart to show trends over time",
                    rationale="Line charts are optimal for showing temporal patterns and trends.",
                    confidence=0.85,
                    data_mapping={
                        'x': temporal_fields[0],
                        'y': measures[0],
                        'color': dimensions[1] if len(dimensions) > 1 else None
                    },
                    original_worksheet=worksheet['name'],
                    improvements=["Better shows temporal trends", "Easier to spot patterns", "Standard for time series data"]
                ))
            
            if len(measures) > 1:
                suggestions.append(VizSuggestion(
                    id=str(uuid.uuid4()),
                    viz_type=VizType.AREA_CHART,
                    title=f"Stacked Area Chart for {worksheet['name']}",
                    description="Use a stacked area chart to show composition over time",
                    rationale="Area charts show both trends and part-to-whole relationships in temporal data.",
                    confidence=0.70,
                    data_mapping={
                        'x': temporal_fields[0],
                        'y': measures,
                        'stack': True
                    },
                    original_worksheet=worksheet['name'],
                    improvements=["Shows composition changes", "Emphasizes cumulative values", "Good for multiple series"]
                ))
        
        return suggestions
    
    def _rule_correlation_opportunity(self, worksheet: Dict[str, Any], workbook_data: Dict[str, Any]) -> List[VizSuggestion]:
        """Suggest scatter plots for correlation analysis"""
        suggestions = []
        
        measures = worksheet.get('measures', [])
        
        if len(measures) >= 2 and worksheet['viz_type'] != 'scatter_plot':
            suggestions.append(VizSuggestion(
                id=str(uuid.uuid4()),
                viz_type=VizType.SCATTER_PLOT,
                title=f"Scatter Plot for {worksheet['name']}",
                description="Use a scatter plot to explore correlations between measures",
                rationale="Scatter plots are ideal for revealing relationships between continuous variables.",
                confidence=0.80,
                data_mapping={
                    'x': measures[0],
                    'y': measures[1],
                    'size': measures[2] if len(measures) > 2 else None,
                    'color': worksheet.get('dimensions', [])[0] if worksheet.get('dimensions') else None
                },
                original_worksheet=worksheet['name'],
                improvements=["Reveals correlations", "Shows data distribution", "Identifies outliers"]
            ))
        
        return suggestions
    
    def _rule_distribution_analysis(self, worksheet: Dict[str, Any], workbook_data: Dict[str, Any]) -> List[VizSuggestion]:
        """Suggest distribution visualizations"""
        suggestions = []
        
        measures = worksheet.get('measures', [])
        
        if measures and worksheet['viz_type'] not in ['histogram', 'box_plot']:
            # Suggest histogram for single measure distribution
            suggestions.append(VizSuggestion(
                id=str(uuid.uuid4()),
                viz_type=VizType.HISTOGRAM,
                title=f"Distribution Histogram for {worksheet['name']}",
                description="Use a histogram to show data distribution",
                rationale="Histograms reveal the shape and spread of data distributions.",
                confidence=0.60,
                data_mapping={
                    'x': measures[0],
                    'bins': 'auto'
                },
                original_worksheet=worksheet['name'],
                improvements=["Shows data distribution", "Identifies skewness", "Reveals outliers"]
            ))
            
            # Suggest box plot for distribution comparison
            dimensions = worksheet.get('dimensions', [])
            if dimensions:
                suggestions.append(VizSuggestion(
                    id=str(uuid.uuid4()),
                    viz_type=VizType.BOX_PLOT,
                    title=f"Box Plot for {worksheet['name']}",
                    description="Use a box plot to compare distributions across categories",
                    rationale="Box plots efficiently show distribution statistics and facilitate comparisons.",
                    confidence=0.65,
                    data_mapping={
                        'x': dimensions[0],
                        'y': measures[0]
                    },
                    original_worksheet=worksheet['name'],
                    improvements=["Shows quartiles and outliers", "Compact distribution summary", "Good for comparisons"]
                ))
        
        return suggestions
    
    def _rule_part_to_whole(self, worksheet: Dict[str, Any], workbook_data: Dict[str, Any]) -> List[VizSuggestion]:
        """Suggest part-to-whole visualizations"""
        suggestions = []
        
        dimensions = worksheet.get('dimensions', [])
        measures = worksheet.get('measures', [])
        
        if len(dimensions) == 1 and len(measures) == 1:
            # Check if current viz is appropriate for part-to-whole
            if worksheet['viz_type'] == 'bar_chart':
                suggestions.append(VizSuggestion(
                    id=str(uuid.uuid4()),
                    viz_type=VizType.PIE_CHART,
                    title=f"Pie Chart for {worksheet['name']}",
                    description="Use a pie chart to emphasize part-to-whole relationships",
                    rationale="Pie charts make proportional relationships more apparent than bar charts.",
                    confidence=0.55,
                    data_mapping={
                        'angle': measures[0],
                        'color': dimensions[0]
                    },
                    original_worksheet=worksheet['name'],
                    improvements=["Emphasizes proportions", "Shows parts of a whole", "Intuitive for percentages"]
                ))
        
        return suggestions
    
    def _rule_hierarchical_data(self, worksheet: Dict[str, Any], workbook_data: Dict[str, Any]) -> List[VizSuggestion]:
        """Detect hierarchical data patterns and suggest appropriate visualizations"""
        suggestions = []
        
        dimensions = worksheet.get('dimensions', [])
        measures = worksheet.get('measures', [])
        
        # Look for hierarchical patterns in dimension names
        hierarchical_patterns = ['category', 'subcategory', 'region', 'country', 'state', 'city']
        hierarchical_dims = [d for d in dimensions if any(pattern in d.lower() for pattern in hierarchical_patterns)]
        
        if len(hierarchical_dims) >= 2 and measures:
            suggestions.append(VizSuggestion(
                id=str(uuid.uuid4()),
                viz_type=VizType.TREEMAP,
                title=f"Hierarchical Treemap for {worksheet['name']}",
                description="Use a treemap to show hierarchical data structure",
                rationale="Treemaps excel at showing hierarchical relationships and proportional sizing.",
                confidence=0.75,
                data_mapping={
                    'hierarchy': hierarchical_dims,
                    'size': measures[0],
                    'color': measures[1] if len(measures) > 1 else measures[0]
                },
                original_worksheet=worksheet['name'],
                improvements=["Shows hierarchy clearly", "Space-efficient", "Supports drill-down"]
            ))
        
        return suggestions
    
    def _rule_multiple_measures(self, worksheet: Dict[str, Any], workbook_data: Dict[str, Any]) -> List[VizSuggestion]:
        """Handle cases with multiple measures"""
        suggestions = []
        
        measures = worksheet.get('measures', [])
        dimensions = worksheet.get('dimensions', [])
        
        if len(measures) > 2:
            # Suggest heatmap for measure comparison
            suggestions.append(VizSuggestion(
                id=str(uuid.uuid4()),
                viz_type=VizType.HEATMAP,
                title=f"Measures Heatmap for {worksheet['name']}",
                description="Use a heatmap to compare multiple measures across dimensions",
                rationale="Heatmaps efficiently display patterns in multi-dimensional data.",
                confidence=0.70,
                data_mapping={
                    'x': dimensions[0] if dimensions else None,
                    'y': measures,
                    'color': 'value'
                },
                original_worksheet=worksheet['name'],
                improvements=["Handles many measures", "Shows patterns visually", "Compact representation"]
            ))
        
        return suggestions
    
    def _rule_geographic_data(self, worksheet: Dict[str, Any], workbook_data: Dict[str, Any]) -> List[VizSuggestion]:
        """Detect geographic data and suggest map visualizations"""
        suggestions = []
        
        dimensions = worksheet.get('dimensions', [])
        geo_patterns = ['country', 'state', 'city', 'region', 'latitude', 'longitude', 'zip', 'postal']
        
        geo_dims = [d for d in dimensions if any(pattern in d.lower() for pattern in geo_patterns)]
        
        if geo_dims:
            # Note: This would typically suggest a map visualization
            # For this example, we'll suggest a bubble chart as a proxy
            measures = worksheet.get('measures', [])
            if measures:
                suggestions.append(VizSuggestion(
                    id=str(uuid.uuid4()),
                    viz_type=VizType.BUBBLE_CHART,
                    title=f"Geographic Bubble Chart for {worksheet['name']}",
                    description="Use a bubble chart to show geographic distribution of data",
                    rationale="Bubble charts can effectively represent geographic data when maps aren't available.",
                    confidence=0.60,
                    data_mapping={
                        'x': geo_dims[0],
                        'y': measures[0],
                        'size': measures[1] if len(measures) > 1 else measures[0]
                    },
                    original_worksheet=worksheet['name'],
                    improvements=["Shows geographic patterns", "Handles multiple measures", "Easy to identify hotspots"]
                ))
        
        return suggestions
    
    def _rule_performance_comparison(self, worksheet: Dict[str, Any], workbook_data: Dict[str, Any]) -> List[VizSuggestion]:
        """Suggest visualizations for performance comparison"""
        suggestions = []
        
        measures = worksheet.get('measures', [])
        dimensions = worksheet.get('dimensions', [])
        
        # Look for performance-related measures
        performance_patterns = ['sales', 'revenue', 'profit', 'performance', 'score', 'rating']
        performance_measures = [m for m in measures if any(pattern in m.lower() for pattern in performance_patterns)]
        
        if performance_measures and dimensions:
            if worksheet['viz_type'] != 'bar_chart':
                suggestions.append(VizSuggestion(
                    id=str(uuid.uuid4()),
                    viz_type=VizType.BAR_CHART,
                    title=f"Performance Bar Chart for {worksheet['name']}",
                    description="Use a bar chart for clear performance comparisons",
                    rationale="Bar charts are optimal for comparing performance metrics across categories.",
                    confidence=0.75,
                    data_mapping={
                        'x': dimensions[0],
                        'y': performance_measures[0],
                        'color': dimensions[1] if len(dimensions) > 1 else None
                    },
                    original_worksheet=worksheet['name'],
                    improvements=["Clear comparisons", "Standard for performance", "Easy to rank"]
                ))
        
        return suggestions
    
    def _serialize_suggestion(self, suggestion: VizSuggestion) -> Dict[str, Any]:
        """Convert VizSuggestion to dictionary for JSON serialization"""
        return {
            'id': suggestion.id,
            'viz_type': suggestion.viz_type.value,
            'title': suggestion.title,
            'description': suggestion.description,
            'rationale': suggestion.rationale,
            'confidence': suggestion.confidence,
            'data_mapping': suggestion.data_mapping,
            'original_worksheet': suggestion.original_worksheet,
            'improvements': suggestion.improvements
        }
