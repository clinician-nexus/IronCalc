# Regrettably at the time of writing there is not a perfect way to
# generate the TypeScript types from Rust so we basically fix them manually
# Hopefully this will suffice for our needs and one day will be automatic

header = r"""
/* tslint:disable */
/* eslint-disable */
""".strip()

# wasm-bindgen emits `any` for everything that crosses the boundary as a JS
# value, so we replace each of those signatures with the real types.
SIGNATURES = [
    (
        "export function getTokens(formula: string): any;",
        "export function getTokens(formula: string): MarkedToken[];",
    ),
    (
        "updateRangeStyle(range: any, style_path: string, value: string): void;",
        "updateRangeStyle(range: Area, style_path: string, value: string): void;",
    ),
    (
        "getWorksheetsProperties(): any;",
        "getWorksheetsProperties(): WorksheetProperties[];",
    ),
    (
        "getCellStyle(sheet: number, row: number, column: number): any;",
        "getCellStyle(sheet: number, row: number, column: number): CellStyle;",
    ),
    (
        "getSelectedView(): any;",
        "getSelectedView(): SelectedView;",
    ),
    (
        "autoFillRows(source_area: any, to_row: number): void;",
        "autoFillRows(source_area: Area, to_row: number): void;",
    ),
    (
        "autoFillColumns(source_area: any, to_column: number): void;",
        "autoFillColumns(source_area: Area, to_column: number): void;",
    ),
    (
        "onPasteStyles(styles: any): void;",
        "onPasteStyles(styles: CellStyle[][]): void;",
    ),
    (
        "setAreaWithBorder(area: any, border_area: any): void;",
        "setAreaWithBorder(area: Area, border_area: BorderArea): void;",
    ),
    (
        "pasteCsvText(area: any, csv: string): void;",
        "pasteCsvText(area: Area, csv: string): void;",
    ),
    (
        "copyToClipboard(): any;",
        "copyToClipboard(): Clipboard;",
    ),
    (
        "pasteFromClipboard(source_sheet: number, source_range: any, clipboard: any, is_cut: boolean): void;",
        "pasteFromClipboard(source_sheet: number, source_range: [number, number, number, number], clipboard: ClipboardData, is_cut: boolean): void;",
    ),
    (
        "getDefinedNameList(): any;",
        "getDefinedNameList(): DefinedName[];",
    ),
]

# Everything after this marker is the raw wasm interface, where `any` is expected
RAW_INTERFACE_MARKER = "export type InitInput"


def fix_types(text):
    for old, new in SIGNATURES:
        if old not in text:
            print("Could not find the signature '{}'. Please check.".format(old))
            exit(1)
        text = text.replace(old, new)
    with open("types.ts") as f:
        types_str = f.read()
        header_types = "{}\n\n{}".format(header, types_str)
    text = text.replace(header, header_types)
    public_api = text.split(RAW_INTERFACE_MARKER)[0]
    if public_api.find("any") != -1:
        print("There are 'unfixed' types. Please check.")
        exit(1)
    return text


if __name__ == "__main__":
    types_file = "pkg/wasm.d.ts"
    with open(types_file) as f:
        text = f.read()
    text = fix_types(text)
    with open(types_file, "wb") as f:
        f.write(bytes(text, "utf8"))

    js_file = "pkg/wasm.js"
    with open("types.js") as f:
        text_js = f.read()
    with open(js_file) as f:
        text = f.read()

    with open(js_file, "wb") as f:
        f.write(bytes("{}\n{}".format(text_js, text), "utf8"))
    

    
