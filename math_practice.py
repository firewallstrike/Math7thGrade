"""
7th Grade Math Practice - Streamlit Web App
Designed for students with inattentive ADHD

Features:
- Visual, engaging interface
- Break complex problems into small steps
- Positive reinforcement
- No time pressure
- Clear, colorful feedback
"""

import streamlit as st
import random
from fractions import Fraction

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="7th Grade Math Practice",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS for ADHD-friendly design
st.markdown("""
<style>
    .big-emoji {
        font-size: 3em;
        text-align: center;
    }
    .success-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #d4edda;
        border: 2px solid #28a745;
        margin: 10px 0;
        color: #000000;
    }
    @media (prefers-color-scheme: dark) {
        .success-box {
            background-color: #0f5132;
            border: 2px solid #198754;
            color: #ffffff;
        }
    }
    .hint-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #fff3cd;
        border: 2px solid #ffc107;
        margin: 10px 0;
        color: #000000;
    }
    @media (prefers-color-scheme: dark) {
        .hint-box {
            background-color: #664d03;
            border: 2px solid #ffca2c;
            color: #ffffff;
        }
    }
    .step-box {
        padding: 10px;
        border-radius: 5px;
        background-color: #e7f3ff;
        border-left: 4px solid #2196F3;
        margin: 5px 0;
        color: #000000;
    }
    @media (prefers-color-scheme: dark) {
        .step-box {
            background-color: #1a3a52;
            border-left: 4px solid #64b5f6;
            color: #ffffff;
        }
    }
    .streak-fire {
        font-size: 2em;
        animation: pulse 1s infinite;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session_state():
    """Initialize all session state variables"""
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 0
    if 'streak' not in st.session_state:
        st.session_state.streak = 0
    if 'current_problem' not in st.session_state:
        st.session_state.current_problem = None
    if 'current_answer' not in st.session_state:
        st.session_state.current_answer = None
    if 'current_steps' not in st.session_state:
        st.session_state.current_steps = []
    if 'show_hint' not in st.session_state:
        st.session_state.show_hint = False
    if 'show_steps' not in st.session_state:
        st.session_state.show_steps = False
    if 'answered' not in st.session_state:
        st.session_state.answered = False
    if 'problem_type' not in st.session_state:
        st.session_state.problem_type = 'simplify'
    if 'hint_level' not in st.session_state:
        st.session_state.hint_level = 0

init_session_state()

# ============================================================================
# PROBLEM GENERATION FUNCTIONS (Unchanged, as they need to be dynamic)
# ============================================================================

# Helper function to generate an algebraic expression answer string
def format_answer_string(x_coef, constant):
    answer = ""
    
    if x_coef == 1:
        answer = "x"
    elif x_coef == -1:
        answer = "-x"
    elif x_coef != 0:
        answer = f"{x_coef}x"
    
    if constant > 0 and answer:
        answer += f" + {constant}"
    elif constant < 0 and answer:
        answer += f" - {abs(constant)}"
    elif constant != 0 and not answer:
        answer = str(constant)
    elif not answer and constant == 0:
        answer = "0"
        
    return answer.replace(" ", "")

def gen_distribute_combine():
    """Generate: a(bx + c) + dx + e"""
    a = random.randint(-5, 5)
    if a == 0: a = 2
    b = random.randint(2, 8)
    c = random.randint(-10, 10)
    d = random.randint(-8, 8)
    e = random.randint(-10, 10)
    
    x_coef = a * b + d
    constant = a * c + e
    
    expr = f"{a}({b}x + {c}) + {d}x + {e}"
    expr = expr.replace("+ -", "- ").replace("- -", "+ ")
    
    answer = format_answer_string(x_coef, constant)
    
    steps = [
        f"🎯 **First, let's distribute!** Think of {a} as giving something to everyone inside the parentheses.",
        f"   • {a} × {b}x = {a*b}x",
        f"   • {a} × {c} = {a*c}",
        f"📝 Now we have: **{a*b}x {('+' if a*c >= 0 else '-')} {abs(a*c)} {('+' if d >= 0 else '-')} {abs(d)}x {('+' if e >= 0 else '-')} {abs(e)}**",
        f"🔍 **Combine the x terms**: {a*b}x + {d}x = **{x_coef}x**",
        f"🔍 **Combine the numbers**: {a*c} + {e} = **{constant}**",
        f"✨ **Final Answer: {answer}**"
    ]
    
    hints = [
        f"💡 **Think of it like sharing pizza!** 🍕 The {a} outside needs to multiply with EVERYTHING inside the ( ).",
        f"💡 **Now play matchmaker!** 💑 Find all your 'x' terms and add them up. Then find all your plain numbers and add those up separately.",
        f"💡 **Almost there, superstar!** ⭐ Combine your x terms ({a*b}x and {d}x) and your number buddies ({a*c} and {e})!"
    ]
    
    return expr, answer, steps, hints

def gen_distribute_negative():
    """Generate: -a(bx - c)"""
    a = random.randint(2, 7)
    b = random.randint(2, 8)
    c = random.randint(1, 10)
    
    x_coef = -a * b
    constant = a * c
    
    expr = f"-{a}({b}x - {c})"
    
    answer = format_answer_string(x_coef, constant)
    
    steps = [
        f"⚠️ **Watch out for the negative sign!** When -{a} goes inside:",
        f"   • -{a} × {b}x = **{x_coef}x** (negative × positive = negative)",
        f"   • -{a} × (-{c}) = **+{constant}** (negative × negative = positive! ✨)",
        f"💡 **Remember:** Two negatives make a positive!",
        f"✨ **Final Answer: {answer}**"
    ]
    
    hints = [
        f"💡 **Think of it like taking damage! 🎮** The -{a} makes {b}x negative. BUT when it hits -{c}, it's like a shield potion—negative times negative is positive!",
        f"💡 **Here's the magic trick:** 🎩✨ Negative times negative equals POSITIVE. So -{a} times -{c} = +{constant}!",
        f"💡 **You're so close!** 🎯 Just remember: -{a} times a positive is negative, and -{a} times a negative is positive!"
    ]
    
    return expr, answer, steps, hints

def gen_multi_distribute():
    """Generate: a(bx + c) - d(ex + f)"""
    a = random.randint(2, 5)
    b = random.randint(2, 6)
    c = random.randint(1, 8)
    d = random.randint(2, 5)
    e = random.randint(2, 6)
    f = random.randint(1, 8)
    
    x_coef = a * b - d * e
    constant = a * c - d * f
    
    expr = f"{a}({b}x + {c}) - {d}({e}x + {f})"
    
    answer = format_answer_string(x_coef, constant)
    
    steps = [
        f"🎯 **Two sets of parentheses - double the fun!**",
        f"**Step 1:** Distribute {a}: {a*b}x + {a*c}",
        f"**Step 2:** Distribute -{d} (watch signs!): {-d*e}x - {d*f}",
        f"**Step 3:** Combine x terms: {a*b}x + ({-d*e}x) = **{x_coef}x**",
        f"**Step 4:** Combine constants: {a*c} + ({-d*f}) = **{constant}**",
        f"✨ **Final Answer: {answer}**"
    ]
    
    hints = [
        f"💡 **It's like a combo attack! ⚔️** First handle {a}( ), then handle -{d}( ). The negative sign flips signs!",
        f"💡 **Now gather your troops! 🛡️** Round up all the x's together, then round up all the numbers together.",
        f"💡 **Almost done!** 🎯 Just combine those x terms and those number terms!"
    ]
    
    return expr, answer, steps, hints

def gen_fraction_simplify():
    """Generate fraction simplification: (a/b)x + (c/d)x"""
    denominators = [2, 3, 4, 5, 6]
    b = random.choice(denominators)
    d = random.choice(denominators)
    a = random.randint(1, 5)
    c = random.randint(1, 5)
    
    numerator = a * d + c * b
    denominator = b * d
    result = Fraction(numerator, denominator)
    
    expr = f"{a}/{b}x + {c}/{d}x"
    
    if result == 1:
        answer = "x"
    elif result == -1:
        answer = "-x"
    else:
        answer = f"{result}x"
    
    steps = [
        f"🎯 **Combining fractions with x - let's do this!**",
        f"**Step 1:** Find common denominator for {b} and {d}: {b * d}",
        f"**Step 2:** Convert to common denominator: {a * d}/{b * d}x + {c * b}/{b * d}x",
        f"**Step 3:** Add the numerators: {numerator}/{denominator}x",
        f"**Step 4:** Simplify: {result}",
        f"✨ **Final Answer: {answer}**"
    ]
    
    hints = [
        f"💡 **Get them speaking the same language! 🗣️** Convert both fractions to have the same bottom number (denominator).",
        f"💡 **Now add 'em up! ➕** Once they have the same denominator, just add the top numbers. Don't forget the x!",
        f"💡 **Simplify!** If your fraction is like 6/4, simplify it to 3/2."
    ]
    
    return expr, answer.replace(" ", ""), steps, hints

def gen_fraction_simplify_mixed():
    """Generate: (a/b)(cx + d) + ex"""
    b = random.choice([2, 3, 4, 5])
    a = random.randint(1, 4)
    c = random.randint(2, 6)
    d = random.randint(-8, 8)
    e = random.randint(-6, 6)
    
    x_coef = Fraction(a * c + e * b, b)
    constant = Fraction(a * d, b)
    
    expr = f"{a}/{b}({c}x + {d}) + {e}x"
    expr = expr.replace("+ -", "- ")
    
    # Format answer
    answer = ""
    if x_coef == 1:
        answer = "x"
    elif x_coef == -1:
        answer = "-x"
    elif x_coef != 0:
        answer = f"{x_coef}x"
    
    if constant > 0 and answer:
        answer += f" + {constant}"
    elif constant < 0 and answer:
        answer += f" - {abs(constant)}"
    elif constant != 0 and not answer:
        answer = str(constant)
    elif not answer and constant == 0:
        answer = "0"
    
    steps = [
        f"🎯 **Fraction distribution incoming!**",
        f"**Step 1:** Distribute {a}/{b} to everything inside: {Fraction(a*c, b)}x + {Fraction(a*d, b)}",
        f"**Step 2:** Add the leftover {e}x term: {Fraction(a*c, b)}x + {Fraction(a*d, b)} + {e}x",
        f"**Step 3:** Combine x terms: {x_coef}x",
        f"✨ **Final Answer: {answer}**"
    ]
    
    hints = [
        f"💡 **Fractions can distribute too! 🎁** Multiply {a}/{b} with BOTH {c}x and {d}.",
        f"💡 **Mix and match! 🎨** Convert {e}x to a fraction with denominator {b} so you can add it to the other x term.",
        f"💡 **Final lap! 🏁** Add those x terms together. Don't forget the constant {Fraction(a*d,b)}!"
    ]
    
    return expr, answer.replace(" ", ""), steps, hints

def gen_multi_variable_combine():
    """Generate: ax^2 + bx + cy + d + ex^2 + fx + gy + h (Combine like terms)"""
    a = random.randint(1, 8)
    b = random.randint(-10, 10)
    c = random.randint(-8, 8)
    d = random.randint(-10, 10)
    e = random.randint(-6, 6)
    f = random.randint(-10, 10)
    g = random.randint(-8, 8)
    h = random.randint(-10, 10)
    
    x2_coef = a + e
    x_coef = b + f
    y_coef = c + g
    constant = d + h
    
    # Helper for creating terms in the expression/answer
    def format_term(coef, var_str, first_term=False):
        if coef == 0: return ""
        
        sign = "+ " if coef > 0 and not first_term else "" if coef > 0 else "- "
        abs_coef = abs(coef)
        
        if abs_coef == 1 and var_str and var_str != "":
            term = var_str
        elif abs_coef == 1 and not var_str:
            term = str(abs_coef)
        else:
            term = str(abs_coef) + var_str
            
        return (sign + term).strip().replace("+ ", "+")
    
    # Build expression (simplified for brevity)
    expr_parts = [format_term(a, "x^2", True)]
    expr_parts.append(format_term(b, "x"))
    expr_parts.append(format_term(c, "y"))
    expr_parts.append(format_term(d, ""))
    expr_parts.append(format_term(e, "x^2"))
    expr_parts.append(format_term(f, "x"))
    expr_parts.append(format_term(g, "y"))
    expr_parts.append(format_term(h, ""))
    
    expr = " ".join([p.strip() for p in expr_parts if p]).replace(" +", " + ").replace(" -", " - ").strip()
    
    # Build answer
    answer_parts = []
    answer_parts.append(format_term(x2_coef, "x^2", True))
    answer_parts.append(format_term(x_coef, "x"))
    answer_parts.append(format_term(y_coef, "y"))
    answer_parts.append(format_term(constant, ""))
    
    answer = " ".join([p.strip() for p in answer_parts if p]).replace(" +", " + ").replace(" -", " - ").strip()
    if not answer: answer = "0"
    
    steps = [
        f"🎯 **Lots of variables - let's organize!**",
        f"**Step 1:** Identify and group like terms (x², x, y, constants)",
        f"**Step 2:** Combine x² terms: {a}x² + ({e}x²) = **{x2_coef}x²**",
        f"**Step 3:** Combine x terms: {b}x + ({f}x) = **{x_coef}x**",
        f"**Step 4:** Combine y terms: {c}y + ({g}y) = **{y_coef}y**",
        f"**Step 5:** Combine constants: {d} + ({h}) = **{constant}**",
        f"**Step 6:** Write in order: x² terms, x terms, y terms, then constants",
        f"✨ **Final Answer: {answer.replace(' ', '')}**"
    ]
    
    hints = [
        f"💡 **Think of it like sorting laundry! 🧺** Put x² items in one pile, x items in another, y items in another, and numbers in the last pile!",
        f"💡 **Each variable is its own team! 🏆** x² players combine only with x² players. Regular x players combine only with x players, etc.",
        f"💡 **Almost there! 🎯** Write your answer starting with x², then x, then y, then the plain number. Watch your negative signs!"
    ]
    
    return expr, answer.replace(" ", ""), steps, hints

def gen_linear_eq():
    """Generate: ax + b = c"""
    a = random.randint(-10, 10)
    if a == 0: a = 3
    b = random.randint(-15, 15)
    c = random.randint(-20, 20)
    
    x_val = Fraction(c - b, a)
    
    equation = f"{a}x + {b} = {c}".replace("+ -", "- ")
    answer = str(x_val)
    
    steps = [
        f"🎯 **Goal:** Get x all by itself!",
        f"**Step 1:** Get rid of {b} by subtracting it from both sides: **{a}x = {c - b}**",
        f"**Step 2:** Divide both sides by {a} to isolate x: **x = {x_val}**",
        f"✨ **Final Answer: x = {x_val}**"
    ]
    
    hints = [
        f"💡 **First, deal with the lonely number!** Subtract {b} from BOTH sides.",
        f"💡 **Now, get rid of the multiplier!** You have {a}x. The opposite of multiplication is division. Divide BOTH sides by {a} to free the x!",
        f"💡 **Golden Rule:** What you do to one side, you MUST do to the other."
    ]
    
    return equation, answer, steps, hints

def gen_fraction_eq():
    """Generate: x/a + b = c (Equation with a fractional term)"""
    a = random.choice([2, 3, 4, 5])
    b = random.randint(-8, 8)
    k = random.randint(-5, 5)
    if k == 0: k = 2
    c = b + k
    x_val = k * a
    
    equation = f"x/{a} + {b} = {c}".replace("+ -", "- ")
    answer = str(x_val)
    
    steps = [
        f"🎯 **Goal:** Get x all by itself!",
        f"**Step 1:** Subtract {b} from both sides: **x/{a} = {c - b}**",
        f"**Step 2:** Multiply both sides by {a} to isolate x: **x = {x_val}**",
        f"✨ **Final Answer: x = {x_val}**"
    ]
    
    hints = [
        f"💡 **First, deal with the lonely number!** Move {b} to the right side by subtracting it from both sides.",
        f"💡 **Now, get rid of that division!** Multiply BOTH sides by {a} to solve for x!",
        f"💡 **You're so close!** The equation should be simplified to x/{a} = {c-b}."
    ]
    
    return equation, answer, steps, hints

def gen_distribute_eq():
    """Generate: a(bx + c) + dx + e = f"""
    a = random.randint(-4, 4)
    if a == 0: a = 2
    b = random.randint(2, 5)
    c = random.randint(-8, 8)
    d = random.randint(-6, 6)
    e = random.randint(-10, 10)
    f = random.randint(-15, 15)
    
    x_coef = a * b + d
    if x_coef == 0: x_coef = 1
    const = a * c + e
    
    x_val = Fraction(f - const, x_coef)
    
    equation = f"{a}({b}x + {c}) + {d}x + {e} = {f}"
    equation = equation.replace("+ -", "- ").replace("- -", "+ ")
    answer = str(x_val)
    
    steps = [
        f"🎯 **Step 1:** Distribute {a}: {a*b}x + {a*c} + {d}x + {e} = {f}",
        f"**Step 2:** Combine like terms on the left: **{x_coef}x + {const} = {f}**",
        f"**Step 3:** Subtract {const} from both sides: **{x_coef}x = {f - const}**",
        f"**Step 4:** Divide both sides by {x_coef}: **x = {x_val}**",
        f"✨ **Final Answer: x = {x_val}**"
    ]
    
    hints = [
        f"💡 **First, distribute!** Multiply {a} by everything inside the parentheses.",
        f"💡 **Time to tidy up! 🧹** Combine all the x terms and all the plain numbers on the left side.",
        f"💡 **Final boss moves! ⚔️** Move the constant to the right side, then divide by the x coefficient."
    ]
    
    return equation, answer, steps, hints

# ============================================================================
# CACHED RESOURCES
# ============================================================================

@st.cache_resource
def get_generator_sets():
    """Caches the list of generator functions (a static resource)."""
    return {
        'simplify': [
            gen_distribute_combine, 
            gen_distribute_negative,
            gen_multi_distribute,
            gen_fraction_simplify,
            gen_multi_variable_combine,
            gen_fraction_simplify_mixed
        ],
        'equations': [
            gen_linear_eq, 
            gen_distribute_eq, 
            gen_fraction_eq
        ]
    }

def generate_new_problem(problem_type):
    """Generate a new problem based on type."""
    generator_sets = get_generator_sets() # Use the cached list
    
    if problem_type == 'simplify':
        generators = generator_sets['simplify']
        expr, answer, steps, hints = random.choice(generators)()
        return expr, answer, steps, hints, "Simplify:"
    else:  # equations
        generators = generator_sets['equations']
        expr, answer, steps, hints = random.choice(generators)()
        return expr, answer, steps, hints, "Solve for x:"

# ============================================================================
# ANSWER CHECKING
# ============================================================================

def check_answer(user_input, correct_answer):
    """Check if answer is correct. Handles fractions and reordering attempts."""
    try:
        # 1. Clean up inputs (remove all spaces)
        user_input_clean = user_input.replace(" ", "")
        correct_answer_clean = correct_answer.replace(" ", "")
        
        # 2. Direct string comparison (e.g., for equations or simple expressions)
        if user_input_clean == correct_answer_clean:
            return True
        
        # 3. Handle fraction comparison (for numerical answers like x=5/4 or a simplified constant)
        try:
            user_frac = Fraction(user_input_clean)
            correct_frac = Fraction(correct_answer_clean)
            if user_frac == correct_frac:
                return True
        except ValueError:
            pass
        
        # 4. Handle term reordering for algebraic expressions
        def split_and_sort(expression):
            import re
            # Temporarily replace '-' signs with '+-' to split correctly, but handle leading negative
            expression = expression.replace('-', '+-')
            if expression.startswith('+-'):
                expression = expression[1:] 
            
            # Find all terms (including their signs)
            terms = re.findall(r'[+-]?[^+-]+', expression)
            # Clean up leading '+' signs that might be left from the split
            terms = [t.lstrip('+') for t in terms if t.lstrip('+')]
            return sorted(terms)

        user_parts = split_and_sort(user_input_clean)
        correct_parts = split_and_sort(correct_answer_clean)
        
        if user_parts == correct_parts:
            return True

        return False

    except Exception:
        return False

# ============================================================================
# MAIN APP INTERFACE
# ============================================================================

# Header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("🎓 7th Grade Math Practice")
    st.caption("Take your time • No pressure • You've got this! 💪")

# Sidebar - Progress and Settings
with st.sidebar:
    st.header("📊 Your Progress")
    
    if st.session_state.total_questions > 0:
        percentage = (st.session_state.score / st.session_state.total_questions) * 100
        st.metric("Problems Solved", st.session_state.total_questions)
        st.metric("Correct", st.session_state.score)
        st.progress(percentage / 100)
        st.write(f"**{percentage:.0f}% Correct!**")
        
        if st.session_state.streak > 0:
            st.markdown(f"<div class='streak-fire'>🔥 {st.session_state.streak} streak!</div>", unsafe_allow_html=True)
    else:
        st.info("Start solving problems to see your progress!")
    
    st.divider()
    
    st.header("⚙️ Settings")
    
    previous_type = st.session_state.problem_type
    
    problem_choice = st.radio(
        "What do you want to practice?",
        ["Simplifying Expressions", "Solving Equations", "Mixed Practice"],
        key="problem_choice"
    )
    
    # Set problem type based on selection
    if problem_choice == "Simplifying Expressions":
        st.session_state.problem_type = 'simplify'
    elif problem_choice == "Solving Equations":
        st.session_state.problem_type = 'equations'
    
    # If problem type changed, reset problem
    if problem_choice != "Mixed Practice" and previous_type != st.session_state.problem_type:
        st.session_state.current_problem = None
        st.rerun()
    
    st.divider()
    
    # --- GOLDEN RULE REMINDER (Enhanced Visual Cue) ---
    current_rule = ""
    if st.session_state.problem_type == 'simplify':
        current_rule = "Match up the X's with the X's, and the numbers with the numbers! 🍎=🍎"
    else:
        current_rule = "Golden Rule: What you do to one side, you MUST do to the other! ⚖️"
        
    st.info(f"🧠 **Today's Focus:** {current_rule}", icon="⭐")

    st.markdown("""
    ### 💡 Tips for Success
    - Take breaks when you need them
    - Use hints if you're stuck
    - It's okay to see the steps
    - Practice makes progress!
    """)

# Main content area
# Logic to generate a new problem if one isn't loaded or if 'New Problem' is clicked
if st.session_state.current_problem is None:
    # Handle mixed practice randomization on first load or manual reload
    if st.session_state.problem_choice == "Mixed Practice":
        st.session_state.problem_type = random.choice(['simplify', 'equations'])
    
    st.session_state.current_problem, st.session_state.current_answer, st.session_state.current_steps, st.session_state.hints, st.session_state.problem_label = generate_new_problem(st.session_state.problem_type)
    st.session_state.show_hint = False
    st.session_state.show_steps = False
    st.session_state.answered = False
    st.session_state.hint_level = 0
    # NO st.rerun() needed here.

if st.button("🔄 New Problem", type="primary", use_container_width=True):
    # For mixed practice, randomize the type on new problem button click
    if st.session_state.problem_choice == "Mixed Practice":
        st.session_state.problem_type = random.choice(['simplify', 'equations'])
        
    st.session_state.current_problem = None # Triggers the logic above to generate
    st.rerun()


# Display problem
st.markdown("---")
col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    # SIMPLIFIED PROBLEM DISPLAY
    st.markdown(f"## {st.session_state.problem_label} **`{st.session_state.current_problem}`**")

st.markdown("---")

# Answer input
if not st.session_state.answered:
    
    # Use a form for the input and the SUBMIT button only
    with st.form("math_quiz_form", clear_on_submit=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            user_answer = st.text_input(
                "Type your answer here, then click Submit:", # Simplified label
                key="temp_answer_input", 
                placeholder="Example: 2x+5 or x=3/4", # Better placeholder
                help="Write your answer. For fractions, use / (like 3/4)."
            )
        with col2:
            st.write("")
            st.write("")
            submit = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
            
    # Hint/Skip buttons are OUTSIDE the form
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💡 Get a Hint", use_container_width=True):
            st.session_state.show_hint = True
            if st.session_state.hint_level < len(st.session_state.hints):
                st.session_state.hint_level += 1
            st.rerun() 
    with col2:
        if st.button("📝 Show All Steps", use_container_width=True):
            st.session_state.show_steps = True
            st.rerun() 
    with col3:
        if st.button("⏭️ Skip Problem", use_container_width=True):
            st.session_state.current_problem = None
            st.rerun() 
    
    # Show hint if requested
    if st.session_state.show_hint and st.session_state.hint_level > 0:
        hint_index = min(st.session_state.hint_level - 1, len(st.session_state.hints) - 1)
        st.markdown(f"""
        <div class='hint-box'>
        {st.session_state.hints[hint_index]}
        </div>
        """, unsafe_allow_html=True)
    
    # Show steps if requested (Enhanced Visual Cue)
    if st.session_state.show_steps:
        st.markdown("### 📖 Solution Steps:")
        for i, step in enumerate(st.session_state.current_steps):
            st.markdown(f"<div class='step-box'>**Step {i+1}:** {step}</div>", unsafe_allow_html=True)


    # Check answer only if the form was submitted and there is an answer
    if submit and user_answer:
        if check_answer(user_answer, st.session_state.current_answer):
            # Correct!
            st.session_state.score += 1
            st.session_state.total_questions += 1
            st.session_state.streak += 1
            st.session_state.answered = True
            
            celebrations = ["Awesome!", "Perfect!", "You got it!", "Excellent!", "Nailed it!", "Outstanding!", "Amazing!"]
            
            st.markdown(f"""
            <div class='success-box'>
            <div class='big-emoji'>🎉</div>
            <h2 style='text-align: center; color: #28a745;'>{random.choice(celebrations)}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.streak >= 3:
                st.balloons()
                st.markdown(f"<h3 style='text-align: center;'>🔥🔥🔥 {st.session_state.streak} IN A ROW! YOU'RE ON FIRE! 🔥🔥🔥</h3>", unsafe_allow_html=True)
            st.rerun() 
            
        else:
            # Incorrect
            st.session_state.total_questions += 1
            st.session_state.streak = 0
            st.session_state.answered = True
            
            st.error(f"Not quite! The correct answer is: **{st.session_state.current_answer}**")
            
            st.markdown("### 📖 Here's how to solve it:")
            for i, step in enumerate(st.session_state.current_steps):
                st.markdown(f"<div class='step-box'>**Step {i+1}:** {step}</div>", unsafe_allow_html=True)
            
            st.info("💪 Don't worry! Making mistakes is how we learn. Try another one!")
            st.rerun()

# If answered, show next button
if st.session_state.answered:
    st.markdown("---")
    if st.button("➡️ Next Problem", type="primary", use_container_width=True):
        st.session_state.current_problem = None 
        st.rerun()
