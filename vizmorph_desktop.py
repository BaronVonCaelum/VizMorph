#!/usr/bin/env python3
"""
VizMorph Desktop Application
Standalone executable that doesn't require server hosting
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import sys
import os
import json
import threading
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from tableau_parser import TableauParser
    from viz_recommender import VizRecommender
    from viz_generator import VizGenerator
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you're running from the VizMorph directory")
    sys.exit(1)

class VizMorphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VizMorph - Tableau Visualization Suggester")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Initialize components
        self.parser = TableauParser()
        self.recommender = VizRecommender()
        self.generator = VizGenerator()
        
        # Variables
        self.current_workbook_data = None
        self.current_suggestions = []
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface"""
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="VizMorph", font=("Arial", 24, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        subtitle_label = ttk.Label(main_frame, text="Tableau Workbook Visualization Suggester", 
                                 font=("Arial", 12))
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # File selection frame
        file_frame = ttk.LabelFrame(main_frame, text="Select Tableau Workbook", padding="10")
        file_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        # File path entry
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, state="readonly")
        file_entry.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Browse button
        browse_btn = ttk.Button(file_frame, text="Browse...", command=self.browse_file)
        browse_btn.grid(row=0, column=2)
        
        # Analyze button
        self.analyze_btn = ttk.Button(file_frame, text="Analyze Workbook", 
                                    command=self.analyze_workbook, state="disabled")
        self.analyze_btn.grid(row=1, column=0, columnspan=3, pady=(10, 0))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Results notebook (tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Summary tab
        self.summary_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.summary_frame, text="Workbook Summary")
        self.setup_summary_tab()
        
        # Suggestions tab
        self.suggestions_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.suggestions_frame, text="Suggestions")
        self.setup_suggestions_tab()
        
        # Export tab
        self.export_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.export_frame, text="Export")
        self.setup_export_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Select a Tableau workbook to begin")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def setup_summary_tab(self):
        """Set up the workbook summary tab"""
        # Create scrolled text widget for summary
        self.summary_text = scrolledtext.ScrolledText(self.summary_frame, wrap=tk.WORD, 
                                                    height=20, state=tk.DISABLED)
        self.summary_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def setup_suggestions_tab(self):
        """Set up the suggestions tab"""
        # Create frame for suggestions list
        suggestions_main = ttk.Frame(self.suggestions_frame)
        suggestions_main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Suggestions listbox with scrollbar
        list_frame = ttk.Frame(suggestions_main)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Listbox
        self.suggestions_listbox = tk.Listbox(list_frame, height=15)
        self.suggestions_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.suggestions_listbox.bind('<<ListboxSelect>>', self.on_suggestion_select)
        
        # Scrollbar for listbox
        suggestions_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, 
                                            command=self.suggestions_listbox.yview)
        suggestions_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.suggestions_listbox.config(yscrollcommand=suggestions_scrollbar.set)
        
        # Details frame
        details_frame = ttk.LabelFrame(suggestions_main, text="Suggestion Details", padding="10")
        details_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.details_text = scrolledtext.ScrolledText(details_frame, wrap=tk.WORD, 
                                                    height=8, state=tk.DISABLED)
        self.details_text.pack(fill=tk.BOTH, expand=True)
        
    def setup_export_tab(self):
        """Set up the export tab"""
        export_main = ttk.Frame(self.export_frame, padding="10")
        export_main.pack(fill=tk.BOTH, expand=True)
        
        # Export options
        options_frame = ttk.LabelFrame(export_main, text="Export Options", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.export_format = tk.StringVar(value="json")
        
        ttk.Radiobutton(options_frame, text="JSON Configuration", 
                       variable=self.export_format, value="json").pack(anchor=tk.W)
        ttk.Radiobutton(options_frame, text="D3.js Code", 
                       variable=self.export_format, value="d3").pack(anchor=tk.W)
        ttk.Radiobutton(options_frame, text="Vega-Lite Specification", 
                       variable=self.export_format, value="vega-lite").pack(anchor=tk.W)
        
        # Export buttons
        buttons_frame = ttk.Frame(options_frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(buttons_frame, text="Export Selected Suggestion", 
                  command=self.export_selected).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Export All Suggestions", 
                  command=self.export_all).pack(side=tk.LEFT)
        
        # Export preview
        preview_frame = ttk.LabelFrame(export_main, text="Export Preview", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        self.export_text = scrolledtext.ScrolledText(preview_frame, wrap=tk.WORD, 
                                                   state=tk.DISABLED)
        self.export_text.pack(fill=tk.BOTH, expand=True)
        
    def browse_file(self):
        """Open file dialog to select Tableau workbook"""
        filetypes = [
            ("Tableau Workbooks", "*.twb *.twbx"),
            ("Tableau Workbook", "*.twb"),
            ("Tableau Packaged Workbook", "*.twbx"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select Tableau Workbook",
            filetypes=filetypes
        )
        
        if filename:
            self.file_path_var.set(filename)
            self.analyze_btn.config(state="normal")
            self.status_var.set(f"Selected: {os.path.basename(filename)}")
            
    def analyze_workbook(self):
        """Analyze the selected workbook in a separate thread"""
        filepath = self.file_path_var.get()
        if not filepath:
            messagebox.showerror("Error", "Please select a Tableau workbook first")
            return
            
        # Disable UI during analysis
        self.analyze_btn.config(state="disabled")
        self.progress.start()
        self.status_var.set("Analyzing workbook...")
        
        # Run analysis in separate thread to prevent UI freezing
        thread = threading.Thread(target=self._analyze_workbook_thread, args=(filepath,))
        thread.daemon = True
        thread.start()
        
    def _analyze_workbook_thread(self, filepath):
        """Analyze workbook in background thread"""
        try:
            # Parse workbook
            self.current_workbook_data = self.parser.parse_workbook(filepath)
            
            # Generate suggestions
            suggestions = self.recommender.generate_suggestions(self.current_workbook_data)
            self.current_suggestions = suggestions
            
            # Update UI in main thread
            self.root.after(0, self._analysis_complete)
            
        except Exception as e:
            error_msg = f"Error analyzing workbook: {str(e)}"
            self.root.after(0, lambda: self._analysis_error(error_msg))
            
    def _analysis_complete(self):
        """Called when analysis is complete"""
        self.progress.stop()
        self.analyze_btn.config(state="normal")
        
        # Update summary tab
        self._update_summary()
        
        # Update suggestions tab
        self._update_suggestions()
        
        # Switch to suggestions tab
        self.notebook.select(1)
        
        suggestion_count = len(self.current_suggestions)
        self.status_var.set(f"Analysis complete - {suggestion_count} suggestions generated")
        
    def _analysis_error(self, error_msg):
        """Called when analysis encounters an error"""
        self.progress.stop()
        self.analyze_btn.config(state="normal")
        self.status_var.set("Analysis failed")
        messagebox.showerror("Analysis Error", error_msg)
        
    def _update_summary(self):
        """Update the summary tab with workbook information"""
        if not self.current_workbook_data:
            return
            
        summary = self.current_workbook_data['summary']
        worksheets = self.current_workbook_data['worksheets']
        
        summary_text = f"""WORKBOOK SUMMARY
{'='*50}

Name: {summary['name']}
Version: {summary['version']}
Worksheets: {summary['worksheet_count']}
Dashboards: {summary['dashboard_count']}
Stories: {summary['story_count']}

WORKSHEET DETAILS
{'='*50}

"""
        
        for i, worksheet in enumerate(worksheets, 1):
            summary_text += f"""Worksheet {i}: {worksheet['name']}
  Visualization Type: {worksheet['viz_type']}
  Dimensions: {len(worksheet['dimensions'])} ({', '.join(worksheet['dimensions'][:3])})
  Measures: {len(worksheet['measures'])} ({', '.join(worksheet['measures'][:3])})
  Filters: {len(worksheet['filters'])}

"""
        
        self.summary_text.config(state=tk.NORMAL)
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(1.0, summary_text)
        self.summary_text.config(state=tk.DISABLED)
        
    def _update_suggestions(self):
        """Update the suggestions tab with generated suggestions"""
        # Clear existing suggestions
        self.suggestions_listbox.delete(0, tk.END)
        
        # Add suggestions to listbox
        for i, suggestion in enumerate(self.current_suggestions):
            confidence = int(suggestion['confidence'] * 100)
            display_text = f"{suggestion['title']} ({confidence}% confidence)"
            self.suggestions_listbox.insert(tk.END, display_text)
            
    def on_suggestion_select(self, event):
        """Handle suggestion selection"""
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            suggestion = self.current_suggestions[index]
            
            # Update details
            details = f"""SUGGESTION DETAILS
{'='*50}

Title: {suggestion['title']}
Visualization Type: {suggestion['viz_type']}
Confidence: {int(suggestion['confidence'] * 100)}%
Original Worksheet: {suggestion['original_worksheet']}

RATIONALE
{'-'*20}
{suggestion['rationale']}

IMPROVEMENTS
{'-'*20}
"""
            for improvement in suggestion['improvements']:
                details += f"• {improvement}\n"
                
            details += f"""

DATA MAPPING
{'-'*20}
{json.dumps(suggestion['data_mapping'], indent=2)}
"""
            
            self.details_text.config(state=tk.NORMAL)
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(1.0, details)
            self.details_text.config(state=tk.DISABLED)
            
    def export_selected(self):
        """Export the currently selected suggestion"""
        selection = self.suggestions_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a suggestion to export")
            return
            
        index = selection[0]
        suggestion_data = self.current_suggestions[index]
        
        # Create VizSuggestion object for generator
        from viz_recommender import VizSuggestion, VizType
        suggestion = VizSuggestion(
            id=suggestion_data['id'],
            viz_type=VizType(suggestion_data['viz_type']),
            title=suggestion_data['title'],
            description=suggestion_data['description'],
            rationale=suggestion_data['rationale'],
            confidence=suggestion_data['confidence'],
            data_mapping=suggestion_data['data_mapping'],
            original_worksheet=suggestion_data['original_worksheet'],
            improvements=suggestion_data['improvements']
        )
        
        try:
            export_data = self.generator.export_visualization(suggestion, self.export_format.get())
            
            # Show preview
            preview_text = json.dumps(export_data, indent=2)
            self.export_text.config(state=tk.NORMAL)
            self.export_text.delete(1.0, tk.END)
            self.export_text.insert(1.0, preview_text)
            self.export_text.config(state=tk.DISABLED)
            
            # Save to file
            self._save_export_file(export_data, suggestion_data['title'])
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {str(e)}")
            
    def export_all(self):
        """Export all suggestions"""
        if not self.current_suggestions:
            messagebox.showwarning("No Suggestions", "No suggestions to export")
            return
            
        try:
            all_exports = []
            
            for suggestion_data in self.current_suggestions:
                # Create VizSuggestion object
                from viz_recommender import VizSuggestion, VizType
                suggestion = VizSuggestion(
                    id=suggestion_data['id'],
                    viz_type=VizType(suggestion_data['viz_type']),
                    title=suggestion_data['title'],
                    description=suggestion_data['description'],
                    rationale=suggestion_data['rationale'],
                    confidence=suggestion_data['confidence'],
                    data_mapping=suggestion_data['data_mapping'],
                    original_worksheet=suggestion_data['original_worksheet'],
                    improvements=suggestion_data['improvements']
                )
                
                export_data = self.generator.export_visualization(suggestion, self.export_format.get())
                all_exports.append(export_data)
            
            # Save all exports
            self._save_export_file(all_exports, "all_suggestions")
            
            # Show summary in preview
            summary = f"Exported {len(all_exports)} suggestions in {self.export_format.get().upper()} format"
            self.export_text.config(state=tk.NORMAL)
            self.export_text.delete(1.0, tk.END)
            self.export_text.insert(1.0, summary)
            self.export_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export all: {str(e)}")
            
    def _save_export_file(self, data, title):
        """Save export data to file"""
        format_ext = {
            'json': '.json',
            'd3': '.html',
            'vega-lite': '.json'
        }
        
        ext = format_ext.get(self.export_format.get(), '.json')
        filename = filedialog.asksaveasfilename(
            title="Save Export",
            defaultextension=ext,
            filetypes=[(f"{self.export_format.get().upper()} files", f"*{ext}"), ("All files", "*.*")],
            initialname=f"{title.replace(' ', '_')}{ext}"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    if self.export_format.get() == 'd3' and 'html' in data:
                        f.write(data['html'])
                    else:
                        json.dump(data, f, indent=2)
                
                messagebox.showinfo("Export Complete", f"Exported to: {filename}")
                
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save file: {str(e)}")

def main():
    """Main application entry point"""
    root = tk.Tk()
    
    # Set application icon (if available)
    try:
        # You can add an icon file here
        # root.iconbitmap('vizmorph_icon.ico')
        pass
    except:
        pass
    
    app = VizMorphApp(root)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
