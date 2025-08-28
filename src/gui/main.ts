import { CodeCell } from './types/codecell.js';
import './components/CodeMemory.js'
import './components/CodeCell.js'
declare const eel: any;
// Expose function to Python
eel.expose(updateCodeMemory);

function updateCodeMemory(cells: CodeCell[]) {
    const code_memory = document.querySelector('code-memory') as any;
    if (code_memory) {
        code_memory.cells = cells;
    }
}

// Initialize the app
async function initApp() {
    try {
        eel.get_initial_code_memory()(updateCodeMemory);
    } catch (error) {
        console.error('Error initializing app:', error);
    }
}

// Start the app when DOM is loaded
document.addEventListener('DOMContentLoaded', initApp);