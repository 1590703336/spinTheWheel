"""Static game data shared by both the legacy Tkinter app and the new web API."""

from __future__ import annotations

from typing import Dict, List

WINNING_SCORE = 30

SPECIAL_TILES = {
    4: "forward",
    11: "backward",
    16: "forward",
    22: "backward",
    26: "backward",
}

# NOTE: This is directly copied from `spinTheWheel.py` so the content stays in sync.
GAME_DATA: Dict[str, List[Dict[str, str]]] = {
    "FINANCIAL WELLBEING": [
        {
            "q": "What is financial literacy?",
            "a": "This is the knowledge, financial skills and ability to effectively manage the economic well-being of individuals;\n\nto manage your money effectively, which includes making informed decisions about budgeting, saving, investing, and managing debt",
        },
        {
            "q": "How does financial well-being affect student success?",
            "a": "Lack of financial well-being = financial stress => less focus on studies (due to pressure like more working hours).\n\nIn other words, financial stress hinders a student’s ability to succeed academically\n\nStudents experiencing financial stress find it challenging to navigate relationships with wealthier peers, often leading to feelings of isolation and embarrassment.\n\nInability to purchase textbooks and other essentials.\nHaving to prioritize work over studies",
        },
        {
            "q": "Why should students learn how to budget?",
            "a": "To avoid overspending and debt\n\nBalance essential expenses and leaving you with some pocket money.\n\nIdentifying and correcting spending patterns\n\nBuilding emergency savings\n\nPreparation for financial success after graduation",
        },
        {
            "q": "What are some huge expenses in Canada as a student?",
            "a": "(Personal Answer based on experience)",
        },
    ],
    "SELF REGULATION AND GOAL SETTING": [
        {
            "q": "What are common challenges first-year students face?",
            "a": "Difference in culture\n\nInterpretation of university policies\n\nComprehension of English either in school setting or regular conversations\n\nEngaging with the university as a whole",
        },
        {
            "q": "What advice do you give to students who are going through something difficult?",
            "a": "Stay steadfast in your goals\n\nBe more specific with your goals. Figure out whether they are short or long term.\nDifferent sacrifices need to be made for your goals, and be more detailed with your planning\n\nGoal setting: one step at a time, learn & adapt, never give up, win your battle!",
        },
        {
            "q": "What is self-regulation?",
            "a": "This can be thought of how much control we have over ourselves, through mental thoughts and physical actions.\n\nCould be referred to as discipline or self-control. Therefore, it has a lot of influence on goal-setting.",
        },
        {
            "q": "How can students achieve their goals through self-regulation?",
            "a": "strategically managing their thoughts, emotions, and behaviors\n\ngoal-setting, planning, monitoring progress, and reflecting on their learning",
        },
        {
            "q": "How do you think university will prepare you for your future goals?",
            "a": "(Personal Answer)",
        },
        {
            "q": "What activities outside of university will also help you in the future?",
            "a": "(Personal Answer)",
        },
    ],
    "U OF A CAREER CENTRE": [
        {
            "q": "What are some skills acquired at university that will help (international) students in their employment?",
            "a": "Communication skills are an important foundation for developing positive and constructive working relationships.\n\nEFFECTIVE COMMUNICATION: learning and sharing information, talking clearly, listening carefully, and interacting actively.\n\nCultural awareness, which means being sensitive to the differences and similarities between two cultures when communicating with people from different cultural backgrounds.\n\nHelps you understand how cultural differences may affect individuals when forming their unique personalities, perceptions, and interactions with others.",
        },
        {
            "q": "How can international students build their employability skills?",
            "a": "Networking, a great way for students and young professionals to get their foot in the door and make meaningful connections.\nIt is building relationships before you need them. Check out networking events specific to your areas of interest\n\nBuild work experience: internships, summer jobs, part-time jobs.\nWith work experience, you will learn new things and grow the transferable skills developed in the classroom",
        },
        {
            "q": "Effective Communication:",
            "a": "> Participating in group projects and discussions\n\n> Delivering a presentation in public\n\n> Writing an essay or a lab report",
        },
        {
            "q": "What career supports on campus are valuable?",
            "a": "UofA Career Centre. You can get an appointment with a Career Advisor to help you in your career development or work search. They also help with interview preparation.\n\nThe Centre for Writers. Offers one-on-one advising to review written work and provide insights on the different styles of writing papers, and email etiquette <written and physical communication>\n\nInternational Student Services. Offers career advising within Canadian work culture context. Can connect you to the appropriate resources to succeed at working in Canada",
        },
        {
            "q": "What programs are beneficial for international students?",
            "a": "UofA Career Centre: Graduate Internship Program. Provides Candian work experience.\n\nInternational Student Services: I-Work! Workshops",
        },
    ],
    "WRITING A RESUME AND COVER LETTER": [
        {
            "q": "What do you need to find work experience?",
            "a": "A goal. What kind of experience do you want? Work and skill experience or a paycheck?\n\nA resume (a document that contains your jobs or volunteer experiences)\n\nA cover letter, which is carefully adapted for ach position you are applying for\n\nAn interview.",
        },
        {
            "q": "What should be in your resume?",
            "a": "Contact information\n\nEducation, Certificates & Awards, Skills\n\nExperiences: Work, Volunteering, Clubs, Leadership Opportunities\n\nAttributes",
        },
        {
            "q": "What are some points to note when formatting your resume?",
            "a": "Arrange your experience with the latest information as the first one; in a reverse chronological order\n\nChoose sections to include depending on the position you are applying\n\nUse a template to guide you\n\nPersonalize your template to fit your information\n\nBe consistent with considered font size and colour\n\nUse bullet points and margins\n\nDo not go beyond two pages. That's the max.\n\nProofread to ensure that there are no spelling, grammar or punctuation errors.",
        },
        {
            "q": "What are the elements of a cover letter?",
            "a": "Name, address, date; name of person and title, name of organisation, address\n\nSalutation: Dear …\n\nOpening Paragraph: Introduce yourself\n\nBody: State your intent\n\nClosing Paragraph: be appreciative and passionate\n\nSincerely, …(your name typed underneath your signature)",
        },
    ],
    "PREPARING FOR AN INTERVIEW": [
        {
            "q": "In what situations might you need to be interviewed?",
            "a": "When applying for a job\n\nWhen applying for a volunteer position\n\nWhen applying for a promotion or an internal role change\n\n(For research purposes\n\nFor investigations\n\nFor journalism/talk shows)",
        },
        {
            "q": "What kind of questions do employers ask at job interviews?",
            "a": "About the individual\n\nAbout the individual’s experience\n\nAbout problem-solving\n\nAbout teamwork\n\nAbout the position and the company",
        },
        {
            "q": "What do you say in a job interview?",
            "a": "Describe yourself\n\nDescribe your profile\n\nState clearly why you want the job\n\nShow that you are the best candidate for the position\n\nTalk about your strengths and weaknesses, as well",
        },
        {
            "q": "Why do employers and managers want to interview potential workers?",
            "a": "To assess a candidate’s skills, experience and cultural fit beyond what is shown on the resume\n\nTo clariy info on the resume\n\nTo assess long-term potential of candidate. Candidate who can grow the company and adapt to future business needs are those being desired for.\n\nTo minimize hiring mistakes; to increase the likelihood of a successful hire, and to help avoid the costs associated with high turnover.",
        },
        {
            "q": "If you were an employer, what questions would you ask a student?",
            "a": "(Personnal Answer)",
        },
    ],
    "TRANSFERABLE AND (INTERCULTURAL) COMMUNICATION SKILLS": [
        {
            "q": "What skills are important in a Canadian workplace?",
            "a": "Proper language skills are necessary for effective workplace communication. Understanding the communication style helps avoid miscommunication.\nDirect and polite email etiquette is an important part of Canadian communication.\n\nEmbracing cultural diversity in Canada can be enriching. Making assumptions about people may be incorrect and hurtful",
        },
        {
            "q": "How does one organize themselves to be productive?",
            "a": "Being independent is expected in the classroom and workplace\n\nBeing able to organize ourselves and manage our time is really essential.\n\nCreating a schedule and breaking up bigger tasks facilitates productivity\n\nBeing able to prioritize helps you to manage tasks",
        },
        {
            "q": "Collaboration skills and Do you think employees work alone?",
            "a": "effective communication\n\nResponsibilities and expectations are shared.\n\nNavigate difficult situations with team members for effective working.\n\nGiving and receiving honest and constructive feedback. Great and room for improvement feedbacks to improve performance",
        },
        {
            "q": "How do we overcome challenges, according to Sofia Elgueta?",
            "a": "Crititcla thinking and problem solving skills are really important in the workplace\n\nConflict resolution skills for team. Good listening and expressing yourself assertively are important conflict resolution skills\n\nWork on problems between people as they often come from poor communication or misunderstandings. These problems may stem from cultural or communication style differences",
        },
        {
            "q": "What are some similarities between the classroom and the workplace?",
            "a": "(Personal Answer)",
        },
    ],
}

