import os
import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
import textwrap
import requests
import json
import threading
import re
from pathlib import Path


def load_local_env():
    """
    将项目根目录下的 .env 内容载入环境变量（不覆盖已有变量）。
    格式：KEY=VALUE，支持 # 注释以及用引号包裹的值。
    """
    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        return

    try:
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            if not key:
                continue

            if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                value = value[1:-1]

            os.environ.setdefault(key, value)
    except OSError:
        pass


def get_env_value(name, default=""):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip()


load_local_env()

# ==========================================
# --- CONFIG / 配置区域 ---
# ==========================================

# 建议：在项目根目录创建 .env，设置 OPENROUTER_API_KEY=your-key
OPENROUTER_API_KEY = get_env_value("OPENROUTER_API_KEY")
YOUR_SITE_URL = get_env_value("YOUR_SITE_URL", "https://your-site-url.com") # OpenRouter 建议填写
YOUR_APP_NAME = get_env_value("YOUR_APP_NAME", "Double Spin Wheel Game")    # OpenRouter 建议填写

# 游戏参数
WINNING_SCORE = 30  # 修改为30格

# 特殊格子配置 {格子索引: 类型}
# 类型: 'forward' (前进), 'backward' (后退)
SPECIAL_TILES = {
    4: 'forward',
    11: 'backward',
    16: 'forward',
    22: 'backward',
    26: 'backward'
}

