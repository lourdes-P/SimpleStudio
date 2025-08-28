import { CodeCell, CodeCellElement } from "../types/codecell";
import { CodeCellComponent } from './CodeCell'

class CodeMemory extends HTMLElement {
    private shadow: ShadowRoot;
    
    constructor() {
        super();
        this.shadow = this.attachShadow({ mode: 'open' });
        this.render([]);
    }

    set cells(cells: CodeCell[]) {
        this.render(cells);
    }

    private render(cells: CodeCell[]) {
        this.shadow.innerHTML = `
            <style>
                :host {
                    display: block;
                    margin: 1rem 0;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                thead {
                    background-color: #f8fafc;
                }
                th {
                    padding: 0.75rem 1rem;
                    text-align: left;
                    font-weight: 500;
                    text-transform: uppercase;
                    font-size: 0.75rem;
                    letter-spacing: 0.05em;
                }
            </style>
            <table>
                <thead>
                    <tr>
                        <th>PC</th>
                        <th>Label</th>
                        <th>Line</th>
                        <th>Instruction</th>
                        <th>Annotation</th>
                    </tr>
                </thead>
                <tbody id="cells-container"></tbody>
            </table>
        `;

        const container = this.shadow.getElementById('cells-container');
        if (container) {
            cells.forEach(cell => {
                const cellElement = document.createElement('code-cell') as CodeCellComponent;
                cellElement.cell = cell;
                container.appendChild(cellElement);
            });
        }
    }
}

customElements.define('code-memory', CodeMemory);

export type { CodeMemory };