// Type definitions for the eel.js browser interface
import { CodeCell } from './codecell'

interface Eel {
    expose(fn: (...args: any[]) => void): void;
    get_initial_code_memory(): (callback: (cells: CodeCell[]) => void) => void;
    update_status(message: string): void;
    
    // Add other Eel functions you use from Python here
    // Example:
    // some_python_function(): (callback: (result: SomeType) => void) => void;
}

// Declare the global eel variable
declare const eel: Eel;