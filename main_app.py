import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
from datetime import datetime, date, timedelta
from enhanced_app_logic import EnhancedAppLogic
from utils import resource_path, ensure_persistent_db
import calendar
from ui_components import UIComponents
db_path = ensure_persistent_db("study_tracker.db")
class StudyTrackerApp:
    def __init__(self):
        self.app_logic = EnhancedAppLogic()
        self.root = tk.Tk()
        self.root.title("Study Progress Tracker")
        self.root.geometry("900x700")
        
        self.colors = {
            'bg_primary': '#f7f6f5',
            'bg_secondary': '#ffffff',
            'bg_dark': '#2c2c2c',
            'accent_orange': '#e95420',
            'accent_light_orange': '#f99157',
            'accent_purple': '#762572',
            'text_dark': '#2c2c2c',
            'text_light': '#ffffff',
            'border': '#d9d9d9',
            'success': '#38b44a',
            'warning': '#efb73e',
            'error': '#df382c',
            'info': '#19b6ee'
        }
        
        self.root.configure(bg=self.colors['bg_primary'])
        self.style = ttk.Style()
        
        available_themes = self.style.theme_names()
        if 'radiance' in available_themes:
            self.style.theme_use('radiance')
        elif 'clam' in available_themes:
            self.style.theme_use('clam')
        else:
            self.style.theme_use('default')
        
        self.configure_ubuntu_styles()
        self.current_frame = None
        self.show_login_screen()
    
    def configure_ubuntu_styles(self):
        """Configure Ubuntu Radiance theme styles"""
        self.style.configure('Ubuntu.Treeview',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_dark'],
                           fieldbackground=self.colors['bg_secondary'],
                           bordercolor=self.colors['border'])
        
        self.style.configure('Ubuntu.Treeview.Heading',
                           background=self.colors['bg_primary'],
                           foreground=self.colors['text_dark'],
                           relief='flat',
                           borderwidth=1)
        
        self.style.configure('Ubuntu.Horizontal.TProgressbar',
                           background=self.colors['accent_orange'],
                           troughcolor=self.colors['bg_primary'])
    
    def clear_frame(self):
        """Clear current frame"""
        if self.current_frame:
            self.current_frame.destroy()
    
    def show_login_screen(self):
        """Display login/register screen"""
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.current_frame.pack(fill='both', expand=True)
        
        title_label = tk.Label(
            self.current_frame, 
            text="Study Progress Tracker", 
            font=('Ubuntu', 24, 'bold'),
            bg=self.colors['bg_primary'],
            fg=self.colors['accent_purple']
        )
        title_label.pack(pady=40)
        
        login_frame = tk.LabelFrame(
            self.current_frame, 
            text="Sign In", 
            font=('Ubuntu', 12, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_purple'],
            relief='solid',
            bd=1
        )
        login_frame.pack(pady=20, padx=60, fill='x', ipady=10)
        
        tk.Label(login_frame, text="Username:", 
                font=('Ubuntu', 10), bg=self.colors['bg_secondary'], 
                fg=self.colors['text_dark']).grid(row=0, column=0, sticky='w', padx=15, pady=8)
        self.login_username = tk.Entry(login_frame, width=35, font=('Ubuntu', 10),
                                     relief='solid', bd=1, bg=self.colors['bg_primary'])
        self.login_username.grid(row=0, column=1, padx=15, pady=8)
        
        tk.Label(login_frame, text="Password:", 
                font=('Ubuntu', 10), bg=self.colors['bg_secondary'], 
                fg=self.colors['text_dark']).grid(row=1, column=0, sticky='w', padx=15, pady=8)
        self.login_password = tk.Entry(login_frame, width=35, show='*', font=('Ubuntu', 10),
                                     relief='solid', bd=1, bg=self.colors['bg_primary'])
        self.login_password.grid(row=1, column=1, padx=15, pady=8)
        
        login_btn = UIComponents.create_button(
            login_frame, 
            "Sign In", 
            self.handle_login,
            self.colors['accent_orange']
        )
        login_btn.grid(row=2, column=1, pady=15, sticky='e')
        
        register_frame = tk.LabelFrame(
            self.current_frame, 
            text="Create Account", 
            font=('Ubuntu', 12, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_purple'],
            relief='solid',
            bd=1
        )
        register_frame.pack(pady=20, padx=60, fill='x', ipady=10)
        
        tk.Label(register_frame, text="Username:", 
                font=('Ubuntu', 10), bg=self.colors['bg_secondary'], 
                fg=self.colors['text_dark']).grid(row=0, column=0, sticky='w', padx=15, pady=5)
        self.register_username = tk.Entry(register_frame, width=35, font=('Ubuntu', 10),
                                        relief='solid', bd=1, bg=self.colors['bg_primary'])
        self.register_username.grid(row=0, column=1, padx=15, pady=5)
        
        tk.Label(register_frame, text="Password:", 
                font=('Ubuntu', 10), bg=self.colors['bg_secondary'], 
                fg=self.colors['text_dark']).grid(row=1, column=0, sticky='w', padx=15, pady=5)
        self.register_password = tk.Entry(register_frame, width=35, show='*', font=('Ubuntu', 10),
                                        relief='solid', bd=1, bg=self.colors['bg_primary'])
        self.register_password.grid(row=1, column=1, padx=15, pady=5)
        
        tk.Label(register_frame, text="Email:", 
                font=('Ubuntu', 10), bg=self.colors['bg_secondary'], 
                fg=self.colors['text_dark']).grid(row=2, column=0, sticky='w', padx=15, pady=5)
        self.register_email = tk.Entry(register_frame, width=35, font=('Ubuntu', 10),
                                     relief='solid', bd=1, bg=self.colors['bg_primary'])
        self.register_email.grid(row=2, column=1, padx=15, pady=5)
        
        register_btn = UIComponents.create_button(
            register_frame, 
            "Create Account", 
            self.handle_register,
            self.colors['info']
        )
        register_btn.grid(row=3, column=1, pady=15, sticky='e')
    
    def handle_login(self):
        """Handle login button click"""
        username = self.login_username.get()
        password = self.login_password.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        success, message = self.app_logic.login_user(username, password)
        
        if success:
            self.show_dashboard()
        else:
            messagebox.showerror("Error", message)
    
    def handle_register(self):
        """Handle register button click"""
        username = self.register_username.get()
        password = self.register_password.get()
        email = self.register_email.get()
        
        if not username or not password or not email:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        success, message = self.app_logic.register_user(username, password, email)
        
        if success:
            messagebox.showinfo("Success", message)
            self.register_username.delete(0, 'end')
            self.register_password.delete(0, 'end')
            self.register_email.delete(0, 'end')
        else:
            messagebox.showerror("Error", message)
    
    def show_dashboard(self):
        """Display main dashboard with all features"""
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.current_frame.pack(fill='both', expand=True)
        
        header_frame = tk.Frame(self.current_frame, bg=self.colors['accent_orange'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        current_user = self.app_logic.get_current_user()
        welcome_label = tk.Label(
            header_frame,
            text=f"Welcome back, {current_user['username']}!",
            font=('Ubuntu', 18, 'bold'),
            bg=self.colors['accent_orange'],
            fg=self.colors['text_light']
        )
        welcome_label.pack(side='left', padx=30, pady=25)
        
        logout_btn = UIComponents.create_button(
            header_frame,
            "Sign Out",
            self.handle_logout,
            self.colors['error']
        )
        logout_btn.pack(side='right', padx=30, pady=25)
        
        progress_frame = tk.LabelFrame(
            self.current_frame, 
            text="Learning Progress Overview", 
            font=('Ubuntu', 14, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_purple'],
            relief='solid',
            bd=1
        )
        progress_frame.pack(fill='x', padx=30, pady=20)
        
        total_progress = self.app_logic.calculate_total_progress()
        streak = self.app_logic.get_current_streak()
        
        stats_top = tk.Frame(progress_frame, bg=self.colors['bg_secondary'])
        stats_top.pack(pady=15)
        
        progress_label = tk.Label(
            stats_top,
            text=f"Overall Progress: {total_progress:.1f}%",
            font=('Ubuntu', 14, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_dark']
        )
        progress_label.pack(side='left', padx=20)
        
        streak_label = tk.Label(
            stats_top,
            text=f"🔥 {streak} Day Streak",
            font=('Ubuntu', 14, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['error']
        )
        streak_label.pack(side='left', padx=20)
        
        progress_bar = ttk.Progressbar(
            progress_frame, 
            length=500, 
            mode='determinate',
            style='Ubuntu.Horizontal.TProgressbar'
        )
        progress_bar.pack(pady=(0, 15))
        progress_bar['value'] = total_progress
        
        stats_frame = tk.Frame(progress_frame, bg=self.colors['bg_secondary'])
        stats_frame.pack(pady=(0, 15))
        
        topics = self.app_logic.get_user_subtopics()
        goals = self.app_logic.get_user_goals()
        notes = self.app_logic.get_user_notes()
        exams = self.app_logic.get_exam_history()
        tasks = self.app_logic.get_tasks(include_completed=False)
        completed_goals = [g for g in goals if g['is_completed']]
        
        stats = [
            (len(topics), "Topics"),
            (len(exams), "Exams Taken"),
            (len(tasks), "Pending Tasks"),
            (len(completed_goals), f"Goals Done")
        ]
        
        for i, (value, label) in enumerate(stats):
            stat_frame = tk.Frame(stats_frame, bg=self.colors['bg_primary'], relief='solid', bd=1)
            stat_frame.pack(side='left', padx=10, pady=5, fill='both', expand=True)
            
            tk.Label(
                stat_frame,
                text=str(value),
                font=('Ubuntu', 20, 'bold'),
                bg=self.colors['bg_primary'],
                fg=self.colors['accent_orange']
            ).pack(pady=(10, 0))
            
            tk.Label(
                stat_frame,
                text=label,
                font=('Ubuntu', 10),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_dark']
            ).pack(pady=(0, 10))
        
        nav_frame = tk.Frame(self.current_frame, bg=self.colors['bg_primary'])
        nav_frame.pack(fill='x', padx=30, pady=20)
        
        nav_title = tk.Label(
            nav_frame,
            text="Quick Actions",
            font=('Ubuntu', 16, 'bold'),
            bg=self.colors['bg_primary'],
            fg=self.colors['accent_purple']
        )
        nav_title.pack(pady=(0, 15))
        
        buttons_frame = tk.Frame(nav_frame, bg=self.colors['bg_primary'])
        buttons_frame.pack()
        
        buttons = [
            ("📚 Topics", self.show_topics, self.colors['info']),
            ("🎯 Goals", self.show_goals, self.colors['success']),
            ("📝 Notes", self.show_notes, self.colors['warning']),
            ("🎓 Exams", self.show_exams, self.colors['accent_orange']),
            ("✅ Tasks", self.show_tasks, self.colors['success']),
            ("💻 Code IDE", self.show_code_ide, self.colors['bg_dark']),
            ("⌨️ Coding Practice", self.show_coding_practice, self.colors['info']),
            ("🔥 Streak", self.show_streak_view, self.colors['error'])
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = UIComponents.create_button(
                buttons_frame,
                text,
                command,
                color
            )
            btn.config(width=15, height=2)
            btn.grid(row=i//4, column=i%4, padx=8, pady=8)
    
    # ========== TOPICS MANAGEMENT ==========
    
    def show_topics(self):
        """Display topics management screen"""
        self.clear_frame()

        self.current_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.current_frame.pack(fill='both', expand=True)

        header = tk.Label(
            self.current_frame,
            text="📚 Topic Management",
            font=('Ubuntu', 20, 'bold'),
            bg=self.colors['bg_primary'],
            fg=self.colors['accent_purple']
        )
        header.pack(pady=25)

        add_frame = tk.LabelFrame(
            self.current_frame,
            text="Add New Topic",
            font=('Ubuntu', 12, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_purple'],
            relief='solid',
            bd=1
        )
        add_frame.pack(fill='x', padx=30, pady=15)

        form_frame = tk.Frame(add_frame, bg=self.colors['bg_secondary'])
        form_frame.pack(padx=20, pady=15)

        tk.Label(form_frame, text="Topic Name:", 
                font=('Ubuntu', 11), bg=self.colors['bg_secondary'], 
                fg=self.colors['text_dark']).grid(row=0, column=0, sticky='w', padx=10, pady=8)
        self.topic_name_entry = tk.Entry(form_frame, width=35, font=('Ubuntu', 10),
                                       relief='solid', bd=1, bg=self.colors['bg_primary'])
        self.topic_name_entry.grid(row=0, column=1, padx=10, pady=8)

        tk.Label(form_frame, text="Subject:", 
                font=('Ubuntu', 11), bg=self.colors['bg_secondary'], 
                fg=self.colors['text_dark']).grid(row=1, column=0, sticky='w', padx=10, pady=8)
        self.subject_entry = tk.Entry(form_frame, width=35, font=('Ubuntu', 10),
                                    relief='solid', bd=1, bg=self.colors['bg_primary'])
        self.subject_entry.grid(row=1, column=1, padx=10, pady=8)

        add_btn = UIComponents.create_button(
            form_frame,
            "Add Topic",
            self.handle_add_topic,
            self.colors['success']
        )
        add_btn.grid(row=2, column=1, pady=15, sticky='e')

        list_frame = tk.LabelFrame(
            self.current_frame,
            text="Your Topics",
            font=('Ubuntu', 12, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_purple'],
            relief='solid',
            bd=1
        )
        list_frame.pack(fill='both', expand=True, padx=30, pady=15)

        tree_frame = tk.Frame(list_frame, bg=self.colors['bg_secondary'])
        tree_frame.pack(fill='both', expand=True, padx=15, pady=15)

        columns = ('Subject', 'Topic', 'Progress')
        self.topics_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            height=12,
            style='Ubuntu.Treeview'
        )

        for col in columns:
            self.topics_tree.heading(col, text=col)
            if col == 'Progress':
                self.topics_tree.column(col, width=100, anchor='center')
            else:
                self.topics_tree.column(col, width=200)

        scrollbar = ttk.Scrollbar(
            tree_frame,
            orient='vertical',
            command=self.topics_tree.yview
        )
        self.topics_tree.configure(yscrollcommand=scrollbar.set)

        self.topics_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        btn_frame = tk.Frame(list_frame, bg=self.colors['bg_secondary'])
        btn_frame.pack(fill='x', padx=15, pady=(0, 15))

        update_progress_btn = UIComponents.create_button(
            btn_frame,
            "Update Progress",
            self.handle_update_progress,
            self.colors['warning']
        )
        update_progress_btn.pack(side='right', padx=5)

        back_btn = UIComponents.create_button(
            self.current_frame,
            "← Back to Dashboard",
            self.show_dashboard,
            self.colors['bg_dark']
        )
        back_btn.pack(pady=20)

        self.refresh_topics_list()

    def refresh_topics_list(self):
        """Refresh the topics list"""
        for item in self.topics_tree.get_children():
            self.topics_tree.delete(item)
        
        topics = self.app_logic.get_user_subtopics()
        for topic in topics:
            tag_id = str(topic['topic_id'])
            self.topics_tree.insert('', 'end', values=(
                topic.get('subject'),
                topic.get('topic_name'),
                f"{topic.get('progress', 0)}%"
            ), tags=(tag_id,))

    def handle_add_topic(self):
        """Handle add topic button click"""
        topic_name = self.topic_name_entry.get()
        subject = self.subject_entry.get()

        success, message = self.app_logic.add_subtopic(topic_name, subject)

        if success:
            messagebox.showinfo("Success", message)
            self.topic_name_entry.delete(0, 'end')
            self.subject_entry.delete(0, 'end')
            self.refresh_topics_list()
        else:
            messagebox.showerror("Error", message)

    def handle_update_progress(self):
        """Handle update progress button click"""
        selection = self.topics_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a topic to update")
            return
        
        item = self.topics_tree.item(selection[0])
        raw_tag = item['tags'][0]
        try:
            topic_id = int(raw_tag)
        except Exception:
            messagebox.showerror("Error", "Invalid topic id")
            return

        topic_name = item['values'][1]
        
        new_progress = simpledialog.askinteger(
            "Update Progress",
            f"Enter new progress for '{topic_name}' (0-100):",
            minvalue=0,
            maxvalue=100
        )
        
        if new_progress is not None:
            success, message = self.app_logic.update_topic_progress(topic_id, new_progress)
            
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_topics_list()
            else:
                messagebox.showerror("Error", message)
    
    # ========== GOALS MANAGEMENT ==========
    
    def show_goals(self):
        """Display goals management screen"""
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.current_frame.pack(fill='both', expand=True)
        
        header = tk.Label(
            self.current_frame,
            text="🎯 Goal Management",
            font=('Ubuntu', 18, 'bold'),
            bg=self.colors['bg_primary'],
            fg=self.colors['accent_purple']
        )
        header.pack(pady=20)
        
        add_frame = tk.LabelFrame(self.current_frame, text="Add New Goal", 
                                bg=self.colors['bg_secondary'], fg=self.colors['accent_purple'])
        add_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(add_frame, text="Goal Text:", bg=self.colors['bg_secondary'], 
                fg=self.colors['text_dark']).grid(row=0, column=0, padx=10, pady=5)
        self.goal_text_entry = tk.Entry(add_frame, width=50)
        self.goal_text_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(add_frame, text="Topic (optional):", bg=self.colors['bg_secondary'],
                fg=self.colors['text_dark']).grid(row=1, column=0, padx=10, pady=5)
        topics = self.app_logic.get_user_subtopics()
        topic_options = ["(General)"] + [f"{t['topic_name']} ({t['subject']})" for t in topics]
        self.goal_topic_var = tk.StringVar(value=topic_options[0])
        ttk.Combobox(add_frame, textvariable=self.goal_topic_var, values=topic_options, width=40, state='readonly').grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(add_frame, text="Target Date (YYYY-MM-DD):", bg=self.colors['bg_secondary'],
                fg=self.colors['text_dark']).grid(row=2, column=0, padx=10, pady=5)
        self.target_date_entry = tk.Entry(add_frame, width=30)
        self.target_date_entry.grid(row=2, column=1, padx=10, pady=5)
        
        add_goal_btn = UIComponents.create_button(
            add_frame,
            "Add Goal",
            self.handle_add_goal,
            self.colors['success']
        )
        add_goal_btn.grid(row=3, column=1, pady=10, sticky='e')
        
        list_frame = tk.LabelFrame(self.current_frame, text="Your Goals", 
                                 bg=self.colors['bg_secondary'], fg=self.colors['accent_purple'])
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('Goal', 'Topic', 'Target Date', 'Status')
        self.goals_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.goals_tree.heading(col, text=col)
            if col == 'Goal':
                self.goals_tree.column(col, width=300)
            else:
                self.goals_tree.column(col, width=120)
        
        goals_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.goals_tree.yview)
        self.goals_tree.configure(yscrollcommand=goals_scrollbar.set)
        
        self.goals_tree.pack(side='left', fill='both', expand=True)
        goals_scrollbar.pack(side='right', fill='y')
        
        toggle_goal_btn = UIComponents.create_button(
            list_frame,
            "Toggle Goal Status",
            self.handle_toggle_goal,
            self.colors['warning']
        )
        toggle_goal_btn.pack(pady=10)
        
        back_btn = UIComponents.create_button(
            self.current_frame,
            "← Back to Dashboard",
            self.show_dashboard,
            self.colors['bg_dark']
        )
        back_btn.pack(pady=20)
        
        self.refresh_goals_list()

    def refresh_goals_list(self):
        """Refresh the goals list"""
        for item in self.goals_tree.get_children():
            self.goals_tree.delete(item)
        
        goals = self.app_logic.get_user_goals()
        for goal in goals:
            status = "✓ Completed" if goal.get('is_completed') else "○ Pending"
            tag_id = str(goal['goal_id'])
            self.goals_tree.insert('', 'end', values=(
                goal.get('goal_text'),
                goal.get('topic_name'),
                goal.get('target_date') or 'Not set',
                status
            ), tags=(tag_id,))

    def handle_add_goal(self):
        """Handle add goal button click"""
        goal_text = self.goal_text_entry.get().strip()
        target_date = self.target_date_entry.get().strip() or None

        topic_sel = self.goal_topic_var.get()
        topic_id = None
        if topic_sel and topic_sel != "(General)":
            topics = self.app_logic.get_user_subtopics()
            for t in topics:
                label = f"{t['topic_name']} ({t['subject']})"
                if label == topic_sel:
                    topic_id = int(t['topic_id'])
                    break

        success, message = self.app_logic.add_goal(goal_text, topic_id=topic_id, target_date=target_date)

        if success:
            messagebox.showinfo("Success", message)
            self.goal_text_entry.delete(0, 'end')
            self.target_date_entry.delete(0, 'end')
            self.refresh_goals_list()
        else:
            messagebox.showerror("Error", message)

    def handle_toggle_goal(self):
        """Handle toggle goal button click"""
        selection = self.goals_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a goal to toggle")
            return
        
        item = self.goals_tree.item(selection[0])
        raw_tag = item['tags'][0]
        try:
            goal_id = int(raw_tag)
        except Exception:
            messagebox.showerror("Error", "Invalid goal id")
            return
        
        success, message = self.app_logic.toggle_goal(goal_id)
        
        if success:
            messagebox.showinfo("Success", message)
            self.refresh_goals_list()
        else:
            messagebox.showerror("Error", message)
    
    # ========== NOTES MANAGEMENT ==========
    
    def show_notes(self):
        """Display notes management screen"""
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.current_frame.pack(fill='both', expand=True)
        
        header = tk.Label(
            self.current_frame,
            text="📝 Notes Management",
            font=('Ubuntu', 18, 'bold'),
            bg=self.colors['bg_primary'],
            fg=self.colors['accent_purple']
        )
        header.pack(pady=20)
        
        add_frame = tk.LabelFrame(self.current_frame, text="Add New Note", 
                                bg=self.colors['bg_secondary'], fg=self.colors['accent_purple'])
        add_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(add_frame, text="Topic (optional):", bg=self.colors['bg_secondary'],
                fg=self.colors['text_dark']).pack(anchor='w', padx=10)
        topics = self.app_logic.get_user_subtopics()
        note_topic_options = ["(General)"] + [f"{t['topic_name']} ({t['subject']})" for t in topics]
        self.note_topic_var = tk.StringVar(value=note_topic_options[0])
        ttk.Combobox(add_frame, textvariable=self.note_topic_var, values=note_topic_options, width=40, state='readonly').pack(anchor='w', padx=10, pady=5)

        tk.Label(add_frame, text="Note Text:", bg=self.colors['bg_secondary'],
                fg=self.colors['text_dark']).pack(anchor='w', padx=10)
        self.note_text = tk.Text(add_frame, width=70, height=4)
        self.note_text.pack(padx=10, pady=5)
        
        add_note_btn = UIComponents.create_button(
            add_frame,
            "Add Note",
            self.handle_add_note,
            self.colors['success']
        )
        add_note_btn.pack(pady=10)
        
        list_frame = tk.LabelFrame(self.current_frame, text="Your Notes", 
                                 bg=self.colors['bg_secondary'], fg=self.colors['accent_purple'])
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('Date', 'Topic', 'Note')
        self.notes_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=8)
        
        self.notes_tree.heading('Date', text='Date')
        self.notes_tree.heading('Topic', text='Topic')
        self.notes_tree.heading('Note', text='Note')
        
        self.notes_tree.column('Date', width=150)
        self.notes_tree.column('Topic', width=120)
        self.notes_tree.column('Note', width=400)
        
        notes_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.notes_tree.yview)
        self.notes_tree.configure(yscrollcommand=notes_scrollbar.set)
        
        self.notes_tree.pack(side='left', fill='both', expand=True)
        notes_scrollbar.pack(side='right', fill='y')
        
        delete_note_btn = UIComponents.create_button(
            list_frame,
            "Delete Selected Note",
            self.handle_delete_note,
            self.colors['error']
        )
        delete_note_btn.pack(pady=10)
        
        back_btn = UIComponents.create_button(
            self.current_frame,
            "← Back to Dashboard",
            self.show_dashboard,
            self.colors['bg_dark']
        )
        back_btn.pack(pady=20)
        
        self.refresh_notes_list()

    def refresh_notes_list(self):
        """Refresh the notes list"""
        for item in self.notes_tree.get_children():
            self.notes_tree.delete(item)
        
        notes = self.app_logic.get_user_notes()
        for note in notes:
            try:
                date_obj = datetime.strptime(note.get('created_at', ''), '%Y-%m-%d %H:%M:%S')
                formatted_date = date_obj.strftime('%Y-%m-%d %H:%M')
            except Exception:
                formatted_date = note.get('created_at', '')
            
            tag_id = str(note['note_id'])
            note_preview = (note.get('note_text') or '')[:100]
            if len(note.get('note_text', '')) > 100:
                note_preview += '...'
            
            self.notes_tree.insert('', 'end', values=(
                formatted_date,
                note.get('topic_name', 'General'),
                note_preview
            ), tags=(tag_id,))

    def handle_add_note(self):
        """Handle add note button"""
        note_text = self.note_text.get('1.0', 'end-1c').strip()
        topic_id = None
        topic_sel = self.note_topic_var.get()
        if topic_sel and topic_sel != "(General)":
            topics = self.app_logic.get_user_subtopics()
            for t in topics:
                label = f"{t['topic_name']} ({t['subject']})"
                if label == topic_sel:
                    topic_id = int(t['topic_id'])
                    break

        success, message = self.app_logic.add_note(note_text, topic_id)

        if success:
            messagebox.showinfo("Success", message)
            self.note_text.delete('1.0', 'end')
            self.refresh_notes_list()
        else:
            messagebox.showerror("Error", message)

    def handle_delete_note(self):
        """Handle delete note button click"""
        selection = self.notes_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a note to delete")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this note?"):
            item = self.notes_tree.item(selection[0])
            raw_tag = item['tags'][0]
            try:
                note_id = int(raw_tag)
            except Exception:
                messagebox.showerror("Error", "Invalid note id")
                return
            
            success, message = self.app_logic.delete_note(note_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_notes_list()
            else:
                messagebox.showerror("Error", message)
    
    # ========== TASK MANAGEMENT ==========
    
    def show_tasks(self):
        """Display task management screen"""
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.current_frame.pack(fill='both', expand=True)
        
        header = tk.Label(
            self.current_frame,
            text="✅ Task Management",
            font=('Ubuntu', 20, 'bold'),
            bg=self.colors['bg_primary'],
            fg=self.colors['accent_purple']
        )
        header.pack(pady=20)
        
        add_frame = tk.LabelFrame(
            self.current_frame, 
            text="Add New Task", 
            font=('Ubuntu', 12, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_purple'],
            relief='solid',
            bd=1
        )
        add_frame.pack(fill='x', padx=30, pady=15)
        
        form_frame = tk.Frame(add_frame, bg=self.colors['bg_secondary'])
        form_frame.pack(padx=20, pady=15)
        
        tk.Label(form_frame, text="Task:", font=('Ubuntu', 11), 
                bg=self.colors['bg_secondary']).grid(row=0, column=0, sticky='w', padx=10, pady=8)
        self.task_entry = tk.Entry(form_frame, width=40, font=('Ubuntu', 10))
        self.task_entry.grid(row=0, column=1, padx=10, pady=8)
        
        tk.Label(form_frame, text="Due Date:", font=('Ubuntu', 11), 
                bg=self.colors['bg_secondary']).grid(row=1, column=0, sticky='w', padx=10, pady=8)
        self.due_date_entry = tk.Entry(form_frame, width=20, font=('Ubuntu', 10))
        self.due_date_entry.insert(0, 'YYYY-MM-DD')
        self.due_date_entry.grid(row=1, column=1, sticky='w', padx=10, pady=8)
        
        tk.Label(form_frame, text="Priority:", font=('Ubuntu', 11), 
                bg=self.colors['bg_secondary']).grid(row=2, column=0, sticky='w', padx=10, pady=8)
        self.priority_var = tk.StringVar(value='medium')
        priority_combo = ttk.Combobox(form_frame, textvariable=self.priority_var, 
                                     values=['low', 'medium', 'high'], width=18, state='readonly')
        priority_combo.grid(row=2, column=1, sticky='w', padx=10, pady=8)
        
        add_btn = UIComponents.create_button(
            form_frame,
            "Add Task",
            self.handle_add_task,
            self.colors['success']
        )
        add_btn.grid(row=3, column=1, pady=15, sticky='e')
        
        list_frame = tk.LabelFrame(
            self.current_frame, 
            text="Your Tasks", 
            font=('Ubuntu', 12, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_purple'],
            relief='solid',
            bd=1
        )
        list_frame.pack(fill='both', expand=True, padx=30, pady=15)
        
        tree_frame = tk.Frame(list_frame, bg=self.colors['bg_secondary'])
        tree_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        columns = ('Status', 'Task', 'Due Date', 'Priority')
        self.tasks_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10, style='Ubuntu.Treeview')
        
        for col in columns:
            self.tasks_tree.heading(col, text=col)
            if col == 'Status':
                self.tasks_tree.column(col, width=80, anchor='center')
            elif col == 'Priority':
                self.tasks_tree.column(col, width=100, anchor='center')
            elif col == 'Due Date':
                self.tasks_tree.column(col, width=120)
            else:
                self.tasks_tree.column(col, width=300)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tasks_tree.yview)
        self.tasks_tree.configure(yscrollcommand=scrollbar.set)
        
        self.tasks_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        btn_frame = tk.Frame(list_frame, bg=self.colors['bg_secondary'])
        btn_frame.pack(pady=10)
        
        toggle_btn = UIComponents.create_button(
            btn_frame,
            "Toggle Status",
            self.handle_toggle_task,
            self.colors['warning']
        )
        toggle_btn.pack(side='left', padx=5)
        
        delete_task_btn = UIComponents.create_button(
            btn_frame,
            "Delete Task",
            self.handle_delete_task,
            self.colors['error']
        )
        delete_task_btn.pack(side='left', padx=5)
        
        back_btn = UIComponents.create_button(
            self.current_frame,
            "← Back to Dashboard",
            self.show_dashboard,
            self.colors['bg_dark']
        )
        back_btn.pack(pady=20)
        
        self.refresh_tasks_list()

    def handle_add_task(self):
        """Handle add task button click"""
        task_text = self.task_entry.get().strip()
        due_date = self.due_date_entry.get().strip()
        priority = self.priority_var.get()
        
        if not task_text:
            messagebox.showerror("Error", "Please enter a task description")
            return
        
        success, message = self.app_logic.add_task(task_text, due_date, priority)
        
        if success:
            messagebox.showinfo("Success", message)
            self.task_entry.delete(0, 'end')
            self.due_date_entry.delete(0, 'end')
            self.due_date_entry.insert(0, 'YYYY-MM-DD')
            self.refresh_tasks_list()
        else:
            messagebox.showerror("Error", message)

    def handle_toggle_task(self):
        """Handle toggle task status button click"""
        selection = self.tasks_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a task to toggle")
            return
        
        item = self.tasks_tree.item(selection[0])
        raw_tag = item['tags'][0]
        try:
            task_id = int(raw_tag)
        except Exception:
            messagebox.showerror("Error", "Invalid task id")
            return
        
        success, message = self.app_logic.toggle_task(task_id)
        
        if success:
            messagebox.showinfo("Success", message)
            self.refresh_tasks_list()
        else:
            messagebox.showerror("Error", message)

    def handle_delete_task(self):
        """Handle delete task button click"""
        selection = self.tasks_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a task to delete")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            item = self.tasks_tree.item(selection[0])
            raw_tag = item['tags'][0]
            try:
                task_id = int(raw_tag)
            except Exception:
                messagebox.showerror("Error", "Invalid task id")
                return
            
            success, message = self.app_logic.delete_task(task_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_tasks_list()
            else:
                messagebox.showerror("Error", message)

    def refresh_tasks_list(self):
        """Refresh the tasks list"""
        for item in self.tasks_tree.get_children():
            self.tasks_tree.delete(item)
        
        tasks = self.app_logic.get_tasks(include_completed=True)
        for task in tasks:
            tag_id = str(task['task_id'])
            status = "✓ Done" if task.get('is_completed') else "○ Pending"
            priority = task.get('priority', 'medium').capitalize()
            
            self.tasks_tree.insert('', 'end', values=(
                status,
                task.get('task_text'),
                task.get('due_date') or 'Not set',
                priority
            ), tags=(tag_id,))
    
    # ========== EXAM MANAGEMENT ==========
    
    def show_exams(self):
        """Display exam management screen"""
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.current_frame.pack(fill='both', expand=True)
        
        header = tk.Label(
            self.current_frame,
            text="🎓 Exam Management",
            font=('Ubuntu', 20, 'bold'),
            bg=self.colors['bg_primary'],
            fg=self.colors['accent_purple']
        )
        header.pack(pady=20)
        
        gen_frame = tk.LabelFrame(
            self.current_frame, 
            text="Generate New Exam", 
            font=('Ubuntu', 12, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_purple'],
            relief='solid',
            bd=1
        )
        gen_frame.pack(fill='x', padx=30, pady=15)
        
        form_frame = tk.Frame(gen_frame, bg=self.colors['bg_secondary'])
        form_frame.pack(padx=20, pady=15)
        
        tk.Label(form_frame, text="Select Topic:", font=('Ubuntu', 11), 
                bg=self.colors['bg_secondary']).grid(row=0, column=0, sticky='w', padx=10, pady=8)
        
        topics = self.app_logic.get_user_subtopics()
        self.topic_var = tk.StringVar()
        self.topic_map = {f"{t['topic_name']} ({t['subject']})": t['topic_id'] for t in topics}
        
        topic_combo = ttk.Combobox(form_frame, textvariable=self.topic_var, 
                                   values=list(self.topic_map.keys()), width=32, state='readonly')
        topic_combo.grid(row=0, column=1, padx=10, pady=8)
        
        tk.Label(form_frame, text="Questions:", font=('Ubuntu', 11), 
                bg=self.colors['bg_secondary']).grid(row=1, column=0, sticky='w', padx=10, pady=8)
        self.count_spin = tk.Spinbox(form_frame, from_=5, to=30, width=10)
        self.count_spin.delete(0, 'end')
        self.count_spin.insert(0, '20')
        self.count_spin.grid(row=1, column=1, sticky='w', padx=10, pady=8)
        
        tk.Label(form_frame, text="Difficulty:", font=('Ubuntu', 11), 
                bg=self.colors['bg_secondary']).grid(row=2, column=0, sticky='w', padx=10, pady=8)
        self.diff_var = tk.StringVar(value='medium')
        diff_combo = ttk.Combobox(form_frame, textvariable=self.diff_var, 
                                 values=['easy', 'medium', 'hard'], width=32, state='readonly')
        diff_combo.grid(row=2, column=1, padx=10, pady=8)
        
        gen_btn = UIComponents.create_button(
            form_frame,
            "Generate Exam",
            self.handle_generate_exam,
            self.colors['accent_orange']
        )
        gen_btn.grid(row=3, column=1, pady=15, sticky='e')
        
        history_frame = tk.LabelFrame(
            self.current_frame, 
            text="Exam History", 
            font=('Ubuntu', 12, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_purple'],
            relief='solid',
            bd=1
        )
        history_frame.pack(fill='both', expand=True, padx=30, pady=15)
        
        tree_frame = tk.Frame(history_frame, bg=self.colors['bg_secondary'])
        tree_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        columns = ('Date', 'Topic', 'Subject', 'Score', 'Questions')
        self.exam_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', 
                                     height=10, style='Ubuntu.Treeview')
        
        for col in columns:
            self.exam_tree.heading(col, text=col)
            if col == 'Score':
                self.exam_tree.column(col, width=80, anchor='center')
            elif col == 'Questions':
                self.exam_tree.column(col, width=100, anchor='center')
            else:
                self.exam_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.exam_tree.yview)
        self.exam_tree.configure(yscrollcommand=scrollbar.set)
        
        self.exam_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        btn_frame = tk.Frame(history_frame, bg=self.colors['bg_secondary'])
        btn_frame.pack(pady=10)
        
        view_results_btn = UIComponents.create_button(
            btn_frame,
            "View Results",
            self.handle_view_exam_results,
            self.colors['info']
        )
        view_results_btn.pack(side='left', padx=5)
        
        back_btn = UIComponents.create_button(
            self.current_frame,
            "← Back to Dashboard",
            self.show_dashboard,
            self.colors['bg_dark']
        )
        back_btn.pack(pady=20)
        
        self.refresh_exam_history()
    
    def handle_generate_exam(self):
        """Handle generate exam button click"""
        topic_name = self.topic_var.get()
        if not topic_name:
            messagebox.showerror("Error", "Please select a topic")
            return
        
        topic_id = self.topic_map[topic_name]
        count = int(self.count_spin.get())
        difficulty = self.diff_var.get()
        
        messagebox.showinfo("Generating...", "Generating exam questions. This may take a moment...")
        
        success, message, exam_id = self.app_logic.start_exam(topic_id, count, difficulty)
        
        if success:
            messagebox.showinfo("Success", message)
            self.take_exam(exam_id)
        else:
            messagebox.showerror("Error", message)
    
    def take_exam(self, exam_id):
        """Display exam taking interface"""
        exam = self.app_logic.get_exam(exam_id)
        if not exam:
            messagebox.showerror("Error", "Exam not found")
            return
        
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.current_frame.pack(fill='both', expand=True)
        
        header = tk.Label(
            self.current_frame,
            text="Taking Exam",
            font=('Ubuntu', 18, 'bold'),
            bg=self.colors['bg_primary'],
            fg=self.colors['accent_purple']
        )
        header.pack(pady=15)
        
        canvas = tk.Canvas(self.current_frame, bg=self.colors['bg_primary'])
        scrollbar = ttk.Scrollbar(self.current_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_primary'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.answer_vars = {}
        questions = exam['questions']
        
        for idx, q in enumerate(questions):
            q_frame = tk.LabelFrame(
                scrollable_frame,
                text=f"Question {idx + 1}",
                font=('Ubuntu', 11, 'bold'),
                bg=self.colors['bg_secondary'],
                fg=self.colors['accent_purple'],
                relief='solid',
                bd=1
            )
            q_frame.pack(fill='x', padx=20, pady=10)
            
            question_text = tk.Label(
                q_frame,
                text=q['question'],
                font=('Ubuntu', 10),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_dark'],
                wraplength=700,
                justify='left'
            )
            question_text.pack(anchor='w', padx=15, pady=(10, 5))
            
            self.answer_vars[idx] = tk.StringVar()
            
            for i, option in enumerate(q['options']):
                option_label = chr(65 + i)
                rb = tk.Radiobutton(
                    q_frame,
                    text=f"{option_label}. {option}",
                    variable=self.answer_vars[idx],
                    value=option_label,
                    font=('Ubuntu', 10),
                    bg=self.colors['bg_secondary'],
                    fg=self.colors['text_dark'],
                    selectcolor=self.colors['bg_primary']
                )
                rb.pack(anchor='w', padx=30, pady=3)
        
        canvas.pack(side='left', fill='both', expand=True, padx=20)
        scrollbar.pack(side='right', fill='y')
        
        submit_btn = UIComponents.create_button(
            self.current_frame,
            "Submit Exam",
            lambda: self.handle_submit_exam(exam_id),
            self.colors['success']
        )
        submit_btn.config(font=('Ubuntu', 12, 'bold'), padx=30, pady=10)
        submit_btn.pack(pady=20)
    
    def handle_submit_exam(self, exam_id):
        """Handle exam submission"""
        answers = {idx: var.get() for idx, var in self.answer_vars.items() if var.get()}
        
        if len(answers) < len(self.answer_vars):
            if not messagebox.askyesno("Warning", "You haven't answered all questions. Submit anyway?"):
                return
        
        success, message, score = self.app_logic.submit_exam(exam_id, answers)
        
        if success:
            messagebox.showinfo("Exam Completed", f"Your score: {score:.1f}%")
            self.show_exam_results(exam_id)
    
    def show_exam_results(self, exam_id):
        """Display detailed exam results"""
        validation = self.app_logic.validate_exam_answers(exam_id)
        if not validation:
            messagebox.showerror("Error", "Cannot load exam results")
            return
        
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.current_frame.pack(fill='both', expand=True)
        
        header = tk.Label(
            self.current_frame,
            text="Exam Results",
            font=('Ubuntu', 18, 'bold'),
            bg=self.colors['bg_primary'],
            fg=self.colors['accent_purple']
        )
        header.pack(pady=15)
        
        score_frame = tk.Frame(self.current_frame, bg=self.colors['bg_secondary'], relief='solid', bd=1)
        score_frame.pack(padx=30, pady=10)
        
        score_pct = (validation['correct'] / validation['total']) * 100
        tk.Label(
            score_frame,
            text=f"Score: {score_pct:.1f}%",
            font=('Ubuntu', 20, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['success'] if score_pct >= 70 else self.colors['error']
        ).pack(pady=10, padx=30)
        
        tk.Label(
            score_frame,
            text=f"Correct: {validation['correct']} | Incorrect: {validation['incorrect']}",
            font=('Ubuntu', 12),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_dark']
        ).pack(pady=(0, 10))
        
        canvas = tk.Canvas(self.current_frame, bg=self.colors['bg_primary'])
        scrollbar = ttk.Scrollbar(self.current_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_primary'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for detail in validation['details']:
            result_frame = tk.LabelFrame(
                scrollable_frame,
                text=f"Question {detail['question_num']} - {'✓ Correct' if detail['is_correct'] else '✗ Incorrect'}",
                font=('Ubuntu', 11, 'bold'),
                bg=self.colors['bg_secondary'],
                fg=self.colors['success'] if detail['is_correct'] else self.colors['error'],
                relief='solid',
                bd=1
            )
            result_frame.pack(fill='x', padx=20, pady=8)
            
            tk.Label(
                result_frame,
                text=detail['question'],
                font=('Ubuntu', 10),
                bg=self.colors['bg_secondary'],
                wraplength=700,
                justify='left'
            ).pack(anchor='w', padx=15, pady=(10, 5))
            
            tk.Label(
                result_frame,
                text=f"Your Answer: {detail['user_answer']}",
                font=('Ubuntu', 10),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_dark']
            ).pack(anchor='w', padx=15, pady=2)
            
            tk.Label(
                result_frame,
                text=f"Correct Answer: {detail['correct_answer']}",
                font=('Ubuntu', 10, 'bold'),
                bg=self.colors['bg_secondary'],
                fg=self.colors['success']
            ).pack(anchor='w', padx=15, pady=2)
            
            tk.Label(
                result_frame,
                text=f"Explanation: {detail['explanation']}",
                font=('Ubuntu', 9, 'italic'),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_dark'],
                wraplength=700,
                justify='left'
            ).pack(anchor='w', padx=15, pady=(2, 10))
        
        canvas.pack(side='left', fill='both', expand=True, padx=20)
        scrollbar.pack(side='right', fill='y')
        
        back_btn = UIComponents.create_button(
            self.current_frame,
            "← Back to Exams",
            self.show_exams,
            self.colors['bg_dark']
        )
        back_btn.pack(pady=15)
    
    def refresh_exam_history(self):
        """Refresh exam history list"""
        for item in self.exam_tree.get_children():
            self.exam_tree.delete(item)
        
        exams = self.app_logic.get_exam_history()
        for exam in exams:
            try:
                date_obj = datetime.strptime(exam['exam_date'], '%Y-%m-%d %H:%M:%S')
                formatted_date = date_obj.strftime('%Y-%m-%d %H:%M')
            except Exception:
                formatted_date = exam['exam_date']
            
            self.exam_tree.insert('', 'end', values=(
                formatted_date,
                exam.get('topic_name') or 'N/A',
                exam.get('subject') or 'N/A',
                f"{(exam.get('score') or 0):.1f}%",
                exam.get('total_questions') or 0
            ), tags=(str(exam['exam_id']),))
    
    def handle_view_exam_results(self):
        """Handle view exam results button"""
        selection = self.exam_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select an exam to view")
            return
        
        item = self.exam_tree.item(selection[0])
        raw_tag = item['tags'][0]
        try:
            exam_id = int(raw_tag)
        except Exception:
            messagebox.showerror("Error", "Invalid exam id")
            return
        self.show_exam_results(exam_id)
    
    # ========== CODE IDE ==========
    
    def show_code_ide(self):
        """Display code IDE interface"""
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.current_frame.pack(fill='both', expand=True)
        
        header = tk.Label(
            self.current_frame,
            text="💻 Code IDE",
            font=('Ubuntu', 18, 'bold'),
            bg=self.colors['bg_primary'],
            fg=self.colors['accent_purple']
        )
        header.pack(pady=20)
        
        code_frame = tk.LabelFrame(
            self.current_frame,
            text="Write and Test Your Code",
            font=('Ubuntu', 12, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_purple'],
            relief='solid',
            bd=1
        )
        code_frame.pack(fill='both', expand=True, padx=30, pady=15)
        
        self.code_text = scrolledtext.ScrolledText(
            code_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=('Courier', 11),
            bg='#1e1e1e',
            fg='#ffffff',
            insertbackground='white'
        )
        self.code_text.pack(fill='both', expand=True, padx=15, pady=15)
        self.code_text.insert('1.0', '# Write your Python code here\n\nprint("Hello, World!")')
        
        btn_frame = tk.Frame(code_frame, bg=self.colors['bg_secondary'])
        btn_frame.pack(pady=10)
        
        run_btn = UIComponents.create_button(
            btn_frame,
            "Run Code",
            self.handle_run_code,
            self.colors['success']
        )
        run_btn.pack(side='left', padx=10)
        
        clear_btn = UIComponents.create_button(
            btn_frame,
            "Clear",
            self.handle_clear_code,
            self.colors['warning']
        )
        clear_btn.pack(side='left', padx=10)
        
        output_frame = tk.LabelFrame(
            code_frame,
            text="Output",
            font=('Ubuntu', 11, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_purple'],
            relief='solid',
            bd=1
        )
        output_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            width=80,
            height=8,
            font=('Courier', 10),
            bg='#2c2c2c',
            fg='#ffffff'
        )
        self.output_text.pack(fill='both', padx=10, pady=10)
        self.output_text.config(state='disabled')
        
        back_btn = UIComponents.create_button(
            self.current_frame,
            "← Back to Dashboard",
            self.show_dashboard,
            self.colors['bg_dark']
        )
        back_btn.pack(pady=20)

    def handle_run_code(self):
        """Handle run code button click"""
        code = self.code_text.get('1.0', 'end-1c')
        
        self.output_text.config(state='normal')
        self.output_text.delete('1.0', 'end')
        
        # Use the safe subprocess method from app_logic
        success, output = self.app_logic.run_code(code, 'python', timeout=5)
        
        self.output_text.insert('1.0', output)
        self.output_text.config(state='disabled')

    def handle_clear_code(self):
        """Handle clear code button click"""
        self.code_text.delete('1.0', 'end')
        self.output_text.config(state='normal')
        self.output_text.delete('1.0', 'end')
        self.output_text.config(state='disabled')

    # ========== CODING PRACTICE ==========
    
    def show_coding_practice(self):
        """Display coding practice interface"""
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.current_frame.pack(fill='both', expand=True)

        # Top bar with back button in black background
        top_bar = tk.Frame(self.current_frame, bg=self.colors['bg_dark'])
        top_bar.pack(fill='x')
        
        back_btn = UIComponents.create_button(
            top_bar,
            "← Back to Dashboard",
            self.show_dashboard,
            self.colors['bg_dark']
        )
        back_btn.pack(side='left', padx=10, pady=10)

        # Header - more compact
        header = tk.Label(
            self.current_frame,
            text="⌨️ Coding Practice",
            font=('Ubuntu', 16, 'bold'),
            bg=self.colors['bg_primary'],
            fg=self.colors['accent_purple']
        )
        header.pack(pady=(10, 5))
        
        # Problem generation frame - compact horizontal layout
        gen_frame = tk.Frame(self.current_frame, bg=self.colors['bg_secondary'], relief='solid', bd=1)
        gen_frame.pack(fill='x', padx=20, pady=5)
        
        # Horizontal form layout
        form_container = tk.Frame(gen_frame, bg=self.colors['bg_secondary'])
        form_container.pack(padx=15, pady=10)
        
        tk.Label(form_container, text="Topic:", font=('Ubuntu', 10, 'bold'),
                bg=self.colors['bg_secondary']).pack(side='left', padx=5)
        self.coding_topic_entry = tk.Entry(form_container, width=20, font=('Ubuntu', 9))
        self.coding_topic_entry.insert(0, "arrays")
        self.coding_topic_entry.pack(side='left', padx=5)
        
        tk.Label(form_container, text="Difficulty:", font=('Ubuntu', 10, 'bold'),
                bg=self.colors['bg_secondary']).pack(side='left', padx=5)
        self.coding_diff_var = tk.StringVar(value='easy')
        diff_combo = ttk.Combobox(form_container, textvariable=self.coding_diff_var,
                                 values=['easy', 'medium', 'hard'], width=10, state='readonly')
        diff_combo.pack(side='left', padx=5)
        
        gen_btn = tk.Button(
            form_container,
            text="Generate Problem",
            command=self.handle_generate_coding_problem,
            bg=self.colors['info'],
            fg='white',
            font=('Ubuntu', 10, 'bold'),
            padx=15,
            pady=5,
            relief='raised',
            bd=2
        )
        gen_btn.pack(side='left', padx=10)
        
        # Main content frame - split into two columns
        content_frame = tk.Frame(self.current_frame, bg=self.colors['bg_primary'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=5)
        
        # Left column - Problem description (40% width)
        left_column = tk.Frame(content_frame, bg=self.colors['bg_secondary'], relief='solid', bd=1)
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        tk.Label(
            left_column,
            text="Problem Description",
            font=('Ubuntu', 11, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_purple']
        ).pack(pady=5)
        
        self.problem_desc_text = scrolledtext.ScrolledText(
            left_column,
            wrap=tk.WORD,
            width=40,
            height=25,
            font=('Ubuntu', 9),
            bg=self.colors['bg_primary']
        )
        self.problem_desc_text.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        self.problem_desc_text.insert('1.0', 'Generate a problem to start coding!')
        self.problem_desc_text.config(state='disabled')
        
        # Right column - Code editor (60% width)
        right_column = tk.Frame(content_frame, bg=self.colors['bg_secondary'], relief='solid', bd=1)
        right_column.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Editor header with Run Tests button
        editor_header = tk.Frame(right_column, bg=self.colors['bg_secondary'])
        editor_header.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            editor_header,
            text="Your Solution",
            font=('Ubuntu', 11, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_purple']
        ).pack(side='left')
        
        # Run Tests button in header - RIGHT SIDE
        self.run_tests_btn = tk.Button(
            editor_header,
            text="▶ Run Tests",
            command=self.handle_submit_coding_solution,
            bg=self.colors['success'],
            fg='white',
            font=('Ubuntu', 10, 'bold'),
            padx=20,
            pady=5,
            relief='raised',
            bd=2,
            cursor='hand2'
        )
        self.run_tests_btn.pack(side='right')
        
        # Code editor
        self.coding_solution_text = scrolledtext.ScrolledText(
            right_column,
            wrap=tk.WORD,
            width=50,
            height=25,
            font=('Courier', 10),
            bg='#1e1e1e',
            fg='#ffffff',
            insertbackground='white'
        )
        self.coding_solution_text.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        self.coding_solution_text.insert('1.0', '# Write your solution here\n\ndef solution():\n    pass')
        
        # Results frame at bottom
        results_container = tk.Frame(self.current_frame, bg=self.colors['bg_primary'])
        results_container.pack(fill='both', padx=20, pady=(0, 10))
        
        tk.Label(
            results_container,
            text="Test Results",
            font=('Ubuntu', 11, 'bold'),
            bg=self.colors['bg_primary'],
            fg=self.colors['accent_purple']
        ).pack(anchor='w', pady=(0, 5))
        
        self.coding_results_frame = tk.Frame(results_container, bg=self.colors['bg_secondary'], relief='solid', bd=1)
        self.coding_results_frame.pack(fill='both', padx=0, pady=0)
        
        # Initial message in results
        tk.Label(
            self.coding_results_frame,
            text="Run tests to see results here",
            font=('Ubuntu', 9, 'italic'),
            bg=self.colors['bg_secondary'],
            fg='gray'
        ).pack(pady=10)

    def handle_generate_coding_problem(self):
        """Handle generate coding problem button click"""
        topic = self.coding_topic_entry.get().strip()
        difficulty = self.coding_diff_var.get()
        
        if not topic:
            messagebox.showerror("Error", "Please enter a topic")
            return
        
        messagebox.showinfo("Generating...", "Generating coding problem. Please wait...")
        
        try:
            problem = self.app_logic.generate_coding_problem(topic, difficulty)
            
            if problem:
                self.display_coding_problem(problem)
            else:
                messagebox.showerror("Error", "Failed to generate problem")
        except Exception as e:
            messagebox.showerror("Error", f"Error generating problem: {str(e)}")
            # Show a test problem anyway for debugging
            test_problem = {
                'title': 'Array Sum Problem',
                'description': '''Write a function called 'array_sum' that takes a list of integers and returns their sum.

Examples:
• array_sum([1, 2, 3]) should return 6
• array_sum([10, 20]) should return 30
• array_sum([5]) should return 5

Hints:
- Use a loop to iterate through the array
- Keep a running total
- Return the final sum''',
                'template': '''# Write your solution here

def array_sum(arr):
    """
    Calculate the sum of all numbers in the array
    
    Args:
        arr: List of integers
    
    Returns:
        Integer sum of all elements
    """
    # Your code here
    total = 0
    # TODO: Implement your solution
    return total
'''
            }
            self.display_coding_problem(test_problem)

    def display_coding_problem(self, problem):
        """Display the generated coding problem in the existing layout"""
        # Update problem description
        self.problem_desc_text.config(state='normal')
        self.problem_desc_text.delete('1.0', 'end')
        
        # Format the problem nicely
        problem_text = f"{problem.get('title', 'Coding Problem')}\n\n"
        problem_text += "=" * 40 + "\n\n"
        problem_text += problem.get('description', 'No description available')
        
        self.problem_desc_text.insert('1.0', problem_text)
        self.problem_desc_text.config(state='disabled')
        
        # Update code editor with template
        self.coding_solution_text.delete('1.0', 'end')
        self.coding_solution_text.insert('1.0', problem.get('template', '# Write your code here\n\ndef solution():\n    pass'))
        
        # Clear previous results
        for widget in self.coding_results_frame.winfo_children():
            widget.destroy()
        
        tk.Label(
            self.coding_results_frame,
            text="Ready! Write your solution and click 'Run Tests'",
            font=('Ubuntu', 10),
            bg=self.colors['bg_secondary'],
            fg=self.colors['info']
        ).pack(pady=15)

    def handle_submit_coding_solution(self):
        """Handle coding solution submission"""
        code = self.coding_solution_text.get('1.0', 'end-1c')
        
        if not code.strip():
            messagebox.showerror("Error", "Please write some code first")
            return
        
        # Clear previous results
        for widget in self.coding_results_frame.winfo_children():
            widget.destroy()
        
        tk.Label(
            self.coding_results_frame,
            text="Running tests... Please wait",
            font=('Ubuntu', 10, 'italic'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['info']
        ).pack(pady=15)
        
        self.root.update()
        
        try:
            # Use fallback test mode directly for now
            # (app_logic method returns incompatible format)
            print("DEBUG: Using fallback test mode")
            results = self.run_basic_code_test(code)
            print(f"DEBUG: Results from fallback: {results}")
            self.display_coding_results(results)
        except Exception as e:
            # Other error - show error message
            print(f"DEBUG: Exception during test execution: {e}")
            import traceback
            traceback.print_exc()
            
            for widget in self.coding_results_frame.winfo_children():
                widget.destroy()
            tk.Label(
                self.coding_results_frame,
                text=f"Error running tests: {str(e)}",
                font=('Ubuntu', 10),
                bg=self.colors['bg_secondary'],
                fg=self.colors['error'],
                wraplength=800
            ).pack(pady=15, padx=10)
    
    def run_basic_code_test(self, code):
        """Fallback method to test code execution"""
        import subprocess
        import sys
        import re
        
        results = {
            'passed': 0,
            'total': 3,
            'score': 0,
            'results': []
        }
        
        # Try to find the function name in the code
        function_match = re.search(r'def\s+(\w+)\s*\(', code)
        if function_match:
            function_name = function_match.group(1)
        else:
            function_name = 'solution'
        
        print(f"DEBUG: Detected function name: {function_name}")
        print(f"DEBUG: Code to test:\n{code}\n")
        
        # Create test cases based on the function
        test_cases = [
            {'input': '[1, 2, 3]', 'expected': '6', 'test_case': 1, 'description': 'Sum of [1,2,3]'},
            {'input': '[10, 20]', 'expected': '30', 'test_case': 2, 'description': 'Sum of [10,20]'},
            {'input': '[5]', 'expected': '5', 'test_case': 3, 'description': 'Sum of [5]'}
        ]
        
        for test in test_cases:
            try:
                # Create test code that calls the function
                test_code = code + f"\n\n# Test execution\ntry:\n    result = {function_name}({test['input']})\n    print(result)\nexcept Exception as e:\n    print(f'ERROR: {{e}}')"
                
                print(f"DEBUG: Running test {test['test_case']}: {test['description']}")
                
                result = subprocess.run(
                    [sys.executable, '-c', test_code],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                stdout = result.stdout.strip()
                stderr = result.stderr.strip()
                
                print(f"DEBUG: Test {test['test_case']} stdout: '{stdout}'")
                print(f"DEBUG: Test {test['test_case']} stderr: '{stderr}'")
                
                # Determine actual output
                if stderr and not stdout:
                    actual = f"Error: {stderr[:80]}"
                    passed = False
                elif stdout.startswith('ERROR:'):
                    actual = stdout
                    passed = False
                else:
                    actual = stdout
                    # Compare as strings
                    passed = str(actual).strip() == str(test['expected']).strip()
                
                if passed:
                    results['passed'] += 1
                
                results['results'].append({
                    'test_case': test['test_case'],
                    'input': test['input'],
                    'expected': test['expected'],
                    'actual': actual if actual else 'No output',
                    'passed': passed
                })
                
            except subprocess.TimeoutExpired:
                print(f"DEBUG: Test {test['test_case']} timed out")
                results['results'].append({
                    'test_case': test['test_case'],
                    'input': test['input'],
                    'expected': test['expected'],
                    'actual': 'Timeout (>5s)',
                    'passed': False
                })
            except Exception as e:
                print(f"DEBUG: Test {test['test_case']} exception: {e}")
                import traceback
                traceback.print_exc()
                results['results'].append({
                    'test_case': test['test_case'],
                    'input': test['input'],
                    'expected': test['expected'],
                    'actual': f'Error: {str(e)[:50]}',
                    'passed': False
                })
        
        results['score'] = (results['passed'] / results['total']) * 100 if results['total'] > 0 else 0
        print(f"DEBUG: Final test results: {results}")
        return results

    def display_coding_results(self, results):
        """Display test results in compact format"""
        print(f"\n=== DEBUG display_coding_results ===")
        print(f"Results received: {results}")
        print(f"Type: {type(results)}")
        if isinstance(results, dict):
            print(f"Keys: {results.keys()}")
            if 'results' in results:
                print(f"Number of test results: {len(results['results'])}")
                for i, tr in enumerate(results['results']):
                    print(f"  Test {i}: {tr}")
        print(f"=== END DEBUG ===\n")
        
        # Clear results frame
        for widget in self.coding_results_frame.winfo_children():
            widget.destroy()
        
        # Validate results structure
        if not results or not isinstance(results, dict):
            tk.Label(
                self.coding_results_frame,
                text="Invalid test results format",
                font=('Ubuntu', 10),
                bg=self.colors['bg_secondary'],
                fg=self.colors['error']
            ).pack(pady=15)
            return
        
        # Results header
        passed = results.get('passed', 0)
        total = results.get('total', 0)
        score = results.get('score', 0)
        
        header_color = self.colors['success'] if passed == total else self.colors['warning']
        
        header_frame = tk.Frame(self.coding_results_frame, bg=header_color)
        header_frame.pack(fill='x')
        
        tk.Label(
            header_frame,
            text=f"Test Results: {passed}/{total} passed ({score:.1f}%)",
            font=('Ubuntu', 12, 'bold'),
            bg=header_color,
            fg='white'
        ).pack(pady=8, padx=10)
        
        # Get test results
        test_results = results.get('results', [])
        
        if not test_results:
            tk.Label(
                self.coding_results_frame,
                text="No test results available",
                font=('Ubuntu', 10),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_dark']
            ).pack(pady=15)
            return
        
        # Create scrollable frame for test results
        canvas = tk.Canvas(self.coding_results_frame, bg=self.colors['bg_secondary'], height=150)
        scrollbar = ttk.Scrollbar(self.coding_results_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_secondary'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Individual test results - compact format
        for test_result in test_results:
            try:
                status = "✓" if test_result.get('passed', False) else "✗"
                status_color = self.colors['success'] if test_result.get('passed', False) else self.colors['error']
                
                test_frame = tk.Frame(scrollable_frame, bg=self.colors['bg_primary'], relief='solid', bd=1)
                test_frame.pack(fill='x', padx=5, pady=3)
                
                # Safely get values with defaults
                test_case = test_result.get('test_case', '?')
                test_input = test_result.get('input', 'N/A')
                expected = test_result.get('expected', 'N/A')
                actual = test_result.get('actual', 'N/A')
                
                # Compact single line display
                result_text = f"{status} Test {test_case}: Input={test_input} | Expected={expected} | Got={actual}"
                
                tk.Label(
                    test_frame,
                    text=result_text,
                    font=('Ubuntu', 9),
                    bg=self.colors['bg_primary'],
                    fg=status_color,
                    anchor='w'
                ).pack(fill='x', padx=8, pady=5)
            except Exception as e:
                # Show error for this specific test
                tk.Label(
                    scrollable_frame,
                    text=f"Error displaying test: {str(e)}",
                    font=('Ubuntu', 9),
                    bg=self.colors['bg_primary'],
                    fg=self.colors['error']
                ).pack(fill='x', padx=5, pady=3)
        
        canvas.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side='right', fill='y', pady=5)

    # ========== STREAK VIEW ==========
    
    def show_streak_view(self):
        """Display streak visualization"""
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.current_frame.pack(fill='both', expand=True)
        
        header = tk.Label(
            self.current_frame,
            text="🔥 Learning Streak",
            font=('Ubuntu', 18, 'bold'),
            bg=self.colors['bg_primary'],
            fg=self.colors['accent_purple']
        )
        header.pack(pady=20)
        
        streak_info = self.app_logic.get_streak_data()
        current_streak = self.app_logic.get_current_streak()
        
        stats_frame = tk.Frame(self.current_frame, bg=self.colors['bg_primary'])
        stats_frame.pack(pady=20)
        
        current_streak_label = tk.Label(
            stats_frame,
            text=f"Current Streak: {current_streak} days",
            font=('Ubuntu', 16, 'bold'),
            bg=self.colors['bg_primary'],
            fg=self.colors['success']
        )
        current_streak_label.pack(pady=10)
        
        calendar_frame = tk.LabelFrame(
            self.current_frame,
            text="Recent Activity",
            font=('Ubuntu', 12, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_purple'],
            relief='solid',
            bd=1
        )
        calendar_frame.pack(fill='both', expand=True, padx=30, pady=15)
        
        canvas = tk.Canvas(calendar_frame, bg=self.colors['bg_secondary'])
        scrollbar = ttk.Scrollbar(calendar_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_secondary'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        study_days = list(streak_info.keys())
        today = date.today()
        
        for i in range(30):
            day = today - timedelta(days=29-i)
            day_str = day.strftime('%Y-%m-%d')
            
            day_frame = tk.Frame(scrollable_frame, bg=self.colors['bg_secondary'])
            day_frame.pack(fill='x', padx=20, pady=5)
            
            date_label = tk.Label(
                day_frame,
                text=day.strftime('%b %d'),
                font=('Ubuntu', 10),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_dark'],
                width=10
            )
            date_label.pack(side='left')
            
            if day_str in study_days:
                status_text = "✓ Studied"
                color = self.colors['success']
            else:
                status_text = "○ No activity"
                color = self.colors['border']
            
            status_label = tk.Label(
                day_frame,
                text=status_text,
                font=('Ubuntu', 10, 'bold'),
                bg=self.colors['bg_secondary'],
                fg=color
            )
            status_label.pack(side='left', padx=20)
        
        canvas.pack(side='left', fill='both', expand=True, padx=20)
        scrollbar.pack(side='right', fill='y')
        
        back_btn = UIComponents.create_button(
            self.current_frame,
            "← Back to Dashboard",
            self.show_dashboard,
            self.colors['bg_dark']
        )
        back_btn.pack(pady=20)
    
    def handle_logout(self):
        """Handle user logout"""
        if messagebox.askyesno("Confirm", "Are you sure you want to sign out?"):
            self.app_logic.logout_user()
            self.show_login_screen()

    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = StudyTrackerApp()
    app.run()