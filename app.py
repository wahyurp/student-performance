import joblib
import numpy as np
import pandas as pd
import streamlit as st
import json

import os
import warnings

warnings.filterwarnings("ignore")

model_folder = "model"


marital_status_dict = {
    1: "Single",
    2: "Married",
    3: "Widower",
    4: "Facto Union",
    5: "Legally Separated"
}

application_mode_dict = {
    1: "1st phase - general contingent",
    2: "Ordinance No. 612/93",
    5: "1st phase - special contingent (Azores Island)",
    7: "Holders of other higher courses",
    10: "Ordinance No. 854-B/99",
    15: "International student (bachelor)",
    16: "1st phase - special contingent (Madeira Island)",
    17: "2nd phase - general contingent",
    18: "3rd phase - general contingent",
    26: "Ordinance No. 533-A/99, item b2) (Different Plan)",
    27: "Ordinance No. 533-A/99, item b3 (Other Institution)",
    39: "Over 23 years old",
    42: "Transfer",
    43: "Change of course",
    44: "Technological specialization diploma holders",
    51: "Change of institution/course",
    53: "Short cycle diploma holders",
    57: "Change of institution/course (International)"
}

course_dict = {
    33: "Biofuel Production Technologies",
    171: "Animation and Multimedia Design",
    8014: "Social Service (evening attendance)",
    9003: "Agronomy",
    9070: "Communication Design",
    9085: "Veterinary Nursing",
    9119: "Informatics Engineering",
    9130: "Equinculture",
    9147: "Management",
    9238: "Social Service",
    9254: "Tourism",
    9500: "Nursing",
    9556: "Oral Hygiene",
    9670: "Advertising and Marketing Management",
    9773: "Journalism and Communication",
    9853: "Basic Education",
    9991: "Management (evening attendance)"
}

previous_qualification_dict = {
    1: "Secondary education",
    2: "Higher education - bachelor's degree",
    3: "Higher education - degree",
    4: "Higher education - master's",
    5: "Higher education - doctorate",
    6: "Frequency of higher education",
    9: "12th year of schooling - not completed",
    10: "11th year of schooling - not completed",
    12: "Other - 11th year of schooling",
    14: "10th year of schooling",
    15: "10th year of schooling - not completed",
    19: "Basic education 3rd cycle (9th/10th/11th year) or equiv.",
    38: "Basic education 2nd cycle (6th/7th/8th year) or equiv.",
    39: "Technological specialization course",
    40: "Higher education - degree (1st cycle)",
    42: "Professional higher technical course",
    43: "Higher education - master (2nd cycle)"
}


nacionality_dict = {
    1: "Portuguese",
    2: "German",
    6: "Spanish",
    11: "Italian",
    13: "Dutch",
    14: "English",
    17: "Lithuanian",
    21: "Angolan",
    22: "Cape Verdean",
    24: "Guinean",
    25: "Mozambican",
    26: "Santomean",
    32: "Turkish",
    41: "Brazilian",
    62: "Romanian",
    100: "Moldova (Republic of)",
    101: "Mexican",
    103: "Ukrainian",
    105: "Russian",
    108: "Cuban",
    109: "Colombian"
}

mothers_qualification_dict = {
    1: "Secondary Education - 12th Year of Schooling or Eq.",
    2: "Higher Education - Bachelor's Degree",
    3: "Higher Education - Degree",
    4: "Higher Education - Master's",
    5: "Higher Education - Doctorate",
    6: "Frequency of Higher Education",
    9: "12th Year of Schooling - Not Completed",
    10: "11th Year of Schooling - Not Completed",
    11: "7th Year (Old)",
    12: "Other - 11th Year of Schooling",
    14: "10th Year of Schooling",
    18: "General commerce course",
    19: "Basic Education 3rd Cycle (9th/10th/11th Year) or Equiv.",
    22: "Technical-professional course",
    26: "7th year of schooling",
    27: "2nd cycle of the general high school course",
    29: "9th Year of Schooling - Not Completed",
    30: "8th year of schooling",
    34: "Unknown",
    35: "Can't read or write",
    36: "Can read without having a 4th year of schooling",
    37: "Basic education 1st cycle (4th/5th year) or equiv.",
    38: "Basic Education 2nd Cycle (6th/7th/8th Year) or Equiv.",
    39: "Technological specialization course",
    40: "Higher education - degree (1st cycle)",
    41: "Specialized higher studies course",
    42: "Professional higher technical course",
    43: "Higher Education - Master (2nd cycle)",
    44: "Higher Education - Doctorate (3rd cycle)"
}


