# VizMorph

VizMorph is a Python-based application that analyzes Tableau workbooks and suggests alternative visualizations using heuristic rules. It provides a Flask API backend with D3.js visualization previews and an optional Electron-based desktop UI.

## Features

- **Tableau Workbook Parsing**: Supports both .twb and .twbx file formats
- **Intelligent Suggestions**: Uses heuristic rules to suggest alternative visualizations
- **D3.js Previews**: Generates interactive D3.js visualizations for suggested charts
- **Multiple Export Formats**: Export suggestions as JSON, D3.js code, or Vega-Lite specifications
- **Web Interface**: Flask-based web interface for browser access
- **Desktop App**: Electron-based desktop application for native OS integration
- **RESTful API**: Complete API for integration with other tools

## Architecture

### Core Components

1. **Tableau Parser** (`src/tableau_parser.py`): Extracts visualization structure from Tableau workbooks
2. **Visualization Recommender** (`src/viz_recommender.py`): Applies heuristic rules to suggest alternatives
3. **Visualization Generator** (`src/viz_generator.py`): Creates D3.js configurations and exports
4. **Flask API** (`app.py`): RESTful API endpoints for all functionality
5. **Web Interface** (`templates/index.html`): Browser-based user interface
6. **Electron App** (`electron-ui/`): Desktop application with native OS integration

### Supported Visualization Types

- Bar Charts
- Line Charts
- Scatter Plots
- Pie Charts
- Heatmaps
- Treemaps
- Bubble Charts
- Area Charts
- Histograms
- Box Plots

## Installation

### Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher (for Electron app)

### Python Backend Setup

1. Clone or download the project:
```bash
cd VizMorph
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Electron Desktop App Setup (Optional)

1. Navigate to the Electron directory:
```bash
cd electron-ui
```

2. Install Node.js dependencies:
```bash
npm install
```

## Usage

### Starting the Flask API Server

1. Activate your virtual environment (if not already active)
2. Run the Flask application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Using the Web Interface

1. Start the Flask server (see above)
2. Open your browser and go to `http://localhost:5000`
3. Upload a Tableau workbook (.twb or .twbx file)
4. Review the generated suggestions
5. Preview and export visualizations

### Using the Desktop App

1. Start the Flask server first
2. In the `electron-ui` directory, run:
```bash
npm start
```

The desktop application will launch with enhanced features like native file dialogs and menu integration.

### Using the API Directly

#### Upload a Workbook
```bash
curl -X POST -F "file=@your_workbook.twb" http://localhost:5000/api/upload
```

#### Get Suggestions
```bash
curl http://localhost:5000/api/suggest/{workbook_id}
```

#### Preview a Suggestion
```bash
curl http://localhost:5000/api/preview/{suggestion_id}
```

#### Export a Visualization
```bash
curl "http://localhost:5000/api/export/{suggestion_id}?format=d3"
```

## API Reference

### Endpoints

- `POST /api/upload` - Upload and parse a Tableau workbook
- `GET /api/suggest/{workbook_id}` - Get visualization suggestions
- `GET /api/preview/{suggestion_id}` - Generate D3.js preview configuration
- `GET /api/export/{suggestion_id}` - Export visualization (supports json, d3, vega-lite formats)

### Response Format

All API responses follow this structure:
```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

## Heuristic Rules

VizMorph uses the following heuristic rules to generate suggestions:

1. **Too Many Categories**: Suggests treemaps or bubble charts for bar charts with many categories
2. **Time Series Opportunity**: Detects temporal data and suggests line/area charts
3. **Correlation Analysis**: Suggests scatter plots when multiple measures are present
4. **Distribution Analysis**: Recommends histograms and box plots for data distribution
5. **Part-to-Whole**: Suggests pie charts for proportional data
6. **Hierarchical Data**: Detects hierarchical patterns and suggests treemaps
7. **Multiple Measures**: Recommends heatmaps for comparing many measures
8. **Geographic Data**: Identifies geographic fields and suggests appropriate visualizations
9. **Performance Comparison**: Optimizes visualizations for performance metrics

## Configuration

### Environment Variables

- `FLASK_ENV`: Set to `development` for debug mode
- `FLASK_PORT`: Override default port (5000)
- `MAX_CONTENT_LENGTH`: Maximum file upload size (default: 50MB)

### Customizing Heuristics

To add new heuristic rules:

1. Add a new method to the `VizRecommender` class in `src/viz_recommender.py`
2. Register the rule in the `_initialize_rules()` method
3. Follow the existing pattern for rule implementation

### Adding Visualization Types

To support new visualization types:

1. Add the type to the `VizType` enum in `src/viz_recommender.py`
2. Create a D3.js template in `src/viz_generator.py`
3. Add appropriate heuristic rules for when to suggest the new type

## Development

### Project Structure

```
VizMorph/
├── src/                          # Core Python modules
│   ├── __init__.py
│   ├── tableau_parser.py         # Tableau workbook parsing
│   ├── viz_recommender.py        # Visualization suggestion engine
│   └── viz_generator.py          # D3.js generation and exports
├── templates/                    # Flask templates
│   └── index.html               # Web interface
├── static/                      # Static web assets
├── electron-ui/                 # Electron desktop app
│   ├── main.js                  # Electron main process
│   ├── index.html               # Electron renderer
│   └── package.json             # Node.js dependencies
├── uploads/                     # Uploaded workbook storage
├── app.py                       # Flask application entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

### Testing

Create test Tableau workbooks and upload them to verify the parsing and suggestion functionality. The application includes comprehensive error handling and logging.

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Troubleshooting

### Common Issues

1. **File Upload Fails**: Check file size limits and ensure the file is a valid .twb or .twbx
2. **No Suggestions Generated**: Verify the workbook contains visualizations with identifiable patterns
3. **Electron App Won't Start**: Ensure the Flask server is running first
4. **Import Errors**: Make sure all dependencies are installed in your virtual environment

### Logging

The application logs important events and errors. Check the console output for debugging information.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Built with Flask, D3.js, and Electron
- Inspired by visualization best practices and academic research in data visualization
- Uses Bootstrap for responsive UI components

## Future Enhancements

- Machine learning-based suggestion improvements
- Support for more Tableau features (calculated fields, parameters)
- Integration with Tableau Server/Online
- Real-time collaboration features
- Advanced export options (PNG, SVG, PDF)
- Custom visualization templates
