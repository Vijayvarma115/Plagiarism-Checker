import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from tkinter import ttk
from collections import Counter
import re
import string
import math
from difflib import SequenceMatcher

class PlagiarismChecker:
    def __init__(self, master):
        self.master = master
        self.master.title("Plagiarism Checker")

        # Text widgets for input
        self.text_widget1 = scrolledtext.ScrolledText(self.master, width=40, height=10, wrap=tk.WORD)
        self.text_widget1.grid(row=0, column=0, padx=10, pady=10)

        self.text_widget2 = scrolledtext.ScrolledText(self.master, width=40, height=10, wrap=tk.WORD)
        self.text_widget2.grid(row=0, column=1, padx=10, pady=10)

        # Entry for setting similarity threshold
        self.threshold_label = tk.Label(self.master, text="Similarity Threshold:")
        self.threshold_label.grid(row=1, column=0, pady=5)

        self.threshold_var = tk.DoubleVar()
        self.threshold_var.set(0.8)  # Default threshold
        self.threshold_entry = tk.Entry(self.master, textvariable=self.threshold_var)
        self.threshold_entry.grid(row=1, column=1, pady=5)

        # Buttons
        self.check_button = tk.Button(self.master, text="Check Plagiarism", command=self.check_plagiarism)
        self.check_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.clear_button = tk.Button(self.master, text="Clear", command=self.clear_text)
        self.clear_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.open_button1 = tk.Button(self.master, text="Open File 1", command=lambda: self.open_file(self.text_widget1))
        self.open_button1.grid(row=4, column=0, pady=5)

        self.open_button2 = tk.Button(self.master, text="Open File 2", command=lambda: self.open_file(self.text_widget2))
        self.open_button2.grid(row=4, column=1, pady=5)

        self.save_button1 = tk.Button(self.master, text="Save File 1", command=lambda: self.save_file(self.text_widget1))
        self.save_button1.grid(row=5, column=0, pady=5)

        self.save_button2 = tk.Button(self.master, text="Save File 2", command=lambda: self.save_file(self.text_widget2))
        self.save_button2.grid(row=5, column=1, pady=5)

        # Label to display result
        self.result_label = tk.Label(self.master, text="")
        self.result_label.grid(row=6, column=0, columnspan=2, pady=10)

        # History of previous checks
        self.history_label = tk.Label(self.master, text="History:")
        self.history_label.grid(row=7, column=0, columnspan=2, pady=5)

        self.history_text = scrolledtext.ScrolledText(self.master, width=60, height=20, wrap=tk.WORD)
        self.history_text.grid(row=8, column=0, columnspan=2, pady=5)



        self.ngram_label = tk.Label(self.master, text="N-gram Value:")
        self.ngram_label.grid(row=2, column=0, pady=5)

        self.ngram_var = tk.IntVar()
        self.ngram_var.set(2)  # Default value for bi-grams
        self.ngram_entry = tk.Entry(self.master, textvariable=self.ngram_var)
        self.ngram_entry.grid(row=2, column=1, pady=5)






        self.similarity_label = tk.Label(self.master, text="Similarity Measure:")
        self.similarity_label.grid(row=2, column=0, pady=5)

        self.similarity_var = tk.StringVar()
        similarity_options = ["Cosine Similarity", "Jaccard Similarity", "Euclidean Distance"]
        self.similarity_combobox = ttk.Combobox(self.master, textvariable=self.similarity_var, values=similarity_options)
        self.similarity_combobox.set("Cosine Similarity")
        self.similarity_combobox.grid(row=2, column=1, pady=5)

        # Entry for custom stop words
        self.stop_words_label = tk.Label(self.master, text="Custom Stop Words (comma-separated):")
        self.stop_words_label.grid(row=3, column=0, pady=5)

        self.stop_words_var = tk.StringVar()
        self.stop_words_entry = tk.Entry(self.master, textvariable=self.stop_words_var)
        self.stop_words_entry.grid(row=3, column=1, pady=5)

        # Dictionary to store history entries
        self.history = {}





    def preprocess_text(self, text):
        # Remove punctuation and convert to lowercase
        text = text.lower()
        text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)

        # Exclude custom stop words
        custom_stop_words = [word.strip() for word in self.stop_words_var.get().split(",")]
        text = ' '.join([word for word in text.split() if word not in custom_stop_words])

        return text
    




    def get_similarity_measure(self):
        selected_measure = self.similarity_var.get()
        if selected_measure == "Cosine Similarity":
            return self.cosine_similarity
        elif selected_measure == "Jaccard Similarity":
            return self.jaccard_similarity
        elif selected_measure == "Euclidean Distance":
            return self.euclidean_distance
        


    def jaccard_similarity(self, set1, set2):
        # Jaccard similarity between two sets
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union != 0 else 0.0
    



    def euclidean_distance(self, vector1, vector2):
        # Euclidean distance between two vectors
        squared_diff = sum((vector1.get(word, 0) - vector2.get(word, 0))**2 for word in set(vector1) | set(vector2))
        return math.sqrt(squared_diff)
    


    def find_similar_indices(self, text1, text2):
        ngram_value = self.ngram_var.get()
        ngrams1 = self.get_ngrams(text1, ngram_value)
        ngrams2 = self.get_ngrams(text2, ngram_value)

        matcher = SequenceMatcher(None, ngrams1, ngrams2)
        similar_blocks = matcher.get_matching_blocks()

        # Convert similar blocks to character indices
        similar_indices = [(block.a, block.a + block.size) for block in similar_blocks]

        return similar_indices
    

    def get_ngrams(self, text, n):
        words = re.findall(r'\w+', text)
        ngrams = zip(*[words[i:] for i in range(n)])
        return [' '.join(gram) for gram in ngrams]
    




    def highlight_similarities(self, text_widget, similar_indices):
        text_widget.tag_configure("highlight", background="yellow")

        for start, end in similar_indices:
            text_widget.tag_add("highlight", f"1.0 + {start}c", f"1.0 + {end}c")


    def preprocess_text(self, text):
        # Remove punctuation and convert to lowercase
        text = text.lower()
        text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)
        return text

    def get_word_frequencies(self, text):
        # Count the frequency of each word in the text
        words = text.split()
        return Counter(words)

    def cosine_similarity(self, vector1, vector2):
        # Calculate the cosine similarity between two vectors
        intersection = set(vector1.keys()) & set(vector2.keys())
        numerator = sum([vector1[x] * vector2[x] for x in intersection])

        sum1 = sum([vector1[x] ** 2 for x in vector1.keys()])
        sum2 = sum([vector2[x] ** 2 for x in vector2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator

    def check_plagiarism(self):
        text1 = self.text_widget1.get("1.0", tk.END)
        text2 = self.text_widget2.get("1.0", tk.END)

        # Preprocess texts
        text1 = self.preprocess_text(text1)
        text2 = self.preprocess_text(text2)

        # Get word frequencies
        freq1 = self.get_word_frequencies(text1)
        freq2 = self.get_word_frequencies(text2)

        # Calculate cosine similarity
        similarity = self.cosine_similarity(freq1, freq2)
        similarity_measure = self.get_similarity_measure()
        similarity = similarity_measure(freq1, freq2)



        # Display result
        result_text = f"Similarity: {similarity:.2%} (Threshold: {self.threshold_var.get():.2%})"
        self.result_label.config(text=result_text)
        


        similar_indices = self.find_similar_indices(text1, text2)
        self.highlight_similarities(self.text_widget1, similar_indices)
        self.highlight_similarities(self.text_widget2, similar_indices)

        # Save the result to history
        history_entry = f"Check: {result_text}\nText 1:\n{text1}\nText 2:\n{text2}\n{'='*40}\n"
        self.history_text.insert(tk.END, history_entry)
        self.history[len(self.history) + 1] = history_entry

        # Check against the threshold
        if similarity >= self.threshold_var.get():
            messagebox.showwarning("Plagiarism Detected", "Plagiarism detected above the threshold!")

    def clear_text(self):
        self.text_widget1.delete(1.0, tk.END)
        self.text_widget2.delete(1.0, tk.END)
        self.result_label.config(text="")

    def open_file(self, text_widget):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", ".txt"), ("All files", ".*")])
        if isinstance(file_path ,tuple ) and file_path:
            file_path=file_path[0]
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    text_widget.delete(1.0, tk.END)  # Clear existing content
                    while True:
                        chunk = file.read(1024)  # Read 1 KB at a time
                        if not chunk:
                            break
                        text_widget.insert(tk.END, chunk)
            except Exception as e:
                error_message = f"Error loading file: {e}"
                print(error_message)  # Print the detailed error to the console
                messagebox.showerror("Error", "Error loading file. Please check the file and try again.")





    def save_file(self, text_widget):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", ".txt"), ("All files", ".*")])
        
        if file_path:
            with open(file_path, 'w') as file:
                content = text_widget.get(1.0, tk.END)
                file.write(content)

# Create the Tkinter root window
root = tk.Tk()

# Create an instance of the PlagiarismChecker class
plagiarism_checker = PlagiarismChecker(root)

# Run the Tkinter event loop
root.mainloop()