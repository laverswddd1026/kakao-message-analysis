import pandas as pd
import tkinter as tk
from tkinter import filedialog
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt

# ==========================================
# 1. 데이터 불러오기 (탐색기 창 띄우기)
# ==========================================
root = tk.Tk()
root.withdraw() 
file_path = filedialog.askopenfilename(title="분석할 데이터 파일(data.csv)을 선택하세요")

# 파일 선택 안 하고 취소했을 때 멈추게 하기
if not file_path:
    print("파일 선택이 취소되었습니다.")
    root.destroy()
    exit()

# ★ 에러 완벽 방지: 대문자 .CSV도 소문자로 변환해서 확인하고, 
# 만약 엑셀로 넘어갔는데 에러가 나면 강제로 CSV로 다시 읽게 합니다.
if file_path.lower().endswith('.csv'):
    df = pd.read_csv(file_path, encoding='euc-kr')
else:
    try:
        df = pd.read_excel(file_path)
    except ValueError:
        # 확장자가 숨겨져 있어서 엑셀 코드로 빠진 경우, CSV 형식으로 강제 열기
        df = pd.read_csv(file_path, encoding='euc-kr')

root.destroy()  # tkinter 창 정상 종료

print("파일 불러오기 성공!")

# ==========================================
# 2. 데이터 전처리 (빠졌던 부분 추가 완료!)
# ==========================================
# 예측과 무관한 '고객번호' 변수 제거
df = df.drop(columns=['고객번호'])

# 예측 변수(X)와 반응 변수(y) 분리
X = df.drop(columns=['주거지역'])
y = df['주거지역']

# 문자형 변수를 숫자로 변환 (원핫 인코딩)
X = pd.get_dummies(X, drop_first=True)

# ==========================================
# 3. 모델 학습 및 예측
# ==========================================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

model = DecisionTreeClassifier(random_state=42, max_depth=3, min_samples_leaf=5)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("--- 정오 분류표 ---")
print(confusion_matrix(y_test, y_pred))
print(f"예측 적중률: {accuracy * 100:.2f}%\n")

# ==========================================
# 4. 모델 시각화
# ==========================================
plt.rc('font', family='AppleGothic') 
plt.rcParams['axes.unicode_minus'] = False 

plt.figure(figsize=(15, 10)) 

plot_tree(model, 
          feature_names=X.columns, 
          class_names=model.classes_, 
          filled=True,   
          rounded=True,  
          fontsize=10)   

plt.show()