fathers_qualification_dict = {
    1: "Secondary Education - 12th Year of Schooling or Eq.",
    2: "Higher Education - Bachelor's Degree",
    3: "Higher Education - Degree",
    4: "Higher Education - Master's",
    5: "Higher Education - Doctorate",
    6: "Frequency of Higher Education",
    9: "12th Year of Schooling - Not Completed",
    10: "11th Year of Schooling - Not Completed",
    11: "7th Year (Old)",
    12: "Other - 11th Year of Schooling",
    13: "2nd Year Complementary High School Course",
    14: "10th Year of Schooling",
    18: "General Commerce Course",
    19: "Basic Education 3rd Cycle (9th/10th/11th Year) or Equiv.",
    20: "Complementary High School Course",
    22: "Technical-Professional Course",
    25: "Complementary High School Course - Not Concluded",
    26: "7th Year of Schooling",
    27: "2nd Cycle of the General High School Course",
    29: "9th Year of Schooling - Not Completed",
    30: "8th Year of Schooling",
    31: "General Course of Administration and Commerce",
    33: "Supplementary Accounting and Administration",
    34: "Unknown",
    35: "Can't Read or Write",
    36: "Can Read Without Having a 4th Year of Schooling",
    37: "Basic Education 1st Cycle (4th/5th Year) or Equiv.",
    38: "Basic Education 2nd Cycle (6th/7th/8th Year) or Equiv.",
    39: "Technological Specialization Course",
    40: "Higher Education - Degree (1st Cycle)",
    41: "Specialized Higher Studies Course",
    42: "Professional Higher Technical Course",
    43: "Higher Education - Master (2nd Cycle)",
    44: "Higher Education - Doctorate (3rd Cycle)"
}

mothers_occupation_dict = {
    0: "Student",
    1: "Representatives of the Legislative Power and Executive Bodies, Directors, Directors and Executive Managers",
    2: "Specialists in Intellectual and Scientific Activities",
    3: "Intermediate Level Technicians and Professions",
    4: "Administrative staff",
    5: "Personal Services, Security and Safety Workers and Sellers",
    6: "Farmers and Skilled Workers in Agriculture, Fisheries and Forestry",
    7: "Skilled Workers in Industry, Construction and Craftsmen",
    8: "Installation and Machine Operators and Assembly Workers",
    9: "Unskilled Workers",
    10: "Armed Forces Professions",
    90: "Other Situation",
    99: "(blank)",
    122: "Health professionals",
    123: "Teachers",
    125: "Specialists in information and communication technologies (ICT)",
    131: "Intermediate level science and engineering technicians and professions",
    132: "Technicians and professionals, of intermediate level of health",
    134: "Intermediate level technicians from legal, social, sports, cultural and similar services",
    141: "Office workers, secretaries in general and data processing operators",
    143: "Data, accounting, statistical, financial services and registry-related operators",
    144: "Other administrative support staff",
    151: "Personal service workers",
    152: "Sellers",
    153: "Personal care workers and the like",
    171: "Skilled construction workers and the like, except electricians",
    173: "Skilled workers in printing, precision instrument manufacturing, jewelers, artisans and the like",
    175: "Workers in food processing, woodworking, clothing and other industries and crafts",
    191: "Cleaning workers",
    192: "Unskilled workers in agriculture, animal production, fisheries and forestry",
    193: "Unskilled workers in extractive industry, construction, manufacturing and transport",
    194: "Meal preparation assistants"
}