# 新的数据结构：Key是组名，Value是列表，列表里包含字典 {'q': 问题, 'a': 答案}
GAME_DATA = {
    "FINANCIAL WELLBEING": [
        {
            "q": "What is financial literacy?",
            "a": "This is the knowledge, financial skills and ability to effectively manage the economic well-being of individuals;\n\nto manage your money effectively, which includes making informed decisions about budgeting, saving, investing, and managing debt"
        },
        {
            "q": "How does financial well-being affect student success?",
            "a": "Lack of financial well-being = financial stress => less focus on studies (due to pressure like more working hours).\n\nIn other words, financial stress hinders a student’s ability to succeed academically\n\nStudents experiencing financial stress find it challenging to navigate relationships with wealthier peers, often leading to feelings of isolation and embarrassment.\n\nInability to purchase textbooks and other essentials.\nHaving to prioritize work over studies"
        },
        {
            "q": "Why should students learn how to budget?",
            "a": "To avoid overspending and debt\n\nBalance essential expenses and leaving you with some pocket money.\n\nIdentifying and correcting spending patterns\n\nBuilding emergency savings\n\nPreparation for financial success after graduation"
        },
        {
            "q": "What are some huge expenses in Canada as a student?",
            "a": "(Personal Answer based on experience)" 
        }
    ],
    "SELF REGULATION AND GOAL SETTING": [
        {
            "q": "What are common challenges first-year students face?",
            "a": "Difference in culture\n\nInterpretation of university policies\n\nComprehension of English either in school setting or regular conversations\n\nEngaging with the university as a whole"
        },
        {
            "q": "What advice do you give to students who are going through something difficult?",
            "a": "Stay steadfast in your goals\n\nBe more specific with your goals. Figure out whether they are short or long term.\nDifferent sacrifices need to be made for your goals, and be more detailed with your planning\n\nGoal setting: one step at a time, learn & adapt, never give up, win your battle!"
        },
        {
            "q": "What is self-regulation?",
            "a": "This can be thought of how much control we have over ourselves, through mental thoughts and physical actions.\n\nCould be referred to as discipline or self-control. Therefore, it has a lot of influence on goal-setting."
        },
        {
            "q": "How can students achieve their goals through self-regulation?",
            "a": "strategically managing their thoughts, emotions, and behaviors\n\ngoal-setting, planning, monitoring progress, and reflecting on their learning"
        },
        {
            "q": "How do you think university will prepare you for your future goals?",
            "a": "(Personal Answer)"
        },
        {
            "q": "What activities outside of university will also help you in the future?",
            "a": "(Personal Answer)"
        }
    ],
    "U OF A CAREER CENTRE": [
        {
            "q": "What are some skills acquired at university that will help (international) students in their employment?",
            "a": "Communication skills are an important foundation for developing positive and constructive working relationships.\n\nEFFECTIVE COMMUNICATION: learning and sharing information, talking clearly, listening carefully, and interacting actively.\n\nCultural awareness, which means being sensitive to the differences and similarities between two cultures when communicating with people from different cultural backgrounds.\n\nHelps you understand how cultural differences may affect individuals when forming their unique personalities, perceptions, and interactions with others."
        },
        {
            "q": "How can international students build their employability skills?",
            "a": "Networking, a great way for students and young professionals to get their foot in the door and make meaningful connections.\nIt is building relationships before you need them. Check out networking events specific to your areas of interest\n\nBuild work experience: internships, summer jobs, part-time jobs.\nWith work experience, you will learn new things and grow the transferable skills developed in the classroom"
        },
        {
            "q": "Effective Communication:",
            "a": "> Participating in group projects and discussions\n\n> Delivering a presentation in public\n\n> Writing an essay or a lab report"
        },
        {
            "q": "What career supports on campus are valuable?",
            "a": "UofA Career Centre. You can get an appointment with a Career Advisor to help you in your career development or work search. They also help with interview preparation.\n\nThe Centre for Writers. Offers one-on-one advising to review written work and provide insights on the different styles of writing papers, and email etiquette <written and physical communication>\n\nInternational Student Services. Offers career advising within Canadian work culture context. Can connect you to the appropriate resources to succeed at working in Canada"
        },
        {
            "q": "What programs are beneficial for international students?",
            "a": "UofA Career Centre: Graduate Internship Program. Provides Candian work experience.\n\nInternational Student Services: I-Work! Workshops"
        }
    ],
    "WRITING A RESUME AND COVER LETTER": [
        {
            "q": "What do you need to find work experience?",
            "a": "A goal. What kind of experience do you want? Work and skill experience or a paycheck?\n\nA resume (a document that contains your jobs or volunteer experiences)\n\nA cover letter, which is carefully adapted for ach position you are applying for\n\nAn interview."
        },
        {
            "q": "What should be in your resume?",
            "a": "Contact information\n\nEducation, Certificates & Awards, Skills\n\nExperiences: Work, Volunteering, Clubs, Leadership Opportunities\n\nAttributes"
        },
        {
            "q": "What are some points to note when formatting your resume?",
            "a": "Arrange your experience with the latest information as the first one; in a reverse chronological order\n\nChoose sections to include depending on the position you are applying\n\nUse a template to guide you\n\nPersonalize your template to fit your information\n\nBe consistent with considered font size and colour\n\nUse bullet points and margins\n\nDo not go beyond two pages. That's the max.\n\nProofread to ensure that there are no spelling, grammar or punctuation errors."
        },
        {
            "q": "What are the elements of a cover letter?",
            "a": "Name, address, date; name of person and title, name of organisation, address\n\nSalutation: Dear …\n\nOpening Paragraph: Introduce yourself\n\nBody: State your intent\n\nClosing Paragraph: be appreciative and passionate\n\nSincerely, …(your name typed underneath your signature)"
        }
    ],
    "PREPARING FOR AN INTERVIEW": [
        {
            "q": "In what situations might you need to be interviewed?",
            "a": "When applying for a job\n\nWhen applying for a volunteer position\n\nWhen applying for a promotion or an internal role change\n\n(For research purposes\n\nFor investigations\n\nFor journalism/talk shows)"
        },
        {
            "q": "What kind of questions do employers ask at job interviews?",
            "a": "About the individual\n\nAbout the individual’s experience\n\nAbout problem-solving\n\nAbout teamwork\n\nAbout the position and the company"
        },
        {
            "q": "What do you say in a job interview?",
            "a": "Describe yourself\n\nDescribe your profile\n\nState clearly why you want the job\n\nShow that you are the best candidate for the position\n\nTalk about your strengths and weaknesses, as well"
        },
        {
            "q": "Why do employers and managers want to interview potential workers?",
            "a": "To assess a candidate’s skills, experience and cultural fit beyond what is shown on the resume\n\nTo clariy info on the resume\n\nTo assess long-term potential of candidate. Candidate who can grow the company and adapt to future business needs are those being desired for.\n\nTo minimize hiring mistakes; to increase the likelihood of a successful hire, and to help avoid the costs associated with high turnover."
        },
        {
            "q": "If you were an employer, what questions would you ask a student?",
            "a": "(Personnal Answer)"
        }
    ],
    "TRANSFERABLE AND (INTERCULTURAL) COMMUNICATION SKILLS": [
        {
            "q": "What skills are important in a Canadian workplace?",
            "a": "Proper language skills are necessary for effective workplace communication. Understanding the communication style helps avoid miscommunication.\nDirect and polite email etiquette is an important part of Canadian communication.\n\nEmbracing cultural diversity in Canada can be enriching. Making assumptions about people may be incorrect and hurtful"
        },
        {
            "q": "How does one organize themselves to be productive?",
            "a": "Being independent is expected in the classroom and workplace\n\nBeing able to organize ourselves and manage our time is really essential.\n\nCreating a schedule and breaking up bigger tasks facilitates productivity\n\nBeing able to prioritize helps you to manage tasks"
        },
        {
            "q": "Collaboration skills and Do you think employees work alone?",
            "a": "effective communication\n\nResponsibilities and expectations are shared.\n\nNavigate difficult situations with team members for effective working.\n\nGiving and receiving honest and constructive feedback. Great and room for improvement feedbacks to improve performance"
        },
        {
            "q": "How do we overcome challenges, according to Sofia Elgueta?",
            "a": "Crititcla thinking and problem solving skills are really important in the workplace\n\nConflict resolution skills for team. Good listening and expressing yourself assertively are important conflict resolution skills\n\nWork on problems between people as they often come from poor communication or misunderstandings. These problems may stem from cultural or communication style differences"
        },
        {
            "q": "What are some similarities between the classroom and the workplace?",
            "a": "(Personal Answer)"
        }
    ]
}

# 窗口设置 (加大宽度以容纳排行榜和地图)
WINDOW_WIDTH = 1600 
WINDOW_HEIGHT = 1050  
WHEEL_RADIUS = 350   
CANVAS_HEIGHT = 750  

# 重新计算中心点 (针对左侧画布，基于新的宽度调整)
# 左侧区域大约占 900-1000px
CENTER_X = 450 
CENTER_Y = CANVAS_HEIGHT // 2 

# 美化配色盘
COLORS = [
    "#FF6B6B", "#4ECDC4", "#FFE66D", "#1A535C", 
    "#FF9F1C", "#2EC459", "#CBF3F0", "#FFBF69"
]
# 飞行器颜色库
SPACESHIP_COLORS = [
    "#E74C3C", "#2ECC71", "#3498DB", "#9B59B6", "#F1C40F", "#E67E22",
    "#1ABC9C", "#34495E", "#D35400", "#C0392B", "#16A085", "#8E44AD"
]

# 界面风格 - 飞行棋主题
BG_COLOR = "#F0F2F5"
SIDEBAR_BG = "#E0E5EC"
MAP_BG = "#FDFBF7" # 米色/纸张色背景
MAP_PATH_COLORS = ["#FF6B6B", "#4ECDC4", "#FFE66D", "#45B7D1"] # 红绿黄蓝循环
BUTTON_FONT = ("Helvetica", 14, "bold")
LABEL_FONT = ("Helvetica", 28, "bold")
WHEEL_TEXT_FONT = ("Helvetica", 14, "bold")

# 展示问答的字体
QUESTION_BIG_FONT = ("Helvetica", 24, "bold")
QUESTION_SMALL_FONT = ("Helvetica", 14, "italic") 
ANSWER_FONT = ("Helvetica", 16)        
AI_FEEDBACK_FONT = ("Helvetica", 16, "italic")

# ==========================================
# --- MAIN CODE / 主程序代码 ---
# ==========================================

class SpinWheelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Double Spin Wheel Game + Flying Chess")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(True, True) 
        self.root.configure(bg=BG_COLOR)

        # 游戏状态
        self.phase = 0
        self.current_items = list(GAME_DATA.keys()) 
        self.selected_group = None
        self.selected_question_data = None 
        
        # 动画参数
        self.angle = 0        
        self.velocity = 0     
        self.friction = 0.98
        self.is_spinning = False

        # 闪烁效果参数
        self.flash_map = {}
        self.flash_count = 0
        self.flash_index = -1
        self.flash_callback = None

        # 排行榜数据 {name: score} 和 玩家颜色 {name: color}
        self.scores = {}
        self.player_colors = {}
        self.winner = None
        
        # UI 控件引用
        self.name_entry = None
        self.answer_text = None
        self.input_window_name = None
        self.input_window_answer = None

        self._setup_layout()
        self.draw_wheel()
        self.update_leaderboard()
        self.draw_map()

    def _setup_layout(self):
        """初始化三列布局：游戏区 | 排行榜 | 地图"""
        # 主容器
        self.main_container = tk.Frame(self.root, bg=BG_COLOR)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # --- 最右侧：地图区域 (Flying Chess Map) ---
        self.map_panel = tk.Frame(self.main_container, bg=MAP_BG, width=400)
        self.map_panel.pack(side=tk.RIGHT, fill=tk.Y)
        self.map_panel.pack_propagate(False)

        # 地图标题
        tk.Label(self.map_panel, text="✈️ FLYING CHESS ✈️", font=("Helvetica", 18, "bold"), bg=MAP_BG, fg="#2C3E50").pack(pady=20)
        
        self.map_canvas = tk.Canvas(self.map_panel, bg=MAP_BG, highlightthickness=0)
        self.map_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- 中右侧：排行榜区域 (Leaderboard) ---
        self.leaderboard_panel = tk.Frame(self.main_container, bg=SIDEBAR_BG, width=300)
        self.leaderboard_panel.pack(side=tk.RIGHT, fill=tk.Y)
        self.leaderboard_panel.pack_propagate(False) # 固定宽度

        tk.Label(self.leaderboard_panel, text="🏆 LEADERBOARD 🏆", font=("Helvetica", 18, "bold"), bg=SIDEBAR_BG, fg="#1A535C").pack(pady=30)
        
        # 排行榜列表框
        self.leaderboard_list = tk.Listbox(
            self.leaderboard_panel, 
            font=("Courier", 14), 
            bg="white", 
            fg="#333333",
            bd=0,
            relief="flat",
            height=30
        )
        self.leaderboard_list.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # --- 左侧：游戏区域 ---
        self.left_panel = tk.Frame(self.main_container, bg=BG_COLOR)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 标题栏
        self.title_frame = tk.Frame(self.left_panel, bg=BG_COLOR, height=150)
        self.title_frame.pack_propagate(False) 
        self.title_frame.pack(pady=20, fill=tk.X)
        
        self.info_label = tk.Label(
            self.title_frame, 
            text="Ready? Click SPIN to select a Group!", 
            font=LABEL_FONT, 
            bg=BG_COLOR, 
            fg="#333333",
            wraplength=700
        )
        self.info_label.place(relx=0.5, rely=0.5, anchor="center")

        # 画布
        self.canvas = tk.Canvas(
            self.left_panel, 
            bg=BG_COLOR, 
            highlightthickness=0,
            height=CANVAS_HEIGHT
        )
        self.canvas.pack(pady=10, fill=tk.BOTH, expand=True)

        # 按钮区
        self.btn_frame = tk.Frame(self.left_panel, bg=BG_COLOR)
        self.btn_frame.pack(pady=20, side=tk.BOTTOM)

        self.spin_btn = tk.Button(
            self.btn_frame, 
            text="SPIN WHEEL", 
            command=self.start_spin, 
            font=BUTTON_FONT, 
            bg="#28a745", 
            fg="black", 
            activeforeground="black",
            width=20, 
            height=2,
            bd=0, cursor="hand2"
        )
        self.spin_btn.pack(side=tk.LEFT, padx=20)

        self.reset_btn = tk.Button(
            self.btn_frame, 
            text="RESET GAME", 
            command=self.reset_game, 
            font=BUTTON_FONT, 
            bg="#dc3545", 
            fg="black", 
            activeforeground="black",
            width=15, 
            height=2,
            bd=0, cursor="hand2"
        )
        self.reset_btn.pack(side=tk.LEFT, padx=20)
        
        # 调试按钮
        self.debug_btn = tk.Button(
            self.btn_frame, 
            text="TEST API", 
            command=self.test_api, 
            font=("Helvetica", 10, "bold"), 
            bg="#607D8B", 
            fg="white", 
            width=10, 
            height=2,
            bd=0, cursor="hand2"
        )
        self.debug_btn.pack(side=tk.LEFT, padx=20)

    def test_api(self):
        """测试 API 连接"""
        if not self._ensure_api_key():
            return

        self.info_label.config(text="Testing API connection...", fg="blue")
        threading.Thread(target=self._run_api_test).start()

    def _ensure_api_key(self):
        """检查 API Key 是否存在"""
        if OPENROUTER_API_KEY:
            return True

        warning = "缺少 OPENROUTER_API_KEY，请在 .env 中配置。"
        self.info_label.config(text=warning, fg="red")
        messagebox.showerror(
            "Missing API Key",
            "未检测到 OPENROUTER_API_KEY。\n请在项目根目录创建 .env 文件并写入：\nOPENROUTER_API_KEY=你的密钥"
        )
        return False

    def _run_api_test(self):
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": YOUR_SITE_URL,
                    "X-Title": YOUR_APP_NAME,
                },
                data=json.dumps({
                    "model": "openai/gpt-oss-20b:free",
                    "messages": [{"role": "user", "content": "Hi"}]
                }),
                timeout=10
            )
            
            if response.status_code == 200:
                self.root.after(0, lambda: messagebox.showinfo("API Test", "✅ API Connection Successful!"))
                self.root.after(0, lambda: self.info_label.config(text="API OK. Ready to play!", fg="#333333"))
            else:
                error_msg = f"Error: {response.status_code}\n{response.text}"
                self.root.after(0, lambda: messagebox.showerror("API Test Failed", error_msg))
                self.root.after(0, lambda: self.info_label.config(text="API Error!", fg="red"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("API Test Failed", f"Connection Error:\n{str(e)}"))
            self.root.after(0, lambda: self.info_label.config(text="Connection Failed", fg="red"))

    def update_leaderboard(self):
        """刷新右侧排行榜"""
        self.leaderboard_list.delete(0, tk.END)
        # 按分数降序排列
        sorted_scores = sorted(self.scores.items(), key=lambda item: item[1], reverse=True)
        
        if not sorted_scores:
            self.leaderboard_list.insert(tk.END, "No scores yet!")
        
        rank = 1
        for name, score in sorted_scores:
            display_text = f"{rank}. {name[:10]:<10} : {score}"
            self.leaderboard_list.insert(tk.END, display_text)
            rank += 1
        
        # 刷新排行榜的同时刷新地图
        self.draw_map()

    def get_board_coords(self, step_index, total_steps, w, h, margin=20):
        """
        计算棋盘格坐标：S 型 (Snake) 路径，从左下角开始往上
        """
        cols = 5
        rows = math.ceil((total_steps + 1) / cols) 
        
        draw_w = w - margin * 2
        draw_h = h - margin * 2
        
        cell_w = draw_w / cols
        cell_h = draw_h / rows
        
        # 限制范围
        safe_index = min(step_index, total_steps)
        
        # 计算行列
        row_idx = safe_index // cols
        col_idx = safe_index % cols
        
        # Y轴翻转：row 0 在最下方
        visual_row = (rows - 1) - row_idx
        
        # S型翻转：偶数行(0,2..)从左到右，奇数行(1,3..)从右到左
        if row_idx % 2 == 1:
            visual_col = (cols - 1) - col_idx
        else:
            visual_col = col_idx
            
        x = margin + visual_col * cell_w + cell_w / 2
        y = margin + visual_row * cell_h + cell_h / 2
        
        return x, y, cell_w, cell_h

    def draw_map(self):
        """绘制飞行棋风格地图"""
        self.map_canvas.delete("all")
        
        w = self.map_canvas.winfo_width() or 400
        h = self.map_canvas.winfo_height() or 700
        margin = 30
        
        total_steps = WINNING_SCORE 
        
        # 1. 绘制路径连接线
        line_points = []
        for i in range(total_steps + 1):
            cx, cy, _, _ = self.get_board_coords(i, total_steps, w, h, margin)
            line_points.append(cx)
            line_points.append(cy)
        
        if len(line_points) > 2:
            self.map_canvas.create_line(line_points, fill="#BDC3C7", width=4, capstyle=tk.ROUND, joinstyle=tk.ROUND)

        # 2. 绘制棋盘格子
        for i in range(total_steps + 1):
            cx, cy, cw, ch = self.get_board_coords(i, total_steps, w, h, margin)
            
            # 格子尺寸
            tile_size = min(cw, ch) * 0.65
            
            # 颜色循环
            color = MAP_PATH_COLORS[i % len(MAP_PATH_COLORS)]
            
            # 特殊格子：起点和终点
            if i == 0:
                self.map_canvas.create_oval(cx-tile_size, cy-tile_size, cx+tile_size, cy+tile_size, fill="#2ECC71", outline="white", width=2)
                self.map_canvas.create_text(cx, cy, text="START", fill="white", font=("Arial", 9, "bold"))
            elif i == total_steps:
                # 终点大格子
                self.map_canvas.create_oval(cx-tile_size*1.2, cy-tile_size*1.2, cx+tile_size*1.2, cy+tile_size*1.2, fill="#F1C40F", outline="white", width=3)
                self.map_canvas.create_text(cx, cy, text="WIN", fill="white", font=("Arial", 10, "bold"))
            
            # 检查是否为特殊格子
            elif i in SPECIAL_TILES:
                effect = SPECIAL_TILES[i]
                if effect == 'forward':
                    # 绿色前进格
                    self.map_canvas.create_rectangle(cx-tile_size/2, cy-tile_size/2, cx+tile_size/2, cy+tile_size/2, fill="#2ECC71", outline="white", width=2)
                    self.map_canvas.create_text(cx, cy, text=">>", fill="white", font=("Arial", 10, "bold"))
                else:
                    # 红色后退格
                    self.map_canvas.create_rectangle(cx-tile_size/2, cy-tile_size/2, cx+tile_size/2, cy+tile_size/2, fill="#E74C3C", outline="white", width=2)
                    self.map_canvas.create_text(cx, cy, text="<<", fill="white", font=("Arial", 10, "bold"))
            else:
                # 普通格子
                self.map_canvas.create_rectangle(cx-tile_size/2, cy-tile_size/2, cx+tile_size/2, cy+tile_size/2, fill=color, outline="white", width=1)
                if i % 5 == 0:
                    self.map_canvas.create_text(cx, cy, text=str(i), fill="white", font=("Arial", 8, "bold"))

        # 3. 绘制玩家飞机
        tile_occupancy = {} # {step_index: count}
        
        for name, score in self.scores.items():
            # 限制分数在 0 - WINNING_SCORE
            current_step = max(0, min(score, WINNING_SCORE))
            
            # 获取该位置已有的玩家数
            count = tile_occupancy.get(current_step, 0)
            tile_occupancy[current_step] = count + 1
            
            # 获取格子中心坐标
            cx, cy, _, _ = self.get_board_coords(current_step, total_steps, w, h, margin)
            
            # 计算偏移 (围绕中心点散开)
            offset_x = 0
            offset_y = 0
            if count == 1: offset_x = 8; offset_y = 8
            elif count == 2: offset_x = -8; offset_y = 8
            elif count == 3: offset_x = 8; offset_y = -8
            elif count >= 4: offset_x = -8; offset_y = -8
            
            px = cx + offset_x
            py = cy + offset_y
            
            # 获取/分配颜色
            if name not in self.player_colors:
                self.player_colors[name] = random.choice(SPACESHIP_COLORS)
            p_color = self.player_colors[name]
            
            # 绘制飞机 (三角形)
            p_size = 10
            points = [
                px, py - p_size,           # Top
                px - p_size + 2, py + p_size - 2, # Bottom Left
                px, py + p_size - 5,       # Bottom Center (indent)
                px + p_size - 2, py + p_size - 2  # Bottom Right
            ]
            
            self.map_canvas.create_polygon(points, fill=p_color, outline="white", width=1)
            # 显示名字缩写
            self.map_canvas.create_text(px, py - p_size - 8, text=name[:3], fill="#34495E", font=("Arial", 7, "bold"))

        # 获胜文字
        if self.winner:
             self.map_canvas.create_text(w//2, h//2, text=f"WINNER:\n{self.winner}", fill="#E74C3C", font=("Helvetica", 36, "bold"), justify="center")

    def wrap_text_smart(self, text):
        """轮盘内的智能换行"""
        words = text.split()
        lines = []
        current_line = []
        current_len = 0
        current_limit = 16
        for word in words:
            current_line.append(word)
            current_len += len(word) + 1
            if current_len >= current_limit:
                lines.append(" ".join(current_line))
                current_line = []
                current_len = 0
                current_limit = 14
        if current_line:
            lines.append(" ".join(current_line))
        return "\n".join(lines)
    
    def wrap_text_rect(self, text, width_chars=55):
        """矩形区域标准换行"""
        paragraphs = text.split('\n')
        final_lines = []
        for p in paragraphs:
            if not p.strip():
                final_lines.append("")
                continue
            wrapped = textwrap.wrap(p, width=width_chars)
            final_lines.extend(wrapped)
        return "\n".join(final_lines)

    def draw_wheel(self):
        """绘制轮盘"""
        if self.phase >= 4:
            self.draw_qa_screen()
            return

        self.canvas.delete("all")
        
        num_items = len(self.current_items)
        if num_items == 0: return

        arc_angle = 360 / num_items
        
        # 阴影
        self.canvas.create_oval(
            CENTER_X - WHEEL_RADIUS - 5, CENTER_Y - WHEEL_RADIUS - 5,
            CENTER_X + WHEEL_RADIUS + 5, CENTER_Y + WHEEL_RADIUS + 5,
            fill="#DDDDDD", outline=""
        )

        # 扇形
        for i in range(num_items):
            start_angle = self.angle + (i * arc_angle)
            
            raw_item = self.current_items[i]
            if isinstance(raw_item, dict):
                item_text = raw_item['q']
            else:
                item_text = raw_item
            
            # === 闪烁逻辑 ===
            color = self.flash_map.get(i, COLORS[i % len(COLORS)])
            
            self.canvas.create_arc(
                CENTER_X - WHEEL_RADIUS, CENTER_Y - WHEEL_RADIUS,
                CENTER_X + WHEEL_RADIUS, CENTER_Y + WHEEL_RADIUS,
                start=start_angle, extent=arc_angle, fill=color, outline="white", width=2
            )

            mid_angle_rad = math.radians(start_angle + arc_angle / 2)
            text_radius = WHEEL_RADIUS * 0.63
            tx = CENTER_X + text_radius * math.cos(mid_angle_rad)
            ty = CENTER_Y - text_radius * math.sin(mid_angle_rad)

            display_text = self.wrap_text_smart(item_text)

            self.canvas.create_text(tx+1, ty+1, text=display_text, font=WHEEL_TEXT_FONT, fill="#333333", justify="center")
            self.canvas.create_text(tx, ty, text=display_text, font=WHEEL_TEXT_FONT, fill="black", justify="center")

        # 指针
        self.canvas.create_polygon(
            CENTER_X + WHEEL_RADIUS + 15, CENTER_Y, 
            CENTER_X + WHEEL_RADIUS + 15 + 40, CENTER_Y - 15, 
            CENTER_X + WHEEL_RADIUS + 15 + 40, CENTER_Y + 15, 
            fill="#FF4444", outline="#8B0000", width=2
        )
        
        # 中心
        self.canvas.create_oval(CENTER_X-25, CENTER_Y-25, CENTER_X+25, CENTER_Y+25, fill="white", outline="#CCCCCC", width=2)

    def draw_qa_screen(self):
        """绘制 Phase 4 (问题+输入) 和 Phase 5 (答案+AI反馈) 的问答界面"""
        self.canvas.delete("all")
        
        if not self.selected_question_data:
            return

        question_text = self.selected_question_data['q']
        
        # 共同元素：大问题显示
        display_q = self.wrap_text_rect(question_text, width_chars=50)
        
        # Phase 4: 显示问题 + 输入框
        if self.phase == 4:
            # 问题文本 (显示在上方)
            self.canvas.create_text(
                CENTER_X, 100, 
                text=display_q, 
                font=QUESTION_BIG_FONT, 
                fill="#333333", 
                justify="center",
                width=WINDOW_WIDTH - 400
            )

            # 提示文本
            self.canvas.create_text(CENTER_X, 250, text="Enter Name:", font=("Helvetica", 12, "bold"), fill="#666")
            self.canvas.create_text(CENTER_X, 330, text="Your Answer:", font=("Helvetica", 12, "bold"), fill="#666")

            if not self.name_entry:
                self.name_entry = tk.Entry(self.canvas, font=("Helvetica", 14), justify="center", width=20)
                self.input_window_name = self.canvas.create_window(CENTER_X, 280, window=self.name_entry)

                self.answer_text = tk.Text(self.canvas, font=("Helvetica", 14), width=40, height=5)
                self.input_window_answer = self.canvas.create_window(CENTER_X, 400, window=self.answer_text)
                
                self.name_entry.focus_set()

        # Phase 5: 显示标准答案 + AI 反馈
        elif self.phase == 5:
            if self.name_entry:
                self.name_entry.destroy()
                self.answer_text.destroy()
                self.name_entry = None
                self.answer_text = None

            self.canvas.create_text(
                CENTER_X, 60, 
                text=f"Q: {question_text}", 
                font=QUESTION_SMALL_FONT, 
                fill="#666666", 
                justify="center",
                width=WINDOW_WIDTH - 400
            )
            self.canvas.create_line(100, 100, WINDOW_WIDTH-400, 100, fill="#DDDDDD", width=2)
            
            y_cursor = 140
            
            if hasattr(self, 'ai_result_text'):
                self.canvas.create_text(CENTER_X, y_cursor, text="--- AI Feedback ---", font=("Helvetica", 12, "bold"), fill="#FF9F1C")
                y_cursor += 30
                display_ai = self.wrap_text_rect(self.ai_result_text, width_chars=60)
                self.canvas.create_text(
                    CENTER_X, y_cursor, 
                    text=display_ai, 
                    font=AI_FEEDBACK_FONT, 
                    fill="#1A535C", 
                    justify="center",
                    anchor="n",
                    width=WINDOW_WIDTH - 450
                )
                lines = display_ai.count('\n') + 1
                y_cursor += lines * 25 + 40

            self.canvas.create_text(CENTER_X, y_cursor, text="--- Standard Answer ---", font=("Helvetica", 12, "bold"), fill="#28a745")
            y_cursor += 30
            answer_text = self.selected_question_data['a']
            display_a = self.wrap_text_rect(answer_text, width_chars=60)
            self.canvas.create_text(
                CENTER_X, y_cursor, 
                text=display_a, 
                font=ANSWER_FONT, 
                fill="#333333", 
                justify="center",
                anchor="n",
                width=WINDOW_WIDTH - 450
            )

    def start_spin(self):
        # 如果在 Phase 4 (答题阶段)，按钮功能是 "CHECK ANSWER"
        if self.phase == 4:
            self.check_answer_with_ai()
            return

        if self.is_spinning:
            return

        if self.phase == 0:
            self.phase = 1
            # === 修改处：使用 uniform 生成浮点数，增加随机性 ===
            self.velocity = random.uniform(30.0, 55.0) 
            # === 修改处：每次旋转给一个微小的随机摩擦力，防止路径固定 ===
            self.friction = random.uniform(0.85, 0.983)
            
            self.spin_btn.config(state=tk.DISABLED, bg="#9E9E9E")
            self.is_spinning = True
            self.animate()
            
        elif self.phase == 2:
            self.phase = 3
            # === 修改处：同上，第二轮也增加随机性 ===
            self.velocity = random.uniform(35.0, 60.0)
            self.friction = random.uniform(0.978, 0.983)
            
            self.spin_btn.config(state=tk.DISABLED, bg="#9E9E9E")
            self.is_spinning = True
            self.animate()

    def check_answer_with_ai(self):
        """调用 AI 进行评分"""
        user_name = self.name_entry.get().strip()
        user_answer = self.answer_text.get("1.0", tk.END).strip()

        if not user_name:
            self.info_label.config(text="Please enter your name!", fg="red")
            return
        if not user_answer:
            self.info_label.config(text="Please enter an answer!", fg="red")
            return

        if not self._ensure_api_key():
            return

        # 禁用按钮，显示 Loading
        self.spin_btn.config(text="AI EVALUATING...", state=tk.DISABLED, bg="#9E9E9E")
        self.info_label.config(text="AI is grading your answer...", fg="#1A535C")

        # 开启线程调用 API
        threading.Thread(target=self.run_ai_thread, args=(user_name, user_answer)).start()

    def run_ai_thread(self, user_name, user_answer):
        """后台线程运行 AI 请求"""
        question = self.selected_question_data['q']
        standard_answer = self.selected_question_data['a']

        prompt = f"""
        You are an encouraging and supportive teacher. be objective and fair, do not strict on the format. If the standard answer is personal answer, you should give a objective score based on the student answer.
        Question: {question}
        Standard Answer: {standard_answer}
        Student Answer: {user_answer}

        Task:
        1. Rate the student answer from 0 to 10.
        2. Provide a very short feedback (max 2 sentences).
        
        Output format strictly as JSON:
        {{
            "score": <number>,
            "feedback": "<text>"
        }}
        """

        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": YOUR_SITE_URL, 
                    "X-Title": YOUR_APP_NAME,
                },
                data=json.dumps({
                    "model": "openai/gpt-oss-20b:free", # 使用免费模型
                    "messages": [{"role": "user", "content": prompt}]
                }),
                timeout=20 # 设置超时
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # 尝试解析 JSON
                try:
                    # 有时候模型可能不只输出 JSON，尝试提取 JSON 部分
                    json_match = re.search(r"\{.*\}", content, re.DOTALL)
                    if json_match:
                        data = json.loads(json_match.group(0))
                        score = int(data.get("score", 0))
                        feedback = data.get("feedback", "No feedback.")
                    else:
                        score = 5
                        feedback = content
                except:
                    score = 5
                    feedback = content

                # 回到主线程更新 UI
                self.root.after(0, lambda: self.finish_ai_check(user_name, score, feedback))
            else:
                self.root.after(0, lambda: self.finish_ai_check(user_name, 0, f"Error: {response.status_code}"))

        except Exception as e:
            self.root.after(0, lambda: self.finish_ai_check(user_name, 0, "AI Connection Failed."))

    def finish_ai_check(self, user_name, score, feedback):
        """AI 完成后更新状态"""
        # 累加分数
        current_score = self.scores.get(user_name, 0)
        
        # 基础总分
        new_total_score = current_score + score
        
        special_msg = ""
        
        # 检查是否踩到特殊格子
        # 循环检查，防止连续跳跃（虽然这里只做一次检查，避免死循环）
        if new_total_score in SPECIAL_TILES:
            effect = SPECIAL_TILES[new_total_score]
            steps = random.randint(1, 5) # 随机1-5步
            
            if effect == 'forward':
                new_total_score += steps
                special_msg = f"\n🚀 LUCKY! Forward {steps} steps!"
            elif effect == 'backward':
                new_total_score -= steps
                special_msg = f"\n⚠️ OOPS! Backward {steps} steps!"
            
            # 确保不小于0
            new_total_score = max(0, new_total_score)
            
        self.scores[user_name] = new_total_score
        
        # 检查是否获胜
        if new_total_score >= WINNING_SCORE and not self.winner:
            self.winner = user_name
        
        # 刷新排行榜和地图
        self.update_leaderboard()

        # 准备 Phase 5 显示文本
        self.ai_result_text = f"Score: {score}/10\nFeedback: {feedback}{special_msg}"
        
        # 切换到 Phase 5
        self.phase = 5
        self.info_label.config(text=f"Grading Complete! {user_name} got {score} points.", fg="#28a745")
        self.spin_btn.config(text="DONE (RESET)", state=tk.DISABLED, bg="#9E9E9E")
        
        self.draw_wheel() # 重绘界面显示结果

    def animate(self):
        if self.is_spinning:
            self.angle += self.velocity
            self.angle %= 360
            self.velocity *= self.friction
            self.draw_wheel()
            
            if self.velocity < 0.15:
                self.velocity = 0
                self.is_spinning = False
                self.handle_stop()
            else:
                self.root.after(20, self.animate)

    def handle_stop(self):
        num_items = len(self.current_items)
        arc_angle = 360 / num_items
        effective_angle = self.angle % 360
        relative_pointer = (360 - effective_angle) % 360
        winner_index = int(relative_pointer // arc_angle)
        winner_data = self.current_items[winner_index]

        if self.phase == 1:
            self.start_flash_sequence(winner_index, lambda: self.update_group_ui(winner_data))
        elif self.phase == 3:
            self.start_flash_sequence(winner_index, lambda: self.show_selected_question(winner_data))

    def start_flash_sequence(self, winner_index, callback):
        self.flash_index = winner_index
        self.flash_callback = callback
        self.flash_count = 0
        self.flash_toggle()

    def flash_toggle(self):
        if self.flash_count >= 6:
            self.flash_map = {} 
            self.draw_wheel()
            if self.flash_callback:
                self.flash_callback()
            return
        
        if self.flash_count % 2 == 0:
            self.flash_map = {self.flash_index: "#FFFFFF"} 
        else:
            self.flash_map = {} 
            
        self.draw_wheel()
        self.flash_count += 1
        self.root.after(250, self.flash_toggle)

    def show_selected_question(self, winner_data):
        self.selected_question_data = winner_data 
        self.phase = 4
        self.info_label.config(text="Enter your answer below!", fg="#FF6B6B")
        # 按钮变为检查答案
        self.spin_btn.config(text="CHECK ANSWER", state=tk.NORMAL, bg="#FF9F1C")
        self.draw_wheel()

    def update_group_ui(self, group_name):
        self.selected_group = group_name
        self.phase = 2
        self.info_label.config(text=f"Selected Group: {self.selected_group}", fg="#1A535C")
        self.spin_btn.config(text="SPIN FOR QUESTION", state=tk.NORMAL, bg="#28a745")
        
        questions = GAME_DATA.get(group_name, [])
        self.current_items = questions
        self.angle = 0
        self.draw_wheel()

    def reset_game(self):
        self.phase = 0
        self.selected_group = None
        self.selected_question_data = None
        self.current_items = list(GAME_DATA.keys())
        self.angle = 0
        self.velocity = 0
        self.is_spinning = False
        self.flash_map = {}
        
        # 清除 Phase 4 的输入框（如果存在）
        if self.name_entry:
            self.name_entry.destroy()
            self.answer_text.destroy()
            self.name_entry = None
            self.answer_text = None
        
        self.info_label.config(text="Ready? Click SPIN to select a Group!", fg="#333333", font=LABEL_FONT)
        self.spin_btn.config(text="SPIN WHEEL", state=tk.NORMAL, bg="#28a745")
        self.draw_wheel()

if __name__ == "__main__":
    root = tk.Tk()
    app = SpinWheelApp(root)
    root.mainloop()
    print("Game closed") # test