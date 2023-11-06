import streamlit as st
import pandas as pd

# カスタムカウント関数の定義
def custom_count(value):
    # 文字列を確実に処理するためにstr型に変換
    str_value = str(value)
    
    # カンマ区切りのデータを分割して、空白を削除
    items = [item.strip() for item in str_value.split(',') if item.strip() != '']
    
    # 特殊アイテムと通常のアイテムの合計数を計算
    # 特殊アイテムの場合は2個分、それ以外は1個分としてカウント
    total_count = 0
    for item in items:
        if item == 'P' or item == 'Z' or item == '*CL':
            total_count += 2
        else:
            total_count += 1
    
    # 5個を超える分のみ追加ポイントとして計算
    additional_points = max(total_count - 5, 0)
    
    return additional_points






# Streamlitアプリのタイトルを設定
st.title('Excelデータの集計')

# ファイルアップロードのウィジェット
uploaded_file = st.file_uploader("Excelファイルをアップロードしてください", type=['xlsx'])

# アップロードされたファイルがあるかどうかを確認
if uploaded_file is not None:
    # Excelファイルを読み込む（ヘッダーが最初の行にあると仮定）
    df = pd.read_excel(uploaded_file)

    # 列名が正しいかどうかを確認（'同梱物'という名前の列が存在するか）
    if '同梱物' not in df.columns:
        st.error("エクセルの'I'列に相当するヘッダー名が'同梱物'ではありません。ファイルを確認してください。")
    else:
        # '同梱物'列に対してカスタム集計関数を適用
        df['Additional Points'] = df['同梱物'].apply(custom_count)
        
        # 結果の集計
        total_points = df['Additional Points'].sum()

        # 集計結果を表示
        st.write(f'総追加ポイント数: {total_points}')
        st.dataframe(df)  # データフレームを表示
