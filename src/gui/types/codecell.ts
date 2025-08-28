export interface CodeCell {
    pc?: number;
    label?: string;
    address: number;
    instruction: string;
    annotation?: string;
    isCurrent?: boolean;
}

export interface CodeCellElement extends HTMLElement {
    cell: CodeCell;
}