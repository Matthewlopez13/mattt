from flask import Flask, render_template_string, request

app = Flask(__name__)

# Function to calculate required Midterm and Final grades
def calculate_required_grades(prelim_grade):
    passing_grade = 75.0
    prelim_weight = 0.20
    midterm_weight = 0.30
    final_weight = 0.50

    # Calculate the required midterm and final grades
    remaining_grade = passing_grade - (prelim_weight * prelim_grade)
    required_midterm_grade = remaining_grade / (midterm_weight + final_weight)
    required_final_grade = remaining_grade / (final_weight + midterm_weight)

    return required_midterm_grade, required_final_grade

@app.route('/', methods=['GET', 'POST'])
def index():
    html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Grade Calculator</title>
    </head>
    <body>
        <h1>Grade Calculator</h1>
        <form method="POST">
            <label for="prelim_grade">Enter your Prelim grade:</label>
            <input type="text" id="prelim_grade" name="prelim_grade" required>
            <button type="submit">Calculate</button>
        </form>
        {% if message %}
            <p>{{ message }}</p>
        {% endif %}
        {% if error %}
            <p style="color: red;">{{ error }}</p>
        {% endif %}
    </body>
    </html>
    '''
    
    if request.method == 'POST':
        try:
            # Get Prelim grade from the form and validate input
            prelim_grade = float(request.form['prelim_grade'])
            if prelim_grade < 0 or prelim_grade > 100:
                return render_template_string(html_template, error='Grade must be between 0 and 100')

            # Calculate the required Midterm and Final grades
            required_midterm_grade, required_final_grade = calculate_required_grades(prelim_grade)

            # Display the result
            if required_midterm_grade > 100 or required_final_grade > 100:
                return render_template_string(html_template, message='It is not possible to pass with the current Prelim grade.', error=True)
            else:
                return render_template_string(html_template, message=f'To pass, you need at least {required_midterm_grade:.2f} in Midterm and {required_final_grade:.2f} in Final.', error=False)

        except ValueError:
            # Handle non-numeric input
            return render_template_string(html_template, error='Please enter a valid number for the Prelim grade.')

    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True)