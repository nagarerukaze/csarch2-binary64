import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import main
import re

def on_button_click():
    # Base 2 or Base 10 Selector
    input_text1 = dropdown_var.get()
    # Exponent Value
    input_text2 = entry2.get()
    # Check if any input field is empty
    if input_text1 == "" or input_text2 == "":
        error_label.config(text="Please fill in all input fields.", fg="red")
        output_label.config(text="")
    else:
        # Check if the dropdown is set to "Base 2" and if the mantissa contains only valid binary digits
        if input_text1 == "Base 2":
            if check_b2input_format(input_text2):
                binary_result = main.toBinary64(input_text2, 2)
                error_label.config(text="")
                # Format the output text
                formatted_binary_result = binary_result[:1] + " " + binary_result[1:11] + " " + binary_result[11:]
                binary_output = format_binary_result(formatted_binary_result)
                binary_text = f"Binary: {binary_output}"
                binary_result_text = f"Binary Result: {formatted_binary_result}"
                hex_result = hex(int(binary_result, 2))
                hex_text = f"Hexadecimal: {hex_result}"
                case_result = check_special_case(binary_result)
                case_text = f"Special Case:{case_result}"

                output_text = f"{binary_text}\n{binary_result_text}\n{hex_text}\n{case_text}"
                output_label.config(text=output_text)
            else:
                error_label.config(text="Invalid input format. Please enter in the format: '0.1 x 2^-15'")
        else:
    # If the input matches the pattern, proceed with conversion
            if check_b10input_format(input_text2):
                binary_result = main.toBinary64(input_text2, 10)
                error_label.config(text="")
                formatted_binary_result = binary_result[:1] + " " + binary_result[1:11] + " " + binary_result[11:]
                binary_output = format_binary_result(formatted_binary_result)
                binary_text = f"Binary: {binary_output}"
                binary_result_text = f"Binary Result: {formatted_binary_result}"
                hex_result = hex(int(binary_result, 2))
                hex_text = f"Hexadecimal: {hex_result}"
                case_result = check_special_case(binary_result)
                case_text = f"Special Case: {case_result}"

                output_text = f"{binary_text}\n{binary_result_text}\n{hex_text}\n{case_text}"
                output_label.config(text=output_text)
            else:
                error_label.config(text="Input format is invalid. Please use the format -5.24 x 10^-51'")


            
            
    
def format_binary_result(binary_result):
    
    if binary_result is None:
        
        return "Error in computing"
        
    else:
        sign_bit = binary_result[0]
        exponent = binary_result[1:12]
        mantissa = binary_result[12:]
        formatted_output = "Sign Bit: {}\nExponent: {}\nMantissa: {}".format(sign_bit, exponent, mantissa)
        return formatted_output

def check_special_case(binary_result2):
    sign_bit = binary_result2[0]
    exponent = binary_result2[1:12]
    mantissa = binary_result2[12:]
    if exponent == '11111111111' and int(mantissa, 2) == 0:
        if sign_bit == '1':
            return '- Infinity'
        else:
            return 'Infinity'
    elif exponent == '11111111111' and int(mantissa, 2) != 0:
        if mantissa[0] == '1':
            return 'qNaN'
        elif binary_result2[0] == '0':
            return 'sNaN'
    if int(exponent, 2) <= 0:
         return 'Denormalized'
    else:
            return 'None'
       



def check_b2input_format(input_text):
    pattern = r'^-?[01]+(\.[01]+)? x 2\^(-?\d+)$'

    if re.match(pattern, input_text):
        return True
    else:
        return False
    
def check_b10input_format(input_text):
    pattern = r'^-?\d+(\.\d+)? x 10\^(-?\d+)$'

    if re.match(pattern, input_text):
        return True
    else:
        return False

def clear_inputs():
    dropdown_var.set(options[0])  # Reset dropdown to "Base 10"
    entry2.delete(0, tk.END)
   
    error_label.config(text="")
    output_label.config(text="")

def save_to_file():
    output_text = output_label.cget("text")
    if output_text == "":
        error_label.config(text="No output to save.", fg="red")
        return
    error_label.config(text="")
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(output_text)
        print("Output saved to:", file_path)

# Create the main window
root = tk.Tk()
root.title("IEEE-754 Binary-64 Floating Point Converter")

# Set the window size and make it unchangeable
root.geometry("600x400")
root.resizable(False, False)

# Create a dropdown menu for the first input
options = ["Base 10", "Base 2"]
dropdown_var = tk.StringVar(root)
dropdown_var.set(options[0])  # default value
dropdown = ttk.Combobox(root, textvariable=dropdown_var, values=options, state="readonly")
dropdown.pack(pady=5)

# Label for the second input field
label2 = tk.Label(root, text="Exponent")
label2.pack_forget()

# Create input fields for Base 2
entry2 = tk.Entry(root, width=30)
entry2.pack(pady=5)
entry2.pack()


# Create input fields for Base 10
label_input = tk.Label(root, text="Input")
label_input.pack()

# Error label
error_label = tk.Label(root, text="", fg="red")
error_label.pack()

# Create a frame for buttons
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, pady=10)

# Create a button for generating output
generate_button = tk.Button(button_frame, text="Convert", command=on_button_click)
generate_button.pack(side=tk.LEFT, padx=5)

# Create a button for clearing inputs
clear_button = tk.Button(button_frame, text="Clear", command=clear_inputs)
clear_button.pack(side=tk.LEFT, padx=5)

# Create a button for saving output to a text file
save_button = tk.Button(button_frame, text="Save to File", command=save_to_file)
save_button.pack(side=tk.LEFT, padx=5)

# Create a label for displaying output
output_label = tk.Label(root, text="")
output_label.pack(pady=10)



# Run the Tkinter event loop
root.mainloop()
