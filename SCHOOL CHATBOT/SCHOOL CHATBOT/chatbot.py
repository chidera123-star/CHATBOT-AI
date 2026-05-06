# ============================================================
#  CSC 309 Mini Project #1 — Smart Rule-Based School Chatbot
#  Concepts : NLP (basic), Pattern Matching
#  Tools    : Python, NLTK
# ============================================================

import re
import random
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)

stemmer    = PorterStemmer()
stop_words = set(stopwords.words("english"))

KNOWLEDGE_BASE = [

    # ── GREETINGS ──────────────────────────────────────────
    {
        "tag": "greeting",
        "patterns": ["hello", "hi", "hey", "good morning", "good afternoon",
                     "good evening", "howdy", "what's up", "sup", "greetings", "how are you"],
        "responses": [
            "Hello! I am SchoolBot, your academic assistant. How may I help you today?",
            "Good day! I am here to assist you with any school-related questions. What would you like to know?",
            "Hello there! Feel free to ask me anything about studying, exams, assignments, or school life.",
        ],
    },

    # ── FAREWELL ───────────────────────────────────────────
    {
        "tag": "farewell",
        "patterns": ["bye", "goodbye", "see you", "later", "take care", "exit", "quit", "farewell", "cya"],
        "responses": [
            "Goodbye! I wish you the very best in your studies.",
            "Take care and keep up the excellent work. All the best!",
            "Farewell! Remember, consistency is the foundation of academic success.",
        ],
    },

    # ── THANKS ─────────────────────────────────────────────
    {
        "tag": "thanks",
        "patterns": ["thank you", "thanks", "appreciate it", "cheers", "that helped", "helpful"],
        "responses": [
            "You are most welcome. I am always happy to help.",
            "It is my pleasure. Do not hesitate to ask if you need anything else.",
            "Glad I could be of assistance. Feel free to come back anytime.",
        ],
    },

    # ── IDENTITY ───────────────────────────────────────────
    {
        "tag": "identity",
        "patterns": ["who are you", "what are you", "your name", "what is your name",
                     "are you a bot", "are you human", "what can you do", "tell me about yourself"],
        "responses": [
            "I am SchoolBot, a rule-based artificial intelligence chatbot developed for CSC 309 Mini Project Number One. I specialize in answering school-related questions to help students succeed academically.",
            "My name is SchoolBot. I was built using Python and the Natural Language Toolkit as part of CSC 309. I can assist you with exams, studying strategies, assignments, time management, programming, and much more.",
        ],
    },

    # ── EXAMS ──────────────────────────────────────────────
    {
        "tag": "exams",
        "patterns": ["exam", "exams", "test", "examination", "finals", "midterm",
                     "quiz", "assessment", "prepare for exam", "exam tips", "how to pass"],
        "responses": [
            "Preparing well for examinations requires a structured and disciplined approach. Begin studying at least one week in advance rather than leaving everything to the night before. Divide your topics into manageable sections and tackle one at a time. Practice with past examination questions, as this is one of the most effective preparation strategies available. Take short breaks every forty-five minutes to keep your mind alert and fresh. Ensure you get adequate sleep the night before your examination, because a well-rested mind performs significantly better under pressure.",
            "Here are some proven strategies to help you excel in your examinations. Create a detailed revision timetable and commit to it consistently. Summarize your notes in your own words rather than copying them, as this strengthens your understanding considerably. Form a study group with serious classmates and quiz each other regularly. Attempt past questions under timed examination conditions to simulate the real experience. Stay well hydrated, maintain a healthy diet, and avoid excessive caffeine during your revision period.",
        ],
    },

    # ── EXAM ANXIETY ───────────────────────────────────────
    {
        "tag": "exam_anxiety",
        "patterns": ["exam anxiety", "scared of exams", "nervous about exam", "fear of exams",
                     "panic exam", "worried about test", "test anxiety"],
        "responses": [
            "Examination anxiety is extremely common among students, and it is entirely manageable with the right strategies. First, thorough preparation is the single most powerful remedy for exam anxiety — the more prepared you are, the more confident you will feel. Second, practice deep breathing exercises before and during the exam to calm your nervous system. Third, arrive early at the examination venue so you are not rushing. During the exam, begin with the questions you find easiest to build your confidence, then return to the more challenging ones. Remember that some level of nerves is actually beneficial, as it sharpens your focus.",
        ],
    },

    # ── STUDYING ───────────────────────────────────────────
    {
        "tag": "study",
        "patterns": ["study", "studying", "how to study", "study tips", "learn",
                     "memorize", "remember", "retain", "concentration", "focus", "reading"],
        "responses": [
            "There are several highly effective study techniques supported by academic research. The Pomodoro Technique involves studying for twenty-five minutes followed by a five-minute break, which helps maintain concentration over extended periods. Active Recall means testing yourself on the material rather than simply re-reading it, and research shows this dramatically improves long-term memory retention. Spaced Repetition involves reviewing information at increasing time intervals. Mind Mapping helps you visualize relationships between ideas. Teaching the material to another person is widely regarded as one of the most powerful learning methods available.",
            "To study more effectively, begin by creating a dedicated, quiet study space that is free from distractions. Silence your phone and place it out of reach while studying. Use flashcards for definitions and key concepts. Rewrite your lecture notes in your own words shortly after each class, while the content is still fresh. Always tackle your most challenging subject first when your mental energy is at its highest level.",
        ],
    },

    # ── NOTE TAKING ────────────────────────────────────────
    {
        "tag": "note_taking",
        "patterns": ["notes", "note taking", "how to take notes", "note-taking",
                     "lecture notes", "class notes", "better notes"],
        "responses": [
            "Effective note-taking is one of the most important academic skills you can develop. The Cornell Method is particularly effective: divide your page into three sections — a wide column on the right for your main notes, a narrow column on the left for key questions and terms, and a summary section at the bottom of the page. Write in your own words rather than copying verbatim, use abbreviations to keep up with the lecturer, and leave space to add details during your review. Always review and complete your notes within twenty-four hours of the lecture while the material is still fresh.",
        ],
    },

    # ── TIME MANAGEMENT ────────────────────────────────────
    {
        "tag": "time_management",
        "patterns": ["time management", "timetable", "schedule", "plan", "planning",
                     "deadline", "procrastination", "procrastinate", "organize", "busy", "no time"],
        "responses": [
            "Effective time management is one of the most valuable skills a student can develop. Begin by using a planner or digital calendar to record every deadline and commitment. Prioritize your tasks by distinguishing between what is urgent and what is merely important. Break large assignments into smaller, specific steps so they feel less daunting. Set clear daily goals each morning and review your progress each evening. If you struggle with procrastination, the most effective remedy is simply to begin — starting with just five minutes of focused work is usually enough to build momentum.",
            "Creating a consistent study schedule will transform your academic performance. List all your subjects and their upcoming deadlines. Allocate more time to the subjects you find most challenging, and ensure your schedule includes regular breaks and time for rest and leisure. Review and adjust your schedule at the beginning of each week. Digital tools such as Google Calendar, Notion, or Trello are excellent for setting reminders and tracking your progress.",
        ],
    },

    # ── ASSIGNMENTS ────────────────────────────────────────
    {
        "tag": "assignments",
        "patterns": ["assignment", "homework", "project", "coursework", "submit",
                     "deadline", "report", "essay", "write", "writing", "dissertation", "thesis"],
        "responses": [
            "To produce high-quality assignments, begin by reading the instructions thoroughly and carefully before you start. Break the work into clearly defined sections and address each one systematically. Starting early gives you sufficient time for research, drafting, revision, and proofreading. Always cite your sources correctly using the referencing style required by your institution, as plagiarism is a serious academic offence with severe consequences. Before submitting, proofread your work carefully for grammatical errors, unclear arguments, and formatting inconsistencies.",
            "Writing an effective academic report or essay requires careful planning from the outset. Begin with a clear outline that maps your introduction, main body sections, and conclusion. Use precise, clear language and support every major argument with relevant evidence. Your introduction should clearly state the purpose of the work, and your conclusion should summarize your key findings or arguments without introducing new information. If possible, ask a trusted classmate to review your draft before submission.",
        ],
    },

    # ── PLAGIARISM ─────────────────────────────────────────
    {
        "tag": "plagiarism",
        "patterns": ["plagiarism", "plagiarize", "copy", "cheating", "academic dishonesty",
                     "cite", "citation", "reference", "referencing", "bibliography"],
        "responses": [
            "Plagiarism is the act of presenting someone else's work, ideas, or words as your own without proper acknowledgment, and it is considered a serious form of academic dishonesty. Most institutions impose severe penalties for plagiarism, including failing the assignment, failing the course, or even expulsion. To avoid plagiarism, always cite your sources using the referencing format required by your department, whether that is APA, Harvard, MLA, or Chicago style. When in doubt about whether something requires a citation, it is always safer to include one. Paraphrasing in your own words and then citing the original source is perfectly acceptable.",
        ],
    },

    # ── PROGRAMMING ────────────────────────────────────────
    {
        "tag": "programming",
        "patterns": ["programming", "coding", "code", "python", "java", "c++", "javascript",
                     "algorithm", "data structure", "software", "debug", "error",
                     "computer science", "csc", "information technology", "software engineering"],
        "responses": [
            "To become proficient in programming, consistent daily practice is absolutely essential. Even thirty minutes of coding each day produces remarkable improvement over time. Always learn by building real projects rather than simply reading tutorials, as practical hands-on experience is irreplaceable. When you encounter an error, do not be discouraged — break the problem into smaller components and test each part individually. Every professional programmer encounters errors constantly; the ability to read and interpret error messages clearly is itself a valuable skill. Platforms such as HackerRank, LeetCode, and Codecademy offer excellent structured practice exercises.",
            "For students studying Python, I recommend building small personal projects to reinforce your understanding of each concept. Practice regularly on coding challenge platforms. Consult the official Python documentation whenever you are uncertain about a function or method. Join developer communities such as Stack Overflow where you can ask questions and learn from experienced practitioners. Remember that understanding the logic behind the code is far more important than memorizing syntax.",
        ],
    },

    # ── MATHEMATICS ────────────────────────────────────────
    {
        "tag": "mathematics",
        "patterns": ["mathematics", "maths", "math", "calculus", "algebra", "statistics",
                     "geometry", "trigonometry", "equations", "numbers", "formula"],
        "responses": [
            "Mathematics requires consistent practice above all else — you cannot learn it by reading alone. Work through as many problems as possible, starting with simpler examples before progressing to more complex ones. When you encounter a concept you do not understand, do not move forward until it is clear, as mathematics builds upon itself and gaps in understanding compound over time. Use textbooks, YouTube tutorials, and platforms such as Khan Academy, which provides free, excellent mathematics instruction at every level. Form a study group with classmates and work through problems together, as explaining your reasoning to others deepens your own understanding significantly.",
        ],
    },

    # ── SCIENCE ────────────────────────────────────────────
    {
        "tag": "science",
        "patterns": ["science", "physics", "chemistry", "biology", "lab", "laboratory",
                     "experiment", "research", "scientific", "hypothesis"],
        "responses": [
            "Science subjects require a combination of conceptual understanding and practical application. For theoretical content, focus on understanding the underlying principles rather than memorizing facts in isolation, as this allows you to answer unfamiliar questions by reasoning from first principles. For laboratory work, prepare thoroughly by reading the procedure in advance and understanding the purpose of each step. Write up your laboratory reports promptly while the details are still clear in your memory. Khan Academy and YouTube channels such as CrashCourse offer excellent free science content for revision.",
        ],
    },

    # ── READING ────────────────────────────────────────────
    {
        "tag": "reading",
        "patterns": ["reading speed", "how to read faster", "reading comprehension",
                     "textbook", "academic reading", "read better", "understand reading"],
        "responses": [
            "Improving your academic reading requires developing active reading habits. Before reading a chapter or article in full, begin by skimming the headings, subheadings, introduction, and conclusion to get an overview of the content and structure. As you read, highlight or underline key points and write brief margin notes in your own words. After completing each section, pause and summarize the main points without looking at the text — this is a form of active recall that greatly improves comprehension and retention. For dense academic texts, reading more slowly and carefully is often more productive than reading quickly.",
        ],
    },

    # ── STRESS ─────────────────────────────────────────────
    {
        "tag": "stress",
        "patterns": ["stressed", "stress", "anxious", "anxiety", "overwhelmed", "tired",
                     "burnout", "exhausted", "worried", "nervous", "motivation", "give up",
                     "depressed", "sad", "struggling", "hard time", "difficult"],
        "responses": [
            "It is completely natural to feel stressed as a student, and you should know that you are certainly not alone in this experience. When you feel overwhelmed, the most important first step is to pause and give yourself permission to take a short break. Go for a walk, do some stretching, or simply step away from your desk for ten minutes. Talk openly to a friend, classmate, family member, or counsellor about how you are feeling, as sharing your concerns often reduces their weight considerably. Break your workload into the smallest possible tasks so that each one feels achievable. Celebrate every small victory, because progress, however modest, deserves genuine recognition.",
            "Maintaining motivation throughout your studies requires deliberate and consistent effort. Remind yourself regularly of the reason you began this academic journey and the goals you are working towards. Understand that every expert was once a complete beginner, and that experiencing difficulty is a sign of growth rather than failure. Take your rest seriously — adequate sleep and proper recovery are not luxuries but absolute necessities for sustained academic performance. Focus on progress rather than perfection, and take each day one step at a time.",
        ],
    },

    # ── MENTAL HEALTH ──────────────────────────────────────
    {
        "tag": "mental_health",
        "patterns": ["mental health", "counseling", "counselling", "therapy",
                     "psychologist", "depression", "not coping", "need help", "help me"],
        "responses": [
            "Your mental health is just as important as your academic performance, and it is courageous to acknowledge when you need support. Most universities and colleges offer free confidential counselling services for students — I strongly encourage you to reach out to your institution's student support or counselling centre. Speaking with a trained counsellor can make an enormous difference. You can also speak with a trusted lecturer, academic advisor, or family member. Please remember that seeking help is a sign of strength, not weakness, and there are people who genuinely want to support you.",
        ],
    },

    # ── GRADES ─────────────────────────────────────────────
    {
        "tag": "grades",
        "patterns": ["gpa", "grade", "grades", "cgpa", "result", "score", "marks",
                     "fail", "failed", "pass", "distinction", "improve grade", "low grade", "retake"],
        "responses": [
            "Improving your grades requires consistent effort across several areas simultaneously. Attend all lectures and take thorough, organized notes. Submit every assignment on time, as missed submissions can significantly reduce your final grade. When you are confused about a topic, seek clarification from your lecturer or a knowledgeable classmate immediately rather than allowing the confusion to build. Forming a focused study group can also be enormously beneficial. Make use of your lecturers' office hours, as most are very willing to provide guidance to students who take the initiative to ask for it.",
            "To raise your Grade Point Average, begin by understanding precisely how your grades are calculated for each course. Pay particular attention to subjects where you are close to the boundary between grade categories, as targeted effort there can make a significant difference to your overall average. Take advantage of any extra credit opportunities your lecturers may offer. Above all, build consistent daily study habits rather than relying on intensive last-minute revision, which is far less effective for long-term retention.",
        ],
    },

    # ── FAILING ────────────────────────────────────────────
    {
        "tag": "failing",
        "patterns": ["i failed", "failed my exam", "failed a course", "i am failing",
                     "bad grades", "poor performance", "i might fail", "repeat"],
        "responses": [
            "Failing an exam or a course is undoubtedly difficult and discouraging, but it is important to understand that it is not the end of your academic journey. Many highly successful people have experienced academic setbacks and gone on to achieve great things. The most important step is to reflect honestly on what went wrong and make a concrete plan to address it. Speak with your lecturer or academic advisor as soon as possible — they can advise you on your options, which may include resitting the examination, repeating the course, or accessing additional academic support. Use this experience as a learning opportunity rather than allowing it to define your self-worth.",
        ],
    },

    # ── LECTURES ───────────────────────────────────────────
    {
        "tag": "lectures",
        "patterns": ["lecture", "class", "attend", "attendance", "lecturer",
                     "professor", "teacher", "course", "tutorial", "seminar"],
        "responses": [
            "To get the maximum benefit from your lectures, sit near the front of the room where you are less likely to be distracted. Put your phone away and give the lecturer your complete attention throughout. Take notes in your own words rather than attempting to write everything down verbatim, as paraphrasing actively engages your understanding. Do not hesitate to ask questions during or after the lecture. Review and complete your notes within twenty-four hours of each lecture while the content is still clear in your memory.",
        ],
    },

    # ── ATTENDANCE ─────────────────────────────────────────
    {
        "tag": "attendance",
        "patterns": ["skip class", "skipping", "miss lecture", "attendance record",
                     "absent", "should i attend", "is attendance important"],
        "responses": [
            "Regular attendance is one of the most important factors in academic success. Research consistently shows a strong positive correlation between lecture attendance and final grades. When you attend every session, you receive information directly from your lecturer, gain context that is difficult to obtain from notes alone, have the opportunity to ask questions in real time, and demonstrate the kind of commitment that can positively influence how lecturers perceive and support you. If you must miss a class due to illness or an emergency, inform your lecturer promptly, obtain notes from a classmate, and review the material before the next session.",
        ],
    },

    # ── SCHOLARSHIP ────────────────────────────────────────
    {
        "tag": "scholarship",
        "patterns": ["scholarship", "bursary", "funding", "financial aid", "school fees",
                     "tuition", "student loan", "sponsor", "grant", "fee payment"],
        "responses": [
            "Finding financial support for your education requires proactive research and early action. Begin by visiting your institution's financial aid or bursary office, as many available scholarships go unclaimed simply because students are unaware of them. Search reputable online scholarship portals for opportunities that match your field of study, nationality, and academic level. Apply as early as possible since most scholarships have strict deadlines. Invest time in writing a compelling personal statement that clearly articulates your academic goals, your financial situation, and your future aspirations. Also explore scholarships offered by local government bodies, NGOs, and professional associations in your chosen field.",
        ],
    },

    # ── CAREER ─────────────────────────────────────────────
    {
        "tag": "career",
        "patterns": ["career", "job", "internship", "future", "after graduation",
                     "work", "employment", "cv", "resume", "interview", "linkedin", "job market"],
        "responses": [
            "Building a strong career foundation begins well before graduation. Start developing your curriculum vitae now, even if your experience is limited, and update it regularly as you gain new skills, certifications, and achievements. Actively seek out internship and volunteer opportunities during your academic vacations, as practical work experience is highly valued by employers. Create a professional LinkedIn profile and begin networking with practitioners and alumni in your field. Attend career fairs organized by your institution. Remember that both technical expertise and strong interpersonal communication skills are essential for long-term career success.",
        ],
    },

    # ── INTERVIEW ──────────────────────────────────────────
    {
        "tag": "interview",
        "patterns": ["interview", "job interview", "interview tips", "how to interview",
                     "interview preparation", "interview questions"],
        "responses": [
            "Preparing effectively for a job interview requires research, practice, and presentation. Before the interview, research the organization thoroughly so that you understand their mission, values, and recent activities. Practice answering common interview questions such as telling them about yourself, describing your greatest strengths and weaknesses, and explaining why you want to work for them. Use the STAR method — Situation, Task, Action, Result — to structure your answers to behavioral questions. Dress professionally and arrive early. Bring a printed copy of your curriculum vitae. At the end of the interview, prepare at least two thoughtful questions to ask the interviewer, as this demonstrates genuine interest.",
        ],
    },

    # ── CV / RESUME ────────────────────────────────────────
    {
        "tag": "cv",
        "patterns": ["cv", "resume", "curriculum vitae", "how to write cv",
                     "cv tips", "build cv", "write resume"],
        "responses": [
            "A strong curriculum vitae is clear, concise, and tailored to the opportunity you are applying for. Include the following sections: personal information and contact details, a brief personal profile or objective statement, your educational qualifications in reverse chronological order, any work experience or internships, relevant skills, and any extracurricular achievements or certifications. Keep the document to one or two pages. Use a clean, professional font and consistent formatting throughout. Proofread carefully, as a single spelling or grammatical error can create a very poor first impression. Have a trusted person review your CV before submitting it.",
        ],
    },

    # ── LIBRARY ────────────────────────────────────────────
    {
        "tag": "library",
        "patterns": ["library", "book", "textbook", "resource", "journal",
                     "research", "reference", "where to find material", "study material"],
        "responses": [
            "There are numerous excellent resources available to support your academic work. Your institution's library, both its physical collection and any digital databases it subscribes to, should be your first point of reference. Google Scholar provides free access to a vast collection of peer-reviewed academic articles and research papers. OpenStax offers high-quality university-level textbooks at absolutely no cost. Khan Academy provides clear and well-structured lessons across a wide range of subjects. YouTube also hosts many outstanding educational channels that can effectively supplement your lecture notes.",
        ],
    },

    # ── GROUP WORK ─────────────────────────────────────────
    {
        "tag": "group_work",
        "patterns": ["group work", "group project", "team", "teamwork",
                     "collaborate", "group member", "classmate", "partner", "group assignment"],
        "responses": [
            "Successful group work depends on clear communication and mutual accountability from the very first meeting. Assign specific roles and responsibilities to each member so that everyone understands precisely what is expected of them. Set internal deadlines that fall one or two days before the actual submission deadline, giving the group sufficient time to review the combined work and correct any inconsistencies. Use collaborative tools such as Google Docs, which allows all members to work simultaneously and track contributions transparently. If disagreements arise within the group, address them openly and professionally at the earliest opportunity rather than allowing tension to accumulate.",
        ],
    },

    # ── PRESENTATION ───────────────────────────────────────
    {
        "tag": "presentation",
        "patterns": ["presentation", "present", "public speaking", "slides", "powerpoint",
                     "seminar presentation", "how to present", "stage fright"],
        "responses": [
            "Delivering an effective academic presentation requires thorough preparation and confident delivery. Know your material deeply rather than memorizing a script word for word, as this allows you to speak naturally and recover smoothly if you lose your place. Structure your presentation clearly with an introduction, well-organized main points, and a concise conclusion. Design your slides to support your speech rather than replace it — use minimal text and clear visuals. Practice delivering your presentation aloud multiple times before the actual day, ideally in front of a friend or family member. Speak slowly and clearly, make eye contact with your audience, and do not apologize for nervousness — most audiences cannot tell.",
        ],
    },

    # ── RESEARCH ───────────────────────────────────────────
    {
        "tag": "research",
        "patterns": ["research", "research paper", "literature review", "methodology",
                     "how to research", "find sources", "academic sources", "peer reviewed"],
        "responses": [
            "Conducting good academic research begins with clearly defining your research question or objective. Use credible, peer-reviewed sources such as academic journals, published textbooks, and reputable institutional websites. Google Scholar, your institution's library database, and platforms such as ResearchGate and JSTOR are excellent starting points. Evaluate every source critically by considering the author's credentials, the publication date, and whether the work has been peer-reviewed. Take organized notes and record full bibliographic details of every source as you go, as reconstructing references later is time-consuming and frustrating.",
        ],
    },

    # ── CONCENTRATION ──────────────────────────────────────
    {
        "tag": "concentration",
        "patterns": ["can't concentrate", "distracted", "concentration", "focus",
                     "phone distraction", "social media", "keep getting distracted", "attention"],
        "responses": [
            "Difficulty concentrating is one of the most common challenges students face, particularly in the age of smartphones and social media. The single most effective step you can take is to place your phone in another room or use an app blocker such as Forest or Cold Turkey while studying. Ensure your study environment is clean, quiet, and dedicated solely to studying. The Pomodoro Technique — twenty-five minutes of focused work followed by a five-minute break — is scientifically proven to improve concentration and reduce mental fatigue. Avoid studying in bed, as your brain associates that environment with sleep and relaxation rather than focused work.",
        ],
    },

    # ── SLEEP ──────────────────────────────────────────────
    {
        "tag": "sleep",
        "patterns": ["sleep", "tired", "sleepy", "insomnia", "can't sleep",
                     "how much sleep", "study all night", "pulling an all nighter", "all nighter"],
        "responses": [
            "Adequate sleep is absolutely essential for academic performance and overall wellbeing. Research consistently shows that sleep deprivation significantly impairs memory consolidation, problem-solving ability, concentration, and emotional regulation. Students generally require between seven and nine hours of sleep per night. Avoid pulling all-nighters before examinations — a well-rested brain with solid preparation will always outperform an exhausted brain that studied through the night. Establish a consistent sleep schedule by going to bed and waking up at the same time each day, including weekends where possible. Avoid screens for at least thirty minutes before bed, as the blue light interferes with your natural sleep cycle.",
        ],
    },

    # ── NUTRITION ──────────────────────────────────────────
    {
        "tag": "nutrition",
        "patterns": ["food", "eat", "nutrition", "diet", "brain food", "healthy eating",
                     "energy", "coffee", "caffeine", "snacks while studying"],
        "responses": [
            "What you eat has a direct and significant impact on your cognitive performance and ability to study effectively. Foods rich in omega-3 fatty acids, such as fish, nuts, and seeds, support brain health and memory function. Complex carbohydrates such as oats, brown rice, and whole grain bread provide sustained energy without the sharp crashes associated with sugary foods. Stay well hydrated throughout the day, as even mild dehydration impairs concentration and memory. While moderate caffeine consumption can improve alertness temporarily, excessive reliance on coffee or energy drinks can disrupt your sleep and ultimately reduce your academic performance.",
        ],
    },

    # ── EXERCISE ───────────────────────────────────────────
    {
        "tag": "exercise",
        "patterns": ["exercise", "workout", "physical activity", "sport", "gym",
                     "running", "walk", "active", "fitness", "healthy lifestyle"],
        "responses": [
            "Regular physical exercise is one of the most underutilized tools for academic improvement. Research consistently demonstrates that aerobic exercise increases blood flow to the brain, enhances memory consolidation, reduces stress and anxiety, and improves sleep quality — all of which directly benefit your studies. You do not need to spend hours at a gym; even a brisk thirty-minute walk three to four times per week produces significant cognitive benefits. Many students find that taking a short walk during study breaks helps them return to their work feeling refreshed and more focused.",
        ],
    },

    # ── ONLINE LEARNING ────────────────────────────────────
    {
        "tag": "online_learning",
        "patterns": ["online learning", "online course", "e-learning", "distance learning",
                     "coursera", "udemy", "edx", "online class", "mooc", "virtual learning"],
        "responses": [
            "Online learning offers tremendous flexibility and access to world-class educational content. Platforms such as Coursera, edX, Udemy, and Khan Academy offer courses taught by leading universities and industry experts, many of which are free or very affordable. To succeed in online learning, treat it with the same discipline and commitment you would give to a formal classroom course. Set aside dedicated study time each day, actively engage with the material rather than passively watching videos, complete all assignments, and participate in any available discussion forums. Earning recognized online certifications can also significantly strengthen your curriculum vitae.",
        ],
    },

    # ── EXTRACURRICULAR ────────────────────────────────────
    {
        "tag": "extracurricular",
        "patterns": ["extracurricular", "club", "society", "volunteer", "student union",
                     "activities", "student organization", "leadership", "sports team"],
        "responses": [
            "Participating in extracurricular activities alongside your academic studies offers significant personal and professional benefits. Student clubs, societies, volunteer work, and sports teams help you develop leadership, teamwork, communication, and time management skills that employers value highly. They also provide excellent networking opportunities and can make your curriculum vitae stand out from those of other candidates. The key is balance — choose one or two activities you are genuinely passionate about and commit to them consistently, rather than joining many organizations superficially.",
        ],
    },

    # ── NETWORKING ─────────────────────────────────────────
    {
        "tag": "networking",
        "patterns": ["networking", "network", "connections", "professional network",
                     "meet professionals", "linkedin", "alumni", "industry contacts"],
        "responses": [
            "Building a professional network while you are still a student gives you a significant advantage when you enter the job market. Start by connecting with your classmates on LinkedIn, as they will be your professional peers throughout your career. Connect with your lecturers and ask to be introduced to their professional contacts where appropriate. Attend industry events, career fairs, and guest lectures at your institution. When reaching out to professionals, be genuine, specific about your interest, and respectful of their time. Remember that networking is about building mutually beneficial relationships over time, not simply asking for favors.",
        ],
    },

    # ── TECHNOLOGY IN STUDY ────────────────────────────────
    {
        "tag": "study_tools",
        "patterns": ["study app", "study tools", "apps for studying", "notion", "anki",
                     "flashcards app", "best app for students", "study software", "google docs"],
        "responses": [
            "There are several excellent digital tools that can significantly enhance your productivity as a student. Anki is a powerful flashcard application that uses spaced repetition to help you memorize information efficiently. Notion is an extremely versatile tool for organizing notes, managing projects, and tracking your study schedule. Google Docs and Google Drive make collaboration on group projects straightforward and efficient. The Forest app helps you stay focused by blocking distracting websites and apps during study sessions. Grammarly assists with proofreading and improving the clarity of your written assignments. Zotero is an excellent free tool for managing your research references and generating citations automatically.",
        ],
    },

]


