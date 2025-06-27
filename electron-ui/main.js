const { app, BrowserWindow, Menu, dialog, ipcMain } = require('electron');
const path = require('path');
const axios = require('axios');

// Keep a global reference of the window object
let mainWindow;

// API base URL (adjust if Flask runs on different port/host)
const API_BASE_URL = 'http://localhost:5000';

function createWindow() {
    // Create the browser window
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            enableRemoteModule: true
        },
        icon: path.join(__dirname, 'assets', 'icon.png'), // Add icon if available
        title: 'VizMorph - Tableau Visualization Suggester'
    });

    // Load the index.html of the app
    mainWindow.loadFile('index.html');

    // Open DevTools in development
    if (process.env.NODE_ENV === 'development') {
        mainWindow.webContents.openDevTools();
    }

    // Emitted when the window is closed
    mainWindow.on('closed', () => {
        mainWindow = null;
    });

    // Create application menu
    createMenu();
}

function createMenu() {
    const template = [
        {
            label: 'File',
            submenu: [
                {
                    label: 'Open Tableau Workbook',
                    accelerator: 'CmdOrCtrl+O',
                    click: () => {
                        openWorkbookDialog();
                    }
                },
                { type: 'separator' },
                {
                    label: 'Exit',
                    accelerator: process.platform === 'darwin' ? 'Cmd+Q' : 'Ctrl+Q',
                    click: () => {
                        app.quit();
                    }
                }
            ]
        },
        {
            label: 'View',
            submenu: [
                { role: 'reload' },
                { role: 'forceReload' },
                { role: 'toggleDevTools' },
                { type: 'separator' },
                { role: 'resetZoom' },
                { role: 'zoomIn' },
                { role: 'zoomOut' },
                { type: 'separator' },
                { role: 'togglefullscreen' }
            ]
        },
        {
            label: 'Window',
            submenu: [
                { role: 'minimize' },
                { role: 'close' }
            ]
        },
        {
            label: 'Help',
            submenu: [
                {
                    label: 'About VizMorph',
                    click: () => {
                        dialog.showMessageBox(mainWindow, {
                            type: 'info',
                            title: 'About VizMorph',
                            message: 'VizMorph v1.0.0',
                            detail: 'A Tableau workbook visualization suggestion engine powered by heuristics and D3.js previews.'
                        });
                    }
                }
            ]
        }
    ];

    const menu = Menu.buildFromTemplate(template);
    Menu.setApplicationMenu(menu);
}

async function openWorkbookDialog() {
    const result = await dialog.showOpenDialog(mainWindow, {
        properties: ['openFile'],
        filters: [
            { name: 'Tableau Workbooks', extensions: ['twb', 'twbx'] },
            { name: 'All Files', extensions: ['*'] }
        ]
    });

    if (!result.canceled && result.filePaths.length > 0) {
        const filePath = result.filePaths[0];
        mainWindow.webContents.send('file-selected', filePath);
    }
}

// IPC handlers for communication with renderer process
ipcMain.handle('upload-workbook', async (event, filePath) => {
    try {
        const FormData = require('form-data');
        const fs = require('fs');
        
        const form = new FormData();
        form.append('file', fs.createReadStream(filePath));

        const response = await axios.post(`${API_BASE_URL}/api/upload`, form, {
            headers: {
                ...form.getHeaders()
            }
        });

        return response.data;
    } catch (error) {
        console.error('Upload error:', error);
        throw new Error(`Upload failed: ${error.message}`);
    }
});

ipcMain.handle('get-suggestions', async (event, workbookId) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/api/suggest/${workbookId}`);
        return response.data;
    } catch (error) {
        console.error('Suggestions error:', error);
        throw new Error(`Failed to get suggestions: ${error.message}`);
    }
});

ipcMain.handle('preview-visualization', async (event, suggestionId) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/api/preview/${suggestionId}`);
        return response.data;
    } catch (error) {
        console.error('Preview error:', error);
        throw new Error(`Failed to get preview: ${error.message}`);
    }
});

ipcMain.handle('export-visualization', async (event, suggestionId, format) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/api/export/${suggestionId}`, {
            params: { format }
        });
        return response.data;
    } catch (error) {
        console.error('Export error:', error);
        throw new Error(`Failed to export: ${error.message}`);
    }
});

// App event handlers
app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (mainWindow === null) {
        createWindow();
    }
});

// Prevent navigation to external URLs
app.on('web-contents-created', (event, contents) => {
    contents.on('new-window', (event, navigationUrl) => {
        event.preventDefault();
    });
});

// Security: Prevent navigation to external sites
app.on('ready', () => {
    if (mainWindow) {
        mainWindow.webContents.on('will-navigate', (event, url) => {
            if (url !== mainWindow.webContents.getURL()) {
                event.preventDefault();
            }
        });
    }
});
