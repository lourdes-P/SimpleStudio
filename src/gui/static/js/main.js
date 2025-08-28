var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import './components/CodeMemory.js';
import './components/CodeCell.js';
// Expose function to Python
eel.expose(updateCodeMemory);
function updateCodeMemory(cells) {
    const code_memory = document.querySelector('code-memory');
    if (code_memory) {
        code_memory.cells = cells;
    }
}
// Initialize the app
function initApp() {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            eel.get_initial_code_memory()(updateCodeMemory);
        }
        catch (error) {
            console.error('Error initializing app:', error);
        }
    });
}
// Start the app when DOM is loaded
document.addEventListener('DOMContentLoaded', initApp);