def preprocess_input(text):
    text  = text.lower()
    text  = re.sub(r"[^\w\s]", "", text)
    words = text.split()
    return [stemmer.stem(w) for w in words if w not in stop_words]


def get_response(user_input):
    tokens     = preprocess_input(user_input)
    best_tag   = None
    best_score = 0

    for entry in KNOWLEDGE_BASE:
        score = 0
        for pattern in entry["patterns"]:
            pattern_tokens = preprocess_input(pattern)
            matches = sum(1 for t in pattern_tokens if t in tokens)
            if pattern.lower() in user_input.lower():
                matches += 2
            score = max(score, matches)

        if score > best_score:
            best_score = score
            best_tag   = entry["tag"]

    if best_score > 0 and best_tag:
        for entry in KNOWLEDGE_BASE:
            if entry["tag"] == best_tag:
                return random.choice(entry["responses"])

    fallbacks = [
        "That is a thoughtful question. I am specifically designed to assist with school-related topics such as examinations, study techniques, time management, programming, mental health, and career preparation. Could you rephrase your question in one of those areas?",
        "I appreciate your question, though it falls slightly outside my area of specialization. I am designed to help students with academic topics. Please feel free to ask me about studying strategies, assignments, grades, career planning, or any other aspect of school life.",
        "I am not entirely certain how to respond to that. I work best with school and academic questions. Try asking me about exam preparation, note-taking, time management, stress management, or career advice and I will do my very best to help.",
    ]
    return random.choice(fallbacks)


if __name__ == "__main__":
    print("=" * 55)
    print("  SchoolBot — CSC 309 Mini Project #1")
    print("  Type 'bye' to exit")
    print("=" * 55)
    while True:
        user = input("\nYou: ").strip()
        if not user:
            continue
        response = get_response(user)
        print(f"\nBot: {response}")
        if any(w in user.lower() for w in ["bye", "exit", "quit"]):
            break
