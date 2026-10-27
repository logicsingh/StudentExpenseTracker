"""Student Expense Tracker: a beginner-friendly desktop application using Tkinter and SQLite."""
from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import date
from pathlib import Path

import database as db

BG = "#f3f6fb"
NAVY = "#172554"
BLUE = "#2563eb"
TEXT = "#172033"
MUTED = "#64748b"
WHITE = "#ffffff"


class ExpenseTrackerApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Student Expense Tracker")
        self.geometry("1100x740")
        self.minsize(960, 650)
        self.configure(bg=BG)
        db.initialize_database(seed_demo=False)
        self._configure_styles()
        self._build_ui()
        self.refresh()

    def _configure_styles(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview", background=WHITE, foreground=TEXT, fieldbackground=WHITE,
                        rowheight=30, font=("Segoe UI", 10), borderwidth=0)
        style.configure("Treeview.Heading", background="#e8eef8", foreground=NAVY,
                        font=("Segoe UI", 10, "bold"), padding=8)
        style.map("Treeview", background=[("selected", "#dbeafe")], foreground=[("selected", NAVY)])
        style.configure("TCombobox", padding=6)

    def _build_ui(self) -> None:
        header = tk.Frame(self, bg=NAVY, padx=24, pady=18)
        header.pack(fill="x")
        tk.Label(header, text="Student Expense Tracker", bg=NAVY, fg=WHITE,
                 font=("Segoe UI", 22, "bold")).pack(anchor="w")
        tk.Label(header, text="Track spending. Understand habits. Stay in control.", bg=NAVY,
                 fg="#cbd5e1", font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 0))

        body = tk.Frame(self, bg=BG, padx=20, pady=16)
        body.pack(fill="both", expand=True)
        cards = tk.Frame(body, bg=BG)
        cards.pack(fill="x", pady=(0, 14))
        self.total_value = self._stat_card(cards, "ALL-TIME SPENDING", "₹0.00", 0)
        self.month_value = self._stat_card(cards, "THIS MONTH", "₹0.00", 1)
        self.count_value = self._stat_card(cards, "RECORDED EXPENSES", "0", 2)

        form = tk.LabelFrame(body, text=" Add an expense ", bg=WHITE, fg=NAVY,
                             font=("Segoe UI", 10, "bold"), padx=12, pady=10, bd=1, relief="solid")
        form.pack(fill="x", pady=(0, 14))
        self.date_var = tk.StringVar(value=date.today().isoformat())
        self.category_var = tk.StringVar(value=db.CATEGORIES[0])
        self.description_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self._field(form, "Date (YYYY-MM-DD)", self.date_var, 0, 0, width=17)
        tk.Label(form, text="Category", bg=WHITE, fg=MUTED, font=("Segoe UI", 9)).grid(row=0, column=2, sticky="w", padx=(12, 4))
        ttk.Combobox(form, textvariable=self.category_var, values=db.CATEGORIES, state="readonly", width=17).grid(row=1, column=2, sticky="ew", padx=(12, 4), pady=(4, 0))
        self._field(form, "Description", self.description_var, 4, 4, width=30)
        self._field(form, "Amount (₹)", self.amount_var, 6, 6, width=13)
        ttk.Button(form, text="+ Add Expense", command=self.add).grid(row=1, column=8, padx=(12, 0), pady=(4, 0), sticky="ew")
        for col in (0, 2, 4, 6, 8):
            form.grid_columnconfigure(col, weight=1)

        toolbar = tk.Frame(body, bg=BG)
        toolbar.pack(fill="x", pady=(0, 8))
        tk.Label(toolbar, text="Expense history", bg=BG, fg=NAVY, font=("Segoe UI", 14, "bold")).pack(side="left")
        self.search_var = tk.StringVar()
        search = ttk.Entry(toolbar, textvariable=self.search_var, width=25)
        search.pack(side="right", padx=(8, 0))
        search.bind("<KeyRelease>", lambda _event: self.refresh_table())
        ttk.Button(toolbar, text="Export CSV", command=self.export).pack(side="right", padx=(8, 0))
        ttk.Button(toolbar, text="Delete Selected", command=self.delete_selected).pack(side="right")

        table_frame = tk.Frame(body, bg=WHITE, bd=1, relief="solid")
        table_frame.pack(fill="both", expand=True)
        columns = ("id", "date", "category", "description", "amount")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        for col, title, width, anchor in [
            ("id", "ID", 55, "center"), ("date", "Date", 115, "center"),
            ("category", "Category", 145, "w"), ("description", "Description", 430, "w"),
            ("amount", "Amount (₹)", 130, "e")]:
            self.tree.heading(col, text=title)
            self.tree.column(col, width=width, anchor=anchor, stretch=(col == "description"))
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)

        self.status_var = tk.StringVar(value="Ready. Add an expense to get started.")
        tk.Label(self, textvariable=self.status_var, bg="#e8eef8", fg=MUTED,
                 anchor="w", padx=20, pady=8, font=("Segoe UI", 9)).pack(fill="x", side="bottom")

    def _stat_card(self, parent: tk.Widget, label: str, value: str, column: int) -> tk.Label:
        card = tk.Frame(parent, bg=WHITE, padx=16, pady=12, highlightbackground="#dbe3ef", highlightthickness=1)
        card.grid(row=0, column=column, sticky="ew", padx=(0 if column == 0 else 10, 0))
        parent.grid_columnconfigure(column, weight=1)
        tk.Label(card, text=label, bg=WHITE, fg=MUTED, font=("Segoe UI", 9, "bold")).pack(anchor="w")
        value_label = tk.Label(card, text=value, bg=WHITE, fg=BLUE, font=("Segoe UI", 20, "bold"))
        value_label.pack(anchor="w", pady=(5, 0))
        return value_label

    def _field(self, parent: tk.Widget, label: str, variable: tk.StringVar, label_col: int,
               entry_col: int, width: int) -> None:
        tk.Label(parent, text=label, bg=WHITE, fg=MUTED, font=("Segoe UI", 9)).grid(
            row=0, column=label_col, sticky="w", padx=(0 if label_col == 0 else 12, 4))
        entry = ttk.Entry(parent, textvariable=variable, width=width)
        entry.grid(row=1, column=entry_col, sticky="ew", padx=(0 if label_col == 0 else 12, 4), pady=(4, 0))

    def add(self) -> None:
        try:
            db.add_expense(self.date_var.get(), self.category_var.get(), self.description_var.get(), self.amount_var.get())
        except ValueError as exc:
            messagebox.showwarning("Check your input", str(exc), parent=self)
            return
        except Exception as exc:
            messagebox.showerror("Could not save expense", f"The expense could not be saved.\nDetails: {exc}", parent=self)
            return
        self.description_var.set("")
        self.amount_var.set("")
        self.refresh()
        self.status_var.set("Expense saved successfully.")

    def refresh_table(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in db.list_expenses(self.search_var.get()):
            self.tree.insert("", "end", values=(row["id"], row["expense_date"], row["category"],
                                                  row["description"], f'{row["amount"]:,.2f}'))

    def refresh(self) -> None:
        summary = db.get_summary()
        self.total_value.config(text=f'₹{summary["total"]:,.2f}')
        self.month_value.config(text=f'₹{summary["month_total"]:,.2f}')
        self.count_value.config(text=str(summary["count"]))
        self.refresh_table()

    def delete_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select an expense", "Please select a row to delete.", parent=self)
            return
        values = self.tree.item(selected[0], "values")
        if not messagebox.askyesno("Confirm deletion", f"Delete expense #{values[0]}? This cannot be undone.", parent=self):
            return
        if db.delete_expense(int(values[0])):
            self.refresh()
            self.status_var.set(f"Expense #{values[0]} deleted.")
        else:
            messagebox.showwarning("Not found", "That expense no longer exists.", parent=self)
            self.refresh()

    def export(self) -> None:
        destination = filedialog.asksaveasfilename(
            parent=self, title="Export expenses", defaultextension=".csv",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*")),
            initialfile="student_expenses.csv")
        if not destination:
            return
        try:
            count = db.export_csv(destination)
        except OSError as exc:
            messagebox.showerror("Export failed", f"Could not write the file.\n{exc}", parent=self)
            return
        messagebox.showinfo("Export complete", f"Exported {count} expense record(s).", parent=self)
        self.status_var.set(f"Exported {count} record(s) to {Path(destination).name}.")


if __name__ == "__main__":
    try:
        ExpenseTrackerApp().mainloop()
    except Exception as exc:
        messagebox.showerror("Application error", f"The application could not start.\n{exc}")
        raise
