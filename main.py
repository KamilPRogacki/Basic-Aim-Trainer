import matplotlib.pyplot as plt
import numpy as np
import threading
import time
import tkinter as tk

class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.clicked = False

    def contains_point(self, x, y):
        return (x - self.x)**2 + (y - self.y)**2 <= self.radius**2

class AdPopup:
    def __init__(self, elapsed_time, record_time):
        self.root = tk.Tk()
        self.root.title("Your Time")
        if elapsed_time < record_time:
            record_time = elapsed_time  # Update record time if a new lowest time is achieved
        self.label = tk.Label(self.root, text=f"Congratulations! You clicked all circles in {elapsed_time:.2f} seconds. Record time: {record_time:.2f} seconds.")
        self.label.pack(padx=20, pady=20)
        self.close_button = tk.Button(self.root, text="Close", command=self.close)
        self.close_button.pack(padx=20, pady=10)
        self.root.after(10000, self.close)  # Close the pop up window automatically after 10 seconds

    def close(self):
        self.root.destroy()

def on_click(event):
    global start_time, circles, record_time
    if event.inaxes is not None:
        for circle in circles:
            if circle.contains_point(event.xdata, event.ydata):
                if not circle.clicked:
                    circle.clicked = True
                    update_plot()
                    if all(circle.clicked for circle in circles):
                        end_time = time.time()
                        elapsed_time = end_time - start_time
                        print(f"Time taken: {elapsed_time:.2f} seconds")
                        show_ad(elapsed_time, record_time)
                        if elapsed_time < record_time:
                            record_time = elapsed_time
                        break

def show_ad(elapsed_time, record_time):
    popup = AdPopup(elapsed_time, record_time)
    popup.root.mainloop()

def update_plot():
    plt.cla()  # Clear the current plot
    plt.xlim(0, 100)  # Adjust limits as needed
    plt.ylim(0, 100)

    for circle in circles:
        color = 'yellow' if circle.clicked else 'red'
        plt.gca().add_patch(plt.Circle((circle.x, circle.y), circle.radius, color=color, fill=True))

    plt.draw()

# Generate random circles
np.random.seed()  # Seed is NOT set for random position each time
circles = [Circle(np.random.uniform(10, 90), np.random.uniform(10, 90), 2.5) for _ in range(10)]

# Setting up the plot
fig, ax = plt.subplots()
plt.xlim(0, 100)  # Adjust limits 
plt.ylim(0, 100)
plt.title('Aim Trainer')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.grid(True)

# Connect the event handler function to the 'button_press_event' 
cid = fig.canvas.mpl_connect('button_press_event', on_click)

start_time = time.time()
record_time = float('inf')  # Initialize record time
update_plot()  # Plot the circles initially

plt.show()

