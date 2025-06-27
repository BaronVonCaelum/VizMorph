================================================================================
                              VizMorph v1.0
            Tableau Workbook Visualization Suggestion Engine
================================================================================

WHAT IS VIZMORPH?
-----------------
VizMorph is a standalone desktop application that analyzes Tableau workbooks 
(.twb and .twbx files) and suggests alternative visualizations using intelligent 
heuristic rules. It helps you discover better ways to visualize your data 
without needing any server or complex setup.

FEATURES:
---------
✓ Parses Tableau workbook files (.twb/.twbx)
✓ Analyzes 11 worksheets and generates intelligent suggestions
✓ Uses 9 heuristic rules for visualization recommendations
✓ Provides confidence scores for each suggestion
✓ Exports suggestions in multiple formats (JSON, D3.js, Vega-Lite)
✓ No internet connection required
✓ No installation needed - just run the executable!

HOW TO USE:
-----------
1. Double-click "VizMorph.exe" or run "Run_VizMorph.bat"
2. Click "Browse..." to select your Tableau workbook file
3. Click "Analyze Workbook" and wait for processing
4. Review suggestions in the "Suggestions" tab
5. Select any suggestion to see detailed rationale and improvements
6. Export suggestions using the "Export" tab

SUPPORTED FILE TYPES:
--------------------
• Tableau Workbook (.twb)
• Tableau Packaged Workbook (.twbx)

SUGGESTION TYPES:
-----------------
VizMorph can suggest:
• Time Series Line Charts (for temporal data)
• Scatter Plots (for correlation analysis)
• Treemaps (for hierarchical or many-category data)
• Heatmaps (for multi-dimensional data)
• Bar Charts (for performance comparisons)
• Histograms (for distribution analysis)
• Box Plots (for statistical comparisons)
• Bubble Charts (for geographic or multi-variate data)
• Area Charts (for part-to-whole over time)
• Pie Charts (for simple proportional data)

HEURISTIC RULES:
---------------
1. Too Many Categories - Suggests space-efficient alternatives
2. Time Series Opportunity - Detects temporal patterns
3. Correlation Analysis - Identifies relationship opportunities
4. Distribution Analysis - Recommends statistical visualizations
5. Part-to-Whole - Suggests proportional representations
6. Hierarchical Data - Detects hierarchical structures
7. Multiple Measures - Handles complex multi-measure data
8. Geographic Data - Identifies location-based fields
9. Performance Comparison - Optimizes for KPI visualization

SYSTEM REQUIREMENTS:
-------------------
• Windows 7/8/10/11 (64-bit)
• At least 100MB free disk space
• No additional software required

EXPORT FORMATS:
--------------
• JSON Configuration - Complete suggestion data structure
• D3.js Code - Ready-to-use HTML with D3.js visualization
• Vega-Lite Specification - Industry-standard viz specification

TROUBLESHOOTING:
---------------
Q: The application won't start
A: Make sure you're running on a 64-bit Windows system and that antivirus 
   software isn't blocking the executable.

Q: Analysis fails or produces no suggestions
A: Ensure your Tableau file is valid and contains worksheets with data fields.
   The application works best with workbooks that have clearly defined 
   dimensions and measures.

Q: Export fails
A: Make sure you have write permissions in the directory where you're trying 
   to save the exported files.

CONTACT & SUPPORT:
-----------------
VizMorph is an open-source project. For issues, feature requests, or 
contributions, please visit: https://github.com/YOUR_USERNAME/VizMorph

LICENSE:
--------
MIT License - Free to use, modify, and distribute.

TECHNICAL DETAILS:
-----------------
• Built with Python and Tkinter
• Packaged with PyInstaller
• Uses XML parsing for Tableau workbook analysis
• Implements rule-based recommendation engine
• Generates D3.js and Vega-Lite compatible outputs

VERSION HISTORY:
---------------
v1.0 - Initial release
• Core parsing and suggestion functionality
• Desktop GUI interface
• Export capabilities
• 9 heuristic rules implemented

================================================================================
Thank you for using VizMorph! 
Transform your Tableau visualizations with intelligent suggestions.
================================================================================