fathers_occupation_dict = {
    0: "Student",
    1: "Representatives of the Legislative Power and Executive Bodies, Directors, Directors and Executive Managers",
    2: "Specialists in Intellectual and Scientific Activities",
    3: "Intermediate Level Technicians and Professions",
    4: "Administrative staff",
    5: "Personal Services, Security and Safety Workers and Sellers",
    6: "Farmers and Skilled Workers in Agriculture, Fisheries and Forestry",
    7: "Skilled Workers in Industry, Construction and Craftsmen",
    8: "Installation and Machine Operators and Assembly Workers",
    9: "Unskilled Workers",
    10: "Armed Forces Professions",
    90: "Other Situation",
    99: "(blank)",
    101: "Armed Forces Officers",
    102: "Armed Forces Sergeants",
    103: "Other Armed Forces personnel",
    112: "Directors of administrative and commercial services",
    114: "Hotel, catering, trade and other services directors",
    121: "Specialists in the physical sciences, mathematics, engineering and related techniques",
    122: "Health professionals",
    123: "Teachers",
    124: "Specialists in finance, accounting, administrative organization, public and commercial relations",
    131: "Intermediate level science and engineering technicians and professions",
    132: "Technicians and professionals, of intermediate level of health",
    134: "Intermediate level technicians from legal, social, sports, cultural and similar services",
    135: "Information and communication technology technicians",
    141: "Office workers, secretaries in general and data processing operators",
    143: "Data, accounting, statistical, financial services and registry-related operators",
    144: "Other administrative support staff",
    151: "Personal service workers",
    152: "Sellers",
    153: "Personal care workers and the like",
    154: "Protection and security services personnel",
    161: "Market-oriented farmers and skilled agricultural and animal production workers",
    163: "Farmers, livestock keepers, fishermen, hunters and gatherers, subsistence",
    171: "Skilled construction workers and the like, except electricians",
    172: "Skilled workers in metallurgy, metalworking and similar",
    174: "Skilled workers in electricity and electronics",
    175: "Workers in food processing, woodworking, clothing and other industries and crafts",
    181: "Fixed plant and machine operators",
    182: "Assembly workers",
    183: "Vehicle drivers and mobile equipment operators",
    192: "Unskilled workers in agriculture, animal production, fisheries and forestry",
    193: "Unskilled workers in extractive industry, construction, manufacturing and transport",
    194: "Meal preparation assistants",
    195: "Street vendors (except food) and street service providers"
}

y_n_dict = {
    0: "No",
    1: "Yes"
}

gender_dict = {
    1: "Male",
    0: "Female"
}


pca_numerical_columns_1 = [
    'Previous_qualification_grade',
    'Admission_grade',
    'Age_at_enrollment',
    'Unemployment_rate',
    'Inflation_rate',
    'GDP'
]

pca_numerical_columns_2 =[
    'Curricular_units_1st_sem_credited',
    'Curricular_units_1st_sem_enrolled',
    'Curricular_units_1st_sem_evaluations',
    'Curricular_units_1st_sem_approved',
    'Curricular_units_1st_sem_grade',
    'Curricular_units_1st_sem_without_evaluations',
    'Curricular_units_2nd_sem_credited',
    'Curricular_units_2nd_sem_enrolled',
    'Curricular_units_2nd_sem_evaluations',
    'Curricular_units_2nd_sem_approved',
    'Curricular_units_2nd_sem_grade',
    'Curricular_units_2nd_sem_without_evaluations'
]

for filename in os.listdir(model_folder):
    if filename.endswith(".joblib"): 
        var_name = filename.replace(".joblib", "").replace(" ", "_")
        
        globals()[var_name] = joblib.load(os.path.join(model_folder, filename))
        print(f"Model {var_name} berhasil dimuat!")


def data_preprocessing(data):
    """Preprocessing data with safe handling for unknown categories"""
    data = data.copy()
    df = pd.DataFrame()
    
    # Handle numerical features with scalers
    numerical_features = {
        "Admission_grade": scaler_Admission_grade,
        "Age_at_enrollment": scaler_Age_at_enrollment,
        "GDP": scaler_GDP,
        "Inflation_rate": scaler_Inflation_rate,
        "Previous_qualification_grade": scaler_Previous_qualification_grade,
        "Unemployment_rate": scaler_Unemployment_rate,
        "Curricular_units_1st_sem_approved": scaler_Curricular_units_1st_sem_approved,
        "Curricular_units_1st_sem_credited": scaler_Curricular_units_1st_sem_credited,
        "Curricular_units_1st_sem_enrolled": scaler_Curricular_units_1st_sem_enrolled,
        "Curricular_units_1st_sem_evaluations": scaler_Curricular_units_1st_sem_evaluations,
        "Curricular_units_1st_sem_grade": scaler_Curricular_units_1st_sem_grade,
        "Curricular_units_1st_sem_without_evaluations": scaler_Curricular_units_1st_sem_without_evaluations,
        "Curricular_units_2nd_sem_approved": scaler_Curricular_units_2nd_sem_approved,
        "Curricular_units_2nd_sem_credited": scaler_Curricular_units_2nd_sem_credited,
        "Curricular_units_2nd_sem_enrolled": scaler_Curricular_units_2nd_sem_enrolled,
        "Curricular_units_2nd_sem_evaluations": scaler_Curricular_units_2nd_sem_evaluations,
        "Curricular_units_2nd_sem_grade": scaler_Curricular_units_2nd_sem_grade,
        "Curricular_units_2nd_sem_without_evaluations": scaler_Curricular_units_2nd_sem_without_evaluations
    }
    
    for feature, scaler in numerical_features.items():
        df[feature] = scaler.transform(np.asarray(data[feature]).reshape(-1, 1))[:, 0]
    
    categorical_encoders = {
        "Application_mode": encoder_Application_mode,
        "Application_order": encoder_Application_order,
        "Course": encoder_Course,
        "Debtor": encoder_Debtor,
        "Displaced": encoder_Displaced,
        "Fathers_occupation": encoder_Fathers_occupation,
        "Fathers_qualification": encoder_Fathers_qualification,
        "Gender": encoder_Gender,
        "Marital_status": encoder_Marital_status,
        "Mothers_occupation": encoder_Mothers_occupation,
        "Mothers_qualification": encoder_Mothers_qualification,
        "Nacionality": encoder_Nacionality,
        "Previous_qualification": encoder_Previous_qualification,
        "Scholarship_holder": encoder_Scholarship_holder,
        "Tuition_fees_up_to_date": encoder_Tuition_fees_up_to_date
    }
    
    for feature, encoder in categorical_encoders.items():
        known_categories = set(encoder.classes_)
        default_value = encoder.classes_[0]  # handle unseen data
        data[feature] = data[feature].apply(lambda x: x if x in known_categories else default_value)
        #transform
        df[feature] = encoder.transform(data[feature])
    
    # PCA transformations
    df[["pc1_1", "pc1_2", "pc1_3", "pc1_4"]] = pca_1.transform(data[pca_numerical_columns_1])
    df[["pc2_1", "pc2_2", "pc2_3", "pc2_4", "pc2_5", "pc2_6", "pc2_7", "pc2_8"]] = pca_2.transform(data[pca_numerical_columns_2])
    final_res = df.drop(columns=pca_numerical_columns_1 + pca_numerical_columns_2)
    correct_order = ['Marital_status', 'Application_mode', 'Application_order', 'Course',
       'Previous_qualification', 'Nacionality', 'Mothers_qualification',
       'Fathers_qualification', 'Mothers_occupation', 'Fathers_occupation',
       'Displaced', 'Debtor', 'Tuition_fees_up_to_date', 'Gender',
       'Scholarship_holder', 'pc1_1', 'pc1_2', 'pc1_3', 'pc1_4', 'pc2_1',
       'pc2_2', 'pc2_3', 'pc2_4', 'pc2_5', 'pc2_6', 'pc2_7', 'pc2_8']
    final_res = final_res[correct_order]
    return final_res


# def data_preprocessing(data):
#     """Preprocessing data with safe handling for unknown categories"""
#     data = data.copy()
#     df = pd.DataFrame()
#     data["Admission_grade"] = scaler_Admission_grade.transform(np.asarray(data["Admission_grade"]).reshape(-1,1))[0]
#     data["Age_at_enrollment"] = scaler_Age_at_enrollment.transform(np.asarray(data["Age_at_enrollment"]).reshape(-1,1))[0]
#     data["GDP"] = scaler_GDP.transform(np.asarray(data["GDP"]).reshape(-1,1))[0]
#     data["Inflation_rate"] = scaler_Inflation_rate.transform(np.asarray(data["Inflation_rate"]).reshape(-1,1))[0]
#     data["Previous_qualification_grade"] = scaler_Previous_qualification_grade.transform(np.asarray(data["Previous_qualification_grade"]).reshape(-1,1))[0]
#     data["Unemployment_rate"] = scaler_Unemployment_rate.transform(np.asarray(data["Unemployment_rate"]).reshape(-1,1))[0]
#     data["Curricular_units_1st_sem_approved"] = scaler_Curricular_units_1st_sem_approved.transform(np.asarray(data["Curricular_units_1st_sem_approved"]).reshape(-1,1))[0]
#     data["Curricular_units_1st_sem_credited"] = scaler_Curricular_units_1st_sem_credited.transform(np.asarray(data["Curricular_units_1st_sem_credited"]).reshape(-1,1))[0]
#     data["Curricular_units_1st_sem_enrolled"] = scaler_Curricular_units_1st_sem_enrolled.transform(np.asarray(data["Curricular_units_1st_sem_enrolled"]).reshape(-1,1))[0]
#     data["Curricular_units_1st_sem_evaluations"] = scaler_Curricular_units_1st_sem_evaluations.transform(np.asarray(data["Curricular_units_1st_sem_evaluations"]).reshape(-1,1))[0]
#     data["Curricular_units_1st_sem_grade"] = scaler_Curricular_units_1st_sem_grade.transform(np.asarray(data["Curricular_units_1st_sem_grade"]).reshape(-1,1))[0]
#     data["Curricular_units_1st_sem_without_evaluations"] = scaler_Curricular_units_1st_sem_without_evaluations.transform(np.asarray(data["Curricular_units_1st_sem_without_evaluations"]).reshape(-1,1))[0]


#     data["Curricular_units_2nd_sem_approved"] = scaler_Curricular_units_2nd_sem_approved.transform(np.asarray(data["Curricular_units_2nd_sem_approved"]).reshape(-1,1))[0]
#     data["Curricular_units_2nd_sem_credited"] = scaler_Curricular_units_2nd_sem_credited.transform(np.asarray(data["Curricular_units_2nd_sem_credited"]).reshape(-1,1))[0]
#     data["Curricular_units_2nd_sem_enrolled"] = scaler_Curricular_units_2nd_sem_enrolled.transform(np.asarray(data["Curricular_units_2nd_sem_enrolled"]).reshape(-1,1))[0]
#     data["Curricular_units_2nd_sem_evaluations"] = scaler_Curricular_units_2nd_sem_evaluations.transform(np.asarray(data["Curricular_units_2nd_sem_evaluations"]).reshape(-1,1))[0]
#     data["Curricular_units_2nd_sem_grade"] = scaler_Curricular_units_2nd_sem_grade.transform(np.asarray(data["Curricular_units_2nd_sem_grade"]).reshape(-1,1))[0]
#     data["Curricular_units_2nd_sem_without_evaluations"] = scaler_Curricular_units_2nd_sem_without_evaluations.transform(np.asarray(data["Curricular_units_2nd_sem_without_evaluations"]).reshape(-1,1))[0]

#     df["Application_mode"] = encoder_Application_mode.transform(data["Application_mode"])
#     df["Application_order"] = encoder_Application_order.transform(data["Application_order"])
#     df["Course"] = encoder_Course.transform(data["Course"])
#     df["Debtor"] = encoder_Debtor.transform(data["Debtor"])
#     df["Displaced"] = encoder_Displaced.transform(data["Displaced"])

#     df["Fathers_occupation"] = encoder_Fathers_occupation.transform(data["Fathers_occupation"])
#     df["Fathers_qualification"] = encoder_Fathers_qualification.transform(data["Fathers_qualification"])
#     df["Gender"] = encoder_Gender.transform(data["Gender"])
#     df["Marital_status"] = encoder_Marital_status.transform(data["Marital_status"])
#     df["Mothers_occupation"] = encoder_Mothers_occupation.transform(data["Mothers_occupation"])
#     df["Mothers_qualification"] = encoder_Mothers_qualification.transform(data["Mothers_qualification"])
#     df["Nacionality"] = encoder_Nacionality.transform(data["Nacionality"])
#     df["Previous_qualification"] = encoder_Previous_qualification.transform(data["Previous_qualification"])
#     df["Scholarship_holder"] = encoder_Scholarship_holder.transform(data["Scholarship_holder"])
#     df["Tuition_fees_up_to_date"] = encoder_Tuition_fees_up_to_date.transform(data["Tuition_fees_up_to_date"])

#     # PCA 1
#     df[["pc1_1", "pc1_2", "pc1_3", "pc1_4"]] = pca_1.transform(data[pca_numerical_columns_1])
    
#     # PCA 2
#     df[["pc2_1", "pc2_2", "pc2_3", "pc2_4", "pc2_5", "pc2_6", "pc2_7", "pc2_8"]] = pca_2.transform(data[pca_numerical_columns_2])
    
#     return df




model = joblib.load("model/rdf_model.joblib")
result_target = joblib.load("model/encoder_target.joblib")

def prediction(data):
    ## Making prediction
    result = model.predict(data)
    final_result = result_target.inverse_transform(result)[0]
    return final_result


st.title("Prototype Student'S Performance")
st.write("Ini adalah prototype modeling untuk Jaya jaya institut")

data = pd.DataFrame()


col1, col2 = st.columns(2)
default_index = 0

marital_status_opt = [f"[{key}] {value}" for key, value in marital_status_dict.items()]

with col1:
    marital_status = st.selectbox(label='Marital Status', options=marital_status_opt, index=1)
    selected_marital_key = int(marital_status.split("]")[0][1:])
    data["Marital_status"] = [selected_marital_key]
 
application_mode_opt = [f"[{key}] {value}" for key, value in application_mode_dict.items()]

with col2:
    application_mode = st.selectbox(label='Application mode', options=application_mode_opt, index=1)
    selected_application_mode_key = int(application_mode.split("]")[0][1:])
    data["Application_mode"] = [selected_application_mode_key]





col1, col2, col3 = st.columns(3)
application_order_opt = angka = [i for i in range(1, 10)]

with col1:
    application_order = st.selectbox(label='Application order', options=application_order_opt, index=1)
    data["Application_order"] = [application_order]

course_opt = [f"[{key}] {value}" for key, value in course_dict.items()]

with col2:
    course = st.selectbox(label='Course', options=course_opt, index=1)
    selected_course_key = int(course.split("]")[0][1:])
    data["Course"] = [selected_course_key]


nacionality_opt = [f"[{key}] {value}" for key, value in nacionality_dict.items()]

with col3:
    nacionality = st.selectbox(label='Nacionality', options=nacionality_opt, index=1)
    selected_nacionality_key = int(nacionality.split("]")[0][1:])
    data["Nacionality"] = [selected_nacionality_key]





col1, col2 = st.columns(2)
default_index = 0

mothers_qualification_opt = [f"[{key}] {value}" for key, value in mothers_qualification_dict.items()]

with col1:
    mothers_qualification = st.selectbox(label='Mothers Qualification', options=mothers_qualification_opt, index=1)
    selected_mothers_qualification_key = int(mothers_qualification.split("]")[0][1:])
    data["Mothers_qualification"] = [selected_mothers_qualification_key]
 
fathers_qualification_opt = [f"[{key}] {value}" for key, value in fathers_qualification_dict.items()]

with col2:
    fathers_qualification = st.selectbox(label='Fathers Qualification', options=fathers_qualification_opt, index=1)
    selected_fathers_qualification_key = int(fathers_qualification.split("]")[0][1:])
    data["Fathers_qualification"] = [selected_fathers_qualification_key]





col1, col2 = st.columns(2)
default_index = 0

