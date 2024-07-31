from tkinter import Tk, Canvas, StringVar, Label, Radiobutton, Button, messagebox
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"


class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain) -> None:
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Take a Quiz")
        self.window.geometry("850x530")
        self.window.configure(bg=THEME_COLOR)

        # Display Title
        self.display_title()

        # Creating a canvas for question text, and display question
        self.canvas = Canvas(self.window, width=800, height=150, bg=THEME_COLOR)  # Adjust the height here
        self.question_text = self.canvas.create_text(400, 75,
                                                     text="Question here",
                                                     width=680,
                                                     fill="white",
                                                     font=('Arial', 15, 'italic')
                                                     )
        self.canvas.grid(row=2, column=0, columnspan=2, pady=20, padx=20)
        self.display_question()

        # Declare a StringVar to store user's answer
        self.user_answer = StringVar()

        # Display four options(radio buttons)
        self.opts = self.radio_buttons()
        self.display_options()

        # To show whether the answer is correct or wrong
        self.feedback = Label(self.window, pady=10, font=("Arial", 15, "bold"), bg=THEME_COLOR, fg="white")
        self.feedback.grid(row=3, column=0, columnspan=2)

        # Timer Label
        self.timer_text = Label(self.window, text="Time Left: 0:30", font=("Arial", 14), bg=THEME_COLOR, fg="white")
        self.timer_text.grid(row=4, column=0, columnspan=2, pady=10)

        # Next and Quit Button
        self.buttons()

        # Start the timer
        self.start_timer()

        # Mainloop
        self.window.mainloop()

    def display_title(self):
        """To display title"""

        # Title
        title = Label(self.window, text="Take a Quiz",
                      width=50, bg=THEME_COLOR, fg="white", font=("Arial", 20, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=20)

    def display_question(self):
        """To display the question"""

        q_text = self.quiz.next_question()
        self.canvas.itemconfig(self.question_text, text=q_text)

    def radio_buttons(self):
        """To create four options (radio buttons)"""

        # initialize the list with an empty list of options
        choice_list = []

        # adding the options to the list
        for val in range(4):
            # setting the radio button properties
            radio_btn = Radiobutton(self.window, text="", variable=self.user_answer,
                                    value='', font=("Arial", 14), bg=THEME_COLOR, fg="white", selectcolor=THEME_COLOR)

            # adding the button to the list
            choice_list.append(radio_btn)

        # placing the buttons in a grid layout
        for i, radio_btn in enumerate(choice_list):
            radio_btn.grid(row=i + 5, column=0, pady=5, padx=20, sticky="w")

        # return the radio buttons
        return choice_list

    def display_options(self):
        """To display four options"""

        # deselecting the options
        self.user_answer.set(None)

        # looping over the options to be displayed for the
        # text of the radio buttons.
        for option, radio_btn in zip(self.quiz.current_question.choices, self.opts):
            radio_btn['text'] = option
            radio_btn['value'] = option

    def next_btn(self):
        """To show feedback for each answer and keep checking for more questions"""

        # Check if the answer is correct
        if self.quiz.check_answer(self.user_answer.get()):
            self.feedback["fg"] = "green"
            self.feedback["text"] = 'Correct answer! \U0001F44D'
        else:
            self.feedback['fg'] = 'red'
            self.feedback['text'] = ('\u274E Oops! \n'
                                     f'The right answer is: {self.quiz.current_question.correct_answer}')

        if self.quiz.has_more_questions():
            # Reset the timer
            self.reset_timer()

            # Moves to the next to display the next question and its options
            self.display_question()
            self.display_options()
        else:
            # Stop the timer
            self.stop_timer()

            # if no more questions, then it displays the score
            self.display_result()

    def buttons(self):
        """To show next button and quit button"""

        # The first button is the Next button to move to the
        # next Question
        next_button = Button(self.window, text="Next", command=self.next_btn,
                             width=10, bg="green", fg="white", font=("Arial", 16, "bold"))
        next_button.grid(row=9, column=0, pady=20, padx=20, sticky="w")  # Adjust the row value

        # This is the second button which is used to Quit the window
        quit_button = Button(self.window, text="Quit", command=self.window.destroy,
                             width=5, bg="red", fg="white", font=("Arial", 16, " bold"))
        quit_button.grid(row=9, column=1, pady=20, sticky="e")  # Adjust the row value

    def display_result(self):
        """To display the result using messagebox"""
        correct, wrong, score_percent = self.quiz.get_score()

        correct = f"Correct: {correct}"
        wrong = f"Wrong: {wrong}"

        # calculates the percentage of correct answers
        result = f"Score: {score_percent}%"

        # Shows a message box to display the result
        messagebox.showinfo("Result", f"{result}\n{correct}\n{wrong}")

    def start_timer(self):
        """Start the timer countdown"""
        self.timer_seconds = 30
        self.update_timer()

    def update_timer(self):
        """Update the timer countdown"""
        minutes = self.timer_seconds // 60
        seconds = self.timer_seconds % 60
        timer_text = f"Time Left: {minutes:02d}:{seconds:02d}"

        self.timer_text['text'] = timer_text

        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.window.after(1000, self.update_timer)
        else:
            # If the timer reaches 0, consider it as a wrong answer
            self.feedback['fg'] = 'red'
            self.feedback['text'] = ('\u274E Oops! \n'
                                     f'Time is up! \n'
                                     f'The right answer is: {self.quiz.current_question.correct_answer}')
            self.next_btn()  # Move to the next question

    def reset_timer(self):
        """Reset the timer to the initial value"""
        self.timer_seconds = 30

    def stop_timer(self):
        """Stop the timer"""
        self.timer_text['text'] = "Time's up!"


