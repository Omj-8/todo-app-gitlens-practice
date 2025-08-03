import tkinter as tk
from tkinter import messagebox
import json
import os

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ToDo アプリ - GitLens練習用")
        self.root.geometry("400x500")
        
        # データファイルのパス
        self.data_file = "todos.json"
        self.todos = self.load_todos()
        
        self.create_widgets()
        self.refresh_list()
    
    def create_widgets(self):
        # タイトルラベル
        title_label = tk.Label(self.root, text="ToDo リスト", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # 入力フレーム
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=5, padx=10, fill="x")
        
        self.entry = tk.Entry(input_frame, font=("Arial", 12))
        self.entry.pack(side="left", fill="x", expand=True)
        
        add_button = tk.Button(input_frame, text="追加", command=self.add_todo)
        add_button.pack(side="right", padx=(5, 0))
        
        # リストボックス
        list_frame = tk.Frame(self.root)
        list_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=("Arial", 10))
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # ボタンフレーム
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        complete_button = tk.Button(button_frame, text="完了", command=self.complete_todo)
        complete_button.pack(side="left", padx=5)
        
        delete_button = tk.Button(button_frame, text="削除", command=self.delete_todo)
        delete_button.pack(side="left", padx=5)
        
        # エンターキーでタスク追加
        self.entry.bind('<Return>', lambda event: self.add_todo())
    
    def load_todos(self):
        """JSONファイルからToDoリストを読み込み"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_todos(self):
        """ToDoリストをJSONファイルに保存"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.todos, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("エラー", f"保存に失敗しました: {e}")
    
    def add_todo(self):
        """新しいタスクを追加（タスク名と日付）"""
        task = self.entry.get().strip()
        date = tk.simpledialog.askstring("日付入力", "タスクの日付を入力してください（例: 2024-06-01）")
        if task:
            todo_item = {
                "task": task,
                "completed": False,
                "id": len(self.todos) + 1,
                "date": date if date else ""
            }
            self.todos.append(todo_item)
            self.save_todos()
            self.refresh_list()
            self.entry.delete(0, tk.END)
        else:
            messagebox.showwarning("警告", "タスクを入力してください")
    
    def complete_todo(self):
        """選択したタスクを完了にする"""
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            self.todos[index]["completed"] = not self.todos[index]["completed"]
            self.save_todos()
            self.refresh_list()
        else:
            messagebox.showinfo("情報", "タスクを選択してください")
    
    def delete_todo(self):
        """選択したタスクを削除"""
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            task_name = self.todos[index]["task"]
            if messagebox.askyesno("確認", f"'{task_name}' を削除しますか？"):
                del self.todos[index]
                self.save_todos()
                self.refresh_list()
        else:
            messagebox.showinfo("情報", "タスクを選択してください")
    
    def refresh_list(self):
        """リストボックスの表示を更新"""
        self.listbox.delete(0, tk.END)
        for todo in self.todos:
            status = "✓" if todo["completed"] else "○"
            display_text = f"{status} {todo['task']}"
            self.listbox.insert(tk.END, display_text)
            
            # 完了したタスクは色を変更
            if todo["completed"]:
                self.listbox.itemconfig(tk.END, {'fg': 'gray'})
    
    #タスクに優先度を追加する機能を実装する場合は、以下のように変更できます。
    def add_priority(self):
        """タスクに優先度を追加する機能"""
        priority = self.priority_entry.get().strip()
        if priority:
            self.todos[-1]["priority"] = priority
            self.save_todos()
            self.refresh_list()
        else:
            messagebox.showwarning("警告", "優先度を入力してください")

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()