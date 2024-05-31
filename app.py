from flask import Flask, render_template, request

# Import necessary libraries (replace with your actual imports)
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Define fuzzy logic system (replace with your existing logic)
# ... (code for fuzzy logic system)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # Define the ranges for each criterion
    product_category = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'product_category')
    product_age = ctrl.Antecedent(np.arange(0, 11, 1), 'product_age')
    inventory_level = ctrl.Antecedent(np.arange(0, 51, 1), 'inventory_level')
    customer_loyalty = ctrl.Antecedent(np.arange(0, 5.1, 0.1), 'customer_loyalty')
    competitor_prices = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'competitor_prices')

    # Define membership functions for each criterion
    product_category['low'] = fuzz.trapmf(product_category.universe, [0, 0, 0.3, 0.5])
    product_category['medium'] = fuzz.trapmf(product_category.universe, [0.3, 0.5, 0.5, 0.7])
    product_category['high'] = fuzz.trapmf(product_category.universe, [0.5, 0.7, 1, 1])

    product_age['low'] = fuzz.trapmf(product_age.universe, [0, 0, 3, 5])
    product_age['medium'] = fuzz.trapmf(product_age.universe, [3, 5, 5, 7])
    product_age['high'] = fuzz.trapmf(product_age.universe, [5, 7, 10, 10])

    inventory_level['low'] = fuzz.trapmf(inventory_level.universe, [0, 0, 20, 30])
    inventory_level['medium'] = fuzz.trapmf(inventory_level.universe, [20, 30, 30, 40])
    inventory_level['high'] = fuzz.trapmf(inventory_level.universe, [30, 40, 50, 50])

    customer_loyalty['low'] = fuzz.trapmf(customer_loyalty.universe, [0, 0, 1, 2])
    customer_loyalty['medium'] = fuzz.trapmf(customer_loyalty.universe, [1, 2, 2, 3])
    customer_loyalty['high'] = fuzz.trapmf(customer_loyalty.universe, [2, 3, 4, 4])

    competitor_prices['low'] = fuzz.trapmf(competitor_prices.universe, [0, 0, 0.7, 0.8])
    competitor_prices['medium'] = fuzz.trapmf(competitor_prices.universe, [0.7, 0.8, 0.8, 0.9])
    competitor_prices['high'] = fuzz.trapmf(competitor_prices.universe, [0.8, 0.9, 1, 1])

    # Define the output variable for Discount
    discount = ctrl.Consequent(np.arange(0, 101, 1), 'discount')
    discount['low'] = fuzz.trapmf(discount.universe, [0, 0, 25, 50])
    discount['medium'] = fuzz.trapmf(discount.universe, [25, 50, 50, 75])
    discount['high'] = fuzz.trapmf(discount.universe, [50, 75, 100, 100])

    # Define fuzzy rules
    rule1 = ctrl.Rule(product_category['high'] & product_age['low'] & inventory_level['high'], discount['high'])
    rule2 = ctrl.Rule(customer_loyalty['high'] & competitor_prices['low'], discount['high'])
    rule3 = ctrl.Rule(product_category['medium'] & product_age['medium'], discount['medium'])
    rule4 = ctrl.Rule(customer_loyalty['low'] & competitor_prices['high'], discount['low'])
    rule5 = ctrl.Rule(product_category['medium'] & inventory_level['high'] & customer_loyalty['medium'], discount['medium'])
    rule6 = ctrl.Rule(product_age['high'] & competitor_prices['high'], discount['high'])


    # Create the control system
    discount_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4,rule5,rule6])

    # Create a simulation for this control system
    discount_simulation = ctrl.ControlSystemSimulation(discount_ctrl)


    # Extract user input from form data
    product_category = float(request.form['product_category'])
    product_age = float(request.form['product_age'])
    inventory_level = float(request.form['inventory_level'])
    customer_loyalty = float(request.form['customer_loyalty'])
    competitor_prices = float(request.form['competitor_prices'])

    # Set input values based on user input
    discount_simulation.input['product_category'] = product_category
    discount_simulation.input['product_age'] = product_age
    discount_simulation.input['inventory_level'] = inventory_level
    discount_simulation.input['customer_loyalty'] = customer_loyalty
    discount_simulation.input['competitor_prices'] = competitor_prices

    # Perform the computation
    discount_simulation.compute()

    # Get the output value
    print(discount_simulation.output['discount'])


    # Compute the result
    discount_simulation.compute()

    # Output the fuzzy result
    fuzzy_output = discount_simulation.output['discount']
    print(f"Fuzzy output (discount): {fuzzy_output}")

    # Normalize the fuzzy output score
    def normalize(value, min_val, max_val):
        return (value - min_val) / (max_val - min_val)

    # Example normalization
    normalized_discount = normalize(fuzzy_output, 0, 100)
    print(f"Normalized discount: {normalized_discount}")

    # Define weights for each criterion
    weights = {
        'product_category': 0.1,
        'product_age': 0.9,
        'inventory_level': 0.5,
        'customer_loyalty': 0.3,
        'competitor_prices': 0.2
    }

    # Define the alternatives
    alternatives = {
        'Low Discount': 0.3,
        'Medium Discount': 0.5,
        'High Discount': 0.8
    }

    # Calculate utility scores
    utility_scores = {alt: sum(weights[crit] * score for crit, score in weights.items()) for alt, score in alternatives.items()}

    print(f"Utility Scores: {utility_scores}")

    # Rank the alternatives
    ranked_alternatives = sorted(utility_scores.items(), key=lambda item: item[1], reverse=True)
    print(f"Ranked Alternatives: {ranked_alternatives}")

    # Select the best alternative
    best_alternative = ranked_alternatives[0][0]
    print(f"Best Alternative: {best_alternative}")

    # Determine the recommended discount based on logic (replace if needed)
    recommended_discount = "Low" if normalized_discount < 0.33 else ("Medium" if normalized_discount < 0.66 else "High")

    return render_template('index.html', result=normalized_discount, recommendation=recommended_discount)

if __name__ == '__main__':
    app.run(debug=True)
