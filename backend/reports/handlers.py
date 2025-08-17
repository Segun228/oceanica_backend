import pandas as pd
from django.http import HttpResponse
from io import BytesIO
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment, Font

def get_xlsx_report(posts, categories):
    post_df = pd.DataFrame(posts)[["category_id", "title", "description", "price", "weight", "country"]]
    cat_df = pd.DataFrame(categories)[["id", "name", "description"]]

    result = pd.merge(
        left=post_df,
        right=cat_df,
        left_on="category_id",
        right_on="id",
        how="inner"
    )

    buffer = BytesIO()

    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        result.to_excel(
            writer,
            index=False,
            sheet_name="Текущие посты"
        )

        workbook = writer.book
        worksheet = writer.sheets["Текущие посты"]

        header_font = Font(bold=True)
        for col_num, column_title in enumerate(result.columns, 1):
            cell = worksheet.cell(row=1, column=col_num)
            cell.font = header_font
            cell.alignment = Alignment(horizontal='center', vertical='center')

        for column_cells in worksheet.columns:
            length = max(len(str(cell.value)) if cell.value else 0 for cell in column_cells)
            col_letter = get_column_letter(column_cells[0].column)
            worksheet.column_dimensions[col_letter].width = length + 4

    buffer.seek(0)

    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=products.xlsx'
    return response