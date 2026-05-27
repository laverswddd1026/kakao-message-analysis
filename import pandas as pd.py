import pandas as pd
import glob
import os

# 1. 엑셀 파일들이 있는 폴더 경로 지정 및 파일 목록 가져오기
folder_path = './dealer_reports/'
file_list = glob.glob(os.path.join(folder_path, '*.xlsx'))

# 2. 모든 엑셀 파일을 읽어서 리스트에 담기
all_data = []
for file in file_list:
    df = pd.read_excel(file)
    # 어느 파일에서 온 데이터인지 출처 기록 (선택 사항)
    df['출처파일명'] = os.path.basename(file) 
    all_data.append(df)

# 3. 하나의 데이터프레임으로 합치기
master_df = pd.concat(all_data, ignore_index=True)

# 4. 결측치 처리 (예: 발송건수가 빈칸이면 0으로 채우기)
master_df['발송건수'] = master_df['발송건수'].fillna(0)

# 5. 취합된 결과를 새로운 엑셀로 저장
master_df.to_excel('master_report_updated.xlsx', index=False)