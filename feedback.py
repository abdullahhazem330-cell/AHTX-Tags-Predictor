import pandas as pd
import os

def add_new_problem(new_text, new_tag):
    # 1. مسار ملف الـ CSV
    file_path = 'problems_dataset.csv'
    
    # 2. تجهيز البيانات الجديدة في شكل ديجيت أو قاموس
    new_data = pd.DataFrame({
        'problem_text': [new_text],
        'tag': [new_tag]
    })
    
    # 3. لو الملف موجود، بنقراه ونحط عليه الداتا الجديدة من غير ما نمسح القديم (append)
    if os.path.exists(file_path):
        # mode='a' تعني إضافة للنهاية (Append)، و header=False عشان ما يكتبش أسماء الأعمدة تاني
        new_data.to_csv(file_path, mode='a', index=False, header=False)
        print("تم إضافة المسألة الجديدة لملف الداتا بنجاح! 📈")
    else:
        # لو لأي سبب الملف مش موجود، بنعمله من أول وجديد
        new_data.to_csv(file_path, index=False, header=True)
        print("تم إنشاء ملف داتا جديد وإضافة المسألة! 📂")

# تجربة عملية لإضافة مسألة جديدة
if __name__ == "__main__":
    sample_text = "Find the strongly connected components in a directed graph using Tarjan algorithm."
    sample_tag = "Graphs"
    
    add_new_problem(sample_text, sample_tag)