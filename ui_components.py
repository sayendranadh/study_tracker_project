import tkinter as tk

class UIComponents:
    """Reusable UI components for the Study Tracker App"""
    
    @staticmethod
    def create_button(parent, text, command, bg_color, fg_color='#ffffff', 
                     font=('Ubuntu', 11, 'bold'), padx=20, pady=8):
        """
        Create a standardized button with consistent styling
        
        Args:
            parent: Parent widget
            text: Button text
            command: Button command/callback
            bg_color: Background color
            fg_color: Foreground/text color (default: white)
            font: Font tuple (default: Ubuntu 11 bold)
            padx: Horizontal padding (default: 20)
            pady: Vertical padding (default: 8)
        
        Returns:
            tk.Button: Configured button widget
        """
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg=fg_color,
            font=font,
            relief='flat',
            padx=padx,
            pady=pady,
            cursor='hand2',
            activebackground=bg_color,
            activeforeground=fg_color
        )
        
        # Add hover effect
        button.bind('<Enter>', lambda e: button.config(bg=UIComponents._lighten_color(bg_color)))
        button.bind('<Leave>', lambda e: button.config(bg=bg_color))
        
        return button
    
    @staticmethod
    def _lighten_color(hex_color):
        """Lighten a hex color by 10% for hover effect"""
        try:
            # Remove '#' if present
            hex_color = hex_color.lstrip('#')
            
            # Convert to RGB
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            
            # Lighten by 10%
            r = min(255, int(r * 1.1))
            g = min(255, int(g * 1.1))
            b = min(255, int(b * 1.1))
            
            # Convert back to hex
            return f'#{r:02x}{g:02x}{b:02x}'
        except:
            return hex_color
    
    @staticmethod
    def create_label_frame(parent, text, bg_color='#ffffff', fg_color='#762572',
                          font=('Ubuntu', 12, 'bold')):
        """
        Create a standardized label frame
        
        Args:
            parent: Parent widget
            text: Frame title
            bg_color: Background color
            fg_color: Foreground/title color
            font: Font tuple
        
        Returns:
            tk.LabelFrame: Configured label frame widget
        """
        frame = tk.LabelFrame(
            parent,
            text=text,
            font=font,
            bg=bg_color,
            fg=fg_color,
            relief='solid',
            bd=1
        )
        return frame
    
    @staticmethod
    def create_entry(parent, width=30, font=('Ubuntu', 10), 
                    bg_color='#f7f6f5', show=None):
        """
        Create a standardized entry widget
        
        Args:
            parent: Parent widget
            width: Entry width
            font: Font tuple
            bg_color: Background color
            show: Character to show (e.g., '*' for password)
        
        Returns:
            tk.Entry: Configured entry widget
        """
        entry_config = {
            'width': width,
            'font': font,
            'relief': 'solid',
            'bd': 1,
            'bg': bg_color
        }
        
        if show:
            entry_config['show'] = show
        
        entry = tk.Entry(parent, **entry_config)
        return entry
    
    @staticmethod
    def show_info_message(title, message):
        """Show an info message box"""
        from tkinter import messagebox
        messagebox.showinfo(title, message)
    
    @staticmethod
    def show_error_message(title, message):
        """Show an error message box"""
        from tkinter import messagebox
        messagebox.showerror(title, message)
    
    @staticmethod
    def show_warning_message(title, message):
        """Show a warning message box"""
        from tkinter import messagebox
        messagebox.showwarning(title, message)
    
    @staticmethod
    def ask_yes_no(title, message):
        """Show a yes/no dialog"""
        from tkinter import messagebox
        return messagebox.askyesno(title, message)