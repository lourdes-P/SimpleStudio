class CodeCellComponent extends HTMLElement {
    constructor() {
        super();
        this.shadow = this.attachShadow({ mode: 'open' });
    }
    // Define observed attributes for reactive updates
    static get observedAttributes() {
        return ['pc', 'label', 'address', 'instruction', 'current'];
    }
    // Called when attributes change
    attributeChangedCallback(name, oldValue, newValue) {
        if (oldValue !== newValue) {
            this.render();
        }
    }
    // Set data via properties
    set cell(data) {
        var _a, _b;
        this.setAttribute('pc', ((_a = data.pc) === null || _a === void 0 ? void 0 : _a.toString()) || '');
        this.setAttribute('label', data.label || '');
        this.setAttribute('address', ((_b = data.address) === null || _b === void 0 ? void 0 : _b.toString()) || '');
        this.setAttribute('instruction', data.instruction || '');
        this.setAttribute('annotation', data.annotation || '');
        this.toggleAttribute('current', !!data.isCurrent);
        this.render();
    }
    render() {
        const pc = this.getAttribute('pc');
        const label = this.getAttribute('label');
        const address = this.getAttribute('address');
        const instruction = this.getAttribute('instruction');
        const annotation = this.getAttribute('annotation');
        const isCurrent = this.hasAttribute('current');
        this.shadow.innerHTML = `
            <link rel="stylesheet" href="/css/input.css">
            <table class="table-fixed w-full">
                <tr class="${isCurrent ? 'bg-cyan-100' : ''}">
                    <td class="px-4 py-2 border-b font-mono">${pc || ''}</td>
                    <td class="px-4 py-2 border-b font-mono">${label || ''}</td>
                    <td class="px-4 py-2 border-b font-mono">${address || ''}</td>
                    <td class="px-4 py-2 border-b font-mono">${instruction || ''}</td>
                    <td class="px-4 py-2 border-b font-mono">${annotation || ''}</td>
                </tr>
            </table>
        `;
    }
}
customElements.define('code-cell', CodeCellComponent);
export {};
