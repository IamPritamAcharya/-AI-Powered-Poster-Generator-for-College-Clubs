prompt_label = ttk.Label(input_frame, text="Prompt:")
prompt_label.grid(row=0, column=0, sticky=tk.W, pady=5)
prompt_entry = ttk.Entry(input_frame, width=30)
prompt_entry.grid(row=0, column=1, pady=5, columnspan=2)