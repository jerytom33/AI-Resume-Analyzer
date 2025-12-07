import io
import os
import random
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import TextConverter
from pyresparser import ResumeParser
from Courses import ds_course, web_course, android_course, ios_course, uiux_course

def pdf_reader(file_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
    converter.close()
    fake_file_handle.close()
    return text

def course_recommender(course_list):
    rec_course = []
    # defaulting to 5 recommendations
    no_of_reco = 5
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        rec_course.append({"name": c_name, "link": c_link})
        if len(rec_course) == no_of_reco:
            break
    return rec_course

def analyze_resume(file_path):
    # 1. Extract Data
    resume_data = ResumeParser(file_path).get_extracted_data()
    if not resume_data:
        return None
        
    resume_text = pdf_reader(file_path)
    
    # 2. Candidate Level
    cand_level = ''
    if resume_data['no_of_pages'] < 1:
        cand_level = "Fresher"
    elif 'INTERNSHIP' in resume_text or 'INTERNSHIPS' in resume_text or 'Internship' in resume_text or 'Internships' in resume_text:
        cand_level = "Intermediate"
    elif 'EXPERIENCE' in resume_text or 'WORK EXPERIENCE' in resume_text or 'Experience' in resume_text or 'Work Experience' in resume_text:
        cand_level = "Experienced"
    else:
        cand_level = "Fresher"

    # 3. Recommendations (Field & Skills & Courses)
    ds_keyword = ['tensorflow','keras','pytorch','machine learning','deep Learning','flask','streamlit']
    web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress','javascript', 'angular js', 'C#', 'Asp.net', 'flask']
    android_keyword = ['android','android development','flutter','kotlin','xml','kivy']
    ios_keyword = ['ios','ios development','swift','cocoa','cocoa touch','xcode']
    uiux_keyword = ['ux','adobe xd','figma','zeplin','balsamiq','ui','prototyping','wireframes','storyframes','adobe photoshop','photoshop','editing','adobe illustrator','illustrator','adobe after effects','after effects','adobe premier pro','premier pro','adobe indesign','indesign','wireframe','solid','grasp','user research','user experience']
    n_any = ['english','communication','writing', 'microsoft office', 'leadership','customer management', 'social media']

    reco_field = 'NA'
    recommended_skills = []
    rec_courses = []

    skills = resume_data['skills'] if resume_data['skills'] else []
    
    for i in skills:
        if i.lower() in ds_keyword:
            reco_field = 'Data Science'
            recommended_skills = ['Data Visualization','Predictive Analysis','Statistical Modeling','Data Mining','Clustering & Classification','Data Analytics','Quantitative Analysis','Web Scraping','ML Algorithms','Keras','Pytorch','Probability','Scikit-learn','Tensorflow',"Flask",'Streamlit']
            rec_courses = course_recommender(ds_course)
            break
        elif i.lower() in web_keyword:
            reco_field = 'Web Development'
            recommended_skills = ['React','Django','Node JS','React JS','php','laravel','Magento','wordpress','Javascript','Angular JS','c#','Flask','SDK']
            rec_courses = course_recommender(web_course)
            break
        elif i.lower() in android_keyword:
            reco_field = 'Android Development'
            recommended_skills = ['Android','Android development','Flutter','Kotlin','XML','Java','Kivy','GIT','SDK','SQLite']
            rec_courses = course_recommender(android_course)
            break
        elif i.lower() in ios_keyword:
            reco_field = 'IOS Development'
            recommended_skills = ['IOS','IOS Development','Swift','Cocoa','Cocoa Touch','Xcode','Objective-C','SQLite','Plist','StoreKit',"UI-Kit",'AV Foundation','Auto-Layout']
            rec_courses = course_recommender(ios_course)
            break
        elif i.lower() in uiux_keyword:
            reco_field = 'UI-UX Development'
            recommended_skills = ['UI','User Experience','Adobe XD','Figma','Zeplin','Balsamiq','Prototyping','Wireframes','Storyframes','Adobe Photoshop','Editing','Illustrator','After Effects','Premier Pro','Indesign','Wireframe','Solid','Grasp','User Research']
            rec_courses = course_recommender(uiux_course)
            break
        elif i.lower() in n_any:
            reco_field = 'NA'
            recommended_skills = ['No Recommendations']
            rec_courses = []
            break

    # 4. Resume Score
    resume_score = 0
    score_breakdown = []

    if 'Objective' in resume_text or 'Summary' in resume_text:
        resume_score += 6
        score_breakdown.append("[+] Added Objective/Summary")
    else:
        score_breakdown.append("[-] Missing Objective/Summary")

    if 'Education' in resume_text or 'School' in resume_text or 'College' in resume_text:
        resume_score += 12
        score_breakdown.append("[+] Added Education Details")
    else:
        score_breakdown.append("[-] Missing Education Details")

    if 'EXPERIENCE' in resume_text or 'Experience' in resume_text:
        resume_score += 16
        score_breakdown.append("[+] Added Experience")
    else:
        score_breakdown.append("[-] Missing Experience")

    if 'INTERNSHIPS' in resume_text or 'INTERNSHIP' in resume_text or 'Internships' in resume_text or 'Internship' in resume_text:
        resume_score += 6
        score_breakdown.append("[+] Added Internships")
    else:
        score_breakdown.append("[-] Missing Internships")

    if 'SKILLS' in resume_text or 'SKILL' in resume_text or 'Skills' in resume_text or 'Skill' in resume_text:
        resume_score += 7
        score_breakdown.append("[+] Added Skills")
    else:
        score_breakdown.append("[-] Missing Skills")

    if 'HOBBIES' in resume_text or 'Hobbies' in resume_text:
        resume_score += 4
        score_breakdown.append("[+] Added Hobbies")
    else:
        score_breakdown.append("[-] Missing Hobbies")

    if 'INTERESTS' in resume_text or 'Interests' in resume_text:
        resume_score += 5
        score_breakdown.append("[+] Added Interests")
    else:
        score_breakdown.append("[-] Missing Interests")

    if 'ACHIEVEMENTS' in resume_text or 'Achievements' in resume_text:
        resume_score += 13
        score_breakdown.append("[+] Added Achievements")
    else:
        score_breakdown.append("[-] Missing Achievements")

    if 'CERTIFICATIONS' in resume_text or 'Certifications' in resume_text or 'Certification' in resume_text:
        resume_score += 12
        score_breakdown.append("[+] Added Certifications")
    else:
        score_breakdown.append("[-] Missing Certifications")

    if 'PROJECTS' in resume_text or 'PROJECT' in resume_text or 'Projects' in resume_text or 'Project' in resume_text:
        resume_score += 19
        score_breakdown.append("[+] Added Projects")
    else:
        score_breakdown.append("[-] Missing Projects")

    return {
        "basic_details": resume_data,
        "candidate_level": cand_level,
        "predicted_field": reco_field,
        "recommended_skills": recommended_skills,
        "recommended_courses": rec_courses,
        "resume_score": resume_score,
        "score_breakdown": score_breakdown
    }