mothers_occupation_opt = [f"[{key}] {value}" for key, value in mothers_occupation_dict.items()]
with col1:
    mothers_occupation = st.selectbox(label='Mothers occupation', options=mothers_occupation_opt, index=1)
    selected_mothers_occupation_key = int(mothers_occupation.split("]")[0][1:])
    data["Mothers_occupation"] = [selected_mothers_occupation_key]
 
fathers_occupation_opt = [f"[{key}] {value}" for key, value in fathers_occupation_dict.items()]
with col2:
    fathers_occupation = st.selectbox(label='Fathers occupation', options=fathers_occupation_opt, index=1)
    selected_fathers_occupation_key = int(fathers_occupation.split("]")[0][1:])
    data["Fathers_occupation"] = [selected_fathers_occupation_key]



col1, col2,col3 = st.columns(3)
default_index = 0

previous_qualification_opt = [f"[{key}] {value}" for key, value in previous_qualification_dict.items()]

with col1:
    previous_qualification = st.selectbox(label='Previous Qualification', options=previous_qualification_opt, index=1)
    selected_previous_qualification_key = int(previous_qualification.split("]")[0][1:])
    data["Previous_qualification"] = [selected_previous_qualification_key]

displaced_opt = [f"[{key}] {value}" for key, value in y_n_dict.items()]
with col2:
    displaced = st.selectbox(label='Displaced', options=displaced_opt, index=1)
    selected_displaced_key = int(displaced.split("]")[0][1:])
    data["Displaced"] = [selected_displaced_key]
 
debtor_opt = [f"[{key}] {value}" for key, value in y_n_dict.items()]
with col3:
    debtor = st.selectbox(label='Debtor', options=debtor_opt, index=1)
    selected_debtor_key = int(debtor.split("]")[0][1:])
    data["Debtor"] = [selected_debtor_key]


col1, col2,col3 = st.columns(3)
default_index = 0

tuition_fees_up_to_date_opt = [f"[{key}] {value}" for key, value in y_n_dict.items()]

with col1:
    tuition_fees_up_to_date = st.selectbox(label='Tuition fees up to date', options=tuition_fees_up_to_date_opt, index=1)
    selected_tuition_fees_up_to_date_key = int(tuition_fees_up_to_date.split("]")[0][1:])
    data["Tuition_fees_up_to_date"] = [selected_tuition_fees_up_to_date_key]

scholarship_holder_opt = [f"[{key}] {value}" for key, value in y_n_dict.items()]
with col2:
    scholarship_holder = st.selectbox(label='Scholarship holder', options=scholarship_holder_opt, index=1)
    selected_scholarship_holder_key = int(scholarship_holder.split("]")[0][1:])
    data["Scholarship_holder"] = [selected_scholarship_holder_key]
 
gender_opt = [f"[{key}] {value}" for key, value in gender_dict.items()]
with col3:
    gender = st.selectbox(label='gender', options=gender_opt, index=1)
    selected_gender_key = int(gender.split("]")[0][1:])
    data["Gender"] = [selected_gender_key]


col1, col2, col3, col4 = st.columns(4)
 
with col1:
    Previous_qualification_grade = float(st.number_input(label='Previous qualification grade', min_value=0, max_value=200))
    data["Previous_qualification_grade"] = Previous_qualification_grade
 
with col2:
    Admission_grade = float(st.number_input(label='Admission grade', min_value=0, max_value=200))
    data["Admission_grade"] = Admission_grade
 
with col3:
    Age_at_enrollment = float(st.number_input(label='Age at enrollment', min_value=17, max_value=80))
    data["Age_at_enrollment"] = Age_at_enrollment
 
with col4:
    GDP = float(st.number_input(label='GDP',value=0.00))
    data["GDP"] = GDP



col1, col2 = st.columns(2)
 
with col1:
    Inflation_rate = float(st.number_input(label='Inflation Rate', min_value=-100.00, max_value=100.00,value=0.00))
    data["Inflation_rate"] = Inflation_rate
 
with col2:
    Unemployment_rate = float(st.number_input(label='Unemployment rate', min_value=-100.00, max_value=100.00, value=0.0))
    data["Unemployment_rate"] = Unemployment_rate
 



col1, col2, col3, col4 = st.columns(4)
 
with col1:
    Curricular_units_1st_sem_approved = float(st.number_input(label='Curricular units 1st sem approved', min_value=-100.00, max_value=100.00,value=0.00))
    data["Curricular_units_1st_sem_approved"] = Curricular_units_1st_sem_approved
 
with col2:
    Curricular_units_1st_sem_credited = float(st.number_input(label='Curricular units 1st sem credited',min_value=-100.00, max_value=100.00,value=0.00))
    data["Curricular_units_1st_sem_credited"] = Curricular_units_1st_sem_credited
 
with col3:
    Curricular_units_1st_sem_enrolled = float(st.number_input(label='Curricular units 1st sem enrolled',min_value=-100.00, max_value=100.00,value=0.00))
    data["Curricular_units_1st_sem_enrolled"] = Curricular_units_1st_sem_enrolled
 
with col4:
    Curricular_units_1st_sem_evaluations = float(st.number_input(label='Curricular units 1st sem evaluations',min_value=-100.00, max_value=100.00,value=0.00))
    data["Curricular_units_1st_sem_evaluations"] = Curricular_units_1st_sem_evaluations


col1, col2 = st.columns(2)
 
with col1:
    Curricular_units_1st_sem_grade = float(st.number_input(label='Curricular units 1st sem grade',min_value=-100.00, max_value=100.00,value=0.00))
    data["Curricular_units_1st_sem_grade"] = Curricular_units_1st_sem_grade
 
with col2:
    Curricular_units_1st_sem_without_evaluations = float(st.number_input(label='Curricular units 1st sem without evaluations',min_value=-100.00, max_value=100.00,value=0.00))
    data["Curricular_units_1st_sem_without_evaluations"] = Curricular_units_1st_sem_without_evaluations




col1, col2, col3, col4 = st.columns(4)
 
with col1:
    Curricular_units_2nd_sem_approved = float(st.number_input(label='Curricular units 2nd sem approved',min_value=-100.00, max_value=100.00,value=0.00))
    data["Curricular_units_2nd_sem_approved"] = Curricular_units_2nd_sem_approved
 
with col2:
    Curricular_units_2nd_sem_credited = float(st.number_input(label='Curricular units 2nd sem credited',min_value=-100.00, max_value=100.00,value=0.00))
    data["Curricular_units_2nd_sem_credited"] = Curricular_units_2nd_sem_credited
 
with col3:
    Curricular_units_2nd_sem_enrolled = float(st.number_input(label='Curricular units 2nd sem enrolled',min_value=-100.00, max_value=100.00,value=0.00))
    data["Curricular_units_2nd_sem_enrolled"] = Curricular_units_2nd_sem_enrolled
 
with col4:
    Curricular_units_2nd_sem_evaluations = float(st.number_input(label='Curricular units 2nd sem evaluations',min_value=-100.00, max_value=100.00,value=0.00))
    data["Curricular_units_2nd_sem_evaluations"] = Curricular_units_2nd_sem_evaluations


col1, col2 = st.columns(2)
 
with col1:
    Curricular_units_2nd_sem_grade = float(st.number_input(label='Curricular units 2nd sem grade',min_value=-100.00, max_value=100.00,value=0.00))
    data["Curricular_units_2nd_sem_grade"] = Curricular_units_2nd_sem_grade
 
with col2:
    Curricular_units_2nd_sem_without_evaluations = float(st.number_input(label='Curricular units 2nd sem without evaluations',min_value=-100.00, max_value=100.00,value=0.00))
    data["Curricular_units_2nd_sem_without_evaluations"] = Curricular_units_2nd_sem_without_evaluations


with st.expander("View the Raw Data"):
    st.dataframe(data=data, width=800, height=10)

from sklearn.preprocessing import OneHotEncoder

# Initialize OneHotEncoder with handle_unknown='ignore'
if st.button('Predict'):
    new_data = data_preprocessing(data=data)
    st.dataframe(data=new_data, width=800, height=10)
    st.write("Forecasting Student's Status: {}".format(prediction(new_data)))