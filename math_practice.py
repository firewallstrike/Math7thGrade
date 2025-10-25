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

init_session_state()

# ============================================================================
# PROBLEM GENERATION FUNCTIONS
# ============================================================================

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
    
    if x_coef == 1:
        answer = f"x"
    elif x_coef == -1:
        answer = f"-x"
    else:
        answer = f"{x_coef}x"
    
    if constant > 0:
        answer += f" + {constant}"
    elif constant < 0:
        answer += f" - {abs(constant)}"
    elif constant == 0 and x_coef != 0:
        pass
    else:
        answer = str(constant)
    
    steps = [
        f"🎯 **First, let's distribute!** Think of {a} as giving something to everyone inside the parentheses.",
        f"   • {a} × {b}x = {a*b}x (multiply {a} times {b}x)",
        f"   • {a} × {c} = {a*c} (multiply {a} times {c})",
        f"📝 Now we have: **{a*b}x + {a*c} + {d}x + {e}**",
        f"🔍 **Combine the x terms** (terms with x stick together!):",
        f"   • {a*b}x + {d}x = **{x_coef}x**",
        f"🔍 **Combine the numbers** (constants stick together!):",
        f"   • {a*c} + {e} = **{constant}**",
        f"✨ **Final Answer: {answer}**"
    ]
    
    hints = [
        f"💡 **Think of it like sharing pizza!** 🍕 The {a} outside needs to multiply with EVERYTHING inside the ( ). It's like if you have {a} groups, and each group gets {b}x and {c}. How much total do you have?",
        f"💡 **Now play matchmaker!** 💑 After distributing, find all your 'x' terms (they're like teammates) and add them up. Then find all your plain numbers and add those up separately. X's hang with X's, numbers hang with numbers!",
        f"💡 **Almost there, superstar!** ⭐ You should have something like __x + __ or __x - __. Just combine those x teammates ({a*b}x and {d}x) and those number buddies ({a*c} and {e})!"
    ]
    
    return expr, answer.replace(" ", ""), steps, hints

def gen_distribute_negative():
    """Generate: -a(bx - c)"""
    a = random.randint(2, 7)
    b = random.randint(2, 8)
    c = random.randint(1, 10)
    
    x_coef = -a * b
    constant = a * c
    
    expr = f"-{a}({b}x - {c})"
    
    if x_coef == -1:
        answer = f"-x + {constant}"
    else:
        answer = f"{x_coef}x + {constant}"
    
    steps = [
        f"⚠️ **Watch out for the negative sign!** When -{a} goes inside:",
        f"   • -{a} × {b}x = **{x_coef}x** (negative × positive = negative)",
        f"   • -{a} × (-{c}) = **+{constant}** (negative × negative = positive! ✨)",
        f"💡 **Remember:** Two negatives make a positive!",
        f"✨ **Final Answer: {answer}**"
    ]
    
    hints = [
        f"💡 **Think of it like taking damage in Fortnite! 🎮** When -{a} multiplies with everything inside, it deals damage (makes things negative). So {b}x takes damage and becomes negative. BUT when it hits -{c} (which is already damaged/negative), it's like using a shield potion - the negative damage actually HEALS it back to positive +{constant}!",
        f"💡 **Here's the magic trick:** 🎩✨ When you multiply two negatives together, they become besties and turn positive! Think: (negative) × (negative) = POSITIVE. So -{a} times -{c} = +{constant}! It's like when two enemies in a game fight each other - they cancel out!",
        f"💡 **You're so close!** 🎯 Just remember: -{a} × {b}x = {x_coef}x (takes damage, stays negative), but -{a} × (-{c}) = +{constant} (negative damage on something already negative = heals it to positive!)"
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
        f"🎯 **Goal:** Get x all by itself on one side!",
        f"**Step 1:** Get rid of {b} by subtracting it from both sides",
        f"   • {a}x + {b} - {b} = {c} - {b}",
        f"   • **{a}x = {c - b}**",
        f"**Step 2:** Divide both sides by {a} to isolate x",
        f"   • {a}x ÷ {a} = {c - b} ÷ {a}",
        f"   • **x = {x_val}**",
        f"✨ **Final Answer: x = {x_val}**"
    ]
    
    hints = [
        f"💡 **Think of it like x is trapped!** 🚪 Right now x is stuck with {b} bothering it. To free x, we need to get rid of {b}. What's the opposite of +{b}? Subtract {b} from BOTH sides (gotta keep it fair!).",
        f"💡 **Now x has a buddy that won't leave!** 👥 You've got {a}x, but we want just plain x. It's like having {a} friends sharing something - divide by {a} to find out what ONE person gets. Do this to BOTH sides!",
        f"💡 **Here's the secret formula:** 🔐 Whatever's NEXT to x, do the opposite! If it's +{b}, subtract {b}. If it's ×{a}, divide by {a}. Just remember: what you do to one side, you MUST do to the other - it's the golden rule of equations!"
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
        f"🎯 **This one has parentheses! Let's break it down:**",
        f"**Step 1:** Distribute {a} into the parentheses",
        f"   • {a} × {b}x = {a*b}x",
        f"   • {a} × {c} = {a*c}",
        f"   • Now we have: **{a*b}x + {a*c} + {d}x + {e} = {f}**",
        f"**Step 2:** Combine like terms on the left side",
        f"   • x terms: {a*b}x + {d}x = **{x_coef}x**",
        f"   • numbers: {a*c} + {e} = **{const}**",
        f"   • Simplified: **{x_coef}x + {const} = {f}**",
        f"**Step 3:** Subtract {const} from both sides",
        f"   • **{x_coef}x = {f - const}**",
        f"**Step 4:** Divide both sides by {x_coef}",
        f"   • **x = {x_val}**",
        f"✨ **Final Answer: x = {x_val}**"
    ]
    
    hints = [
        f"💡 **BOSS LEVEL! 🎮** This is like a combo move! First, handle those parentheses - distribute {a} to everything inside (it's like {a} is giving high-fives to {b}x and {c}). Once you break open those parentheses, you can see what you're really working with!",
        f"💡 **Time to tidy up! 🧹** After distributing, you've got x terms scattered around like toys on the floor. Gather all the x's together (add {a*b}x and {d}x). Then gather all the regular numbers ({a*c} and {e}). Now it looks way simpler, right?",
        f"💡 **Final boss moves! ⚔️** You should have something like {x_coef}x + {const} = {f}. Now it's just a regular equation! Move {const} to the other side, then divide by {x_coef}. You got this!"
    ]
    
    return equation, answer, steps, hints

def generate_new_problem(problem_type):
    """Generate a new problem based on type"""
    if problem_type == 'simplify':
        generators = [gen_distribute_combine, gen_distribute_negative]
        expr, answer, steps, hints = random.choice(generators)()
        return expr, answer, steps, hints, "Simplify:"
    else:  # equations
        generators = [gen_linear_eq, gen_distribute_eq]
        expr, answer, steps, hints = random.choice(generators)()
        return expr, answer, steps, hints, "Solve for x:"

# ============================================================================
# ANSWER CHECKING
# ============================================================================

def check_answer(user_input, correct_answer):
    """Check if answer is correct"""
    try:
        user_input = user_input.replace(" ", "")
        correct_answer = correct_answer.replace(" ", "")
        
        if user_input == correct_answer:
            return True
        
        if "+" in user_input and "+" in correct_answer:
            user_parts = sorted(user_input.split("+"))
            correct_parts = sorted(correct_answer.split("+"))
            if user_parts == correct_parts:
                return True
        
        if "/" in user_input or "/" in correct_answer:
            try:
                return Fraction(user_input) == Fraction(correct_answer)
            except:
                pass
        
        return False
    except:
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
    
    # Store previous problem type to detect changes
    previous_type = st.session_state.problem_type
    
    problem_choice = st.radio(
        "What do you want to practice?",
        ["Simplifying Expressions", "Solving Equations", "Mixed Practice"],
        key="problem_choice"
    )
    
    if problem_choice == "Simplifying Expressions":
        st.session_state.problem_type = 'simplify'
    elif problem_choice == "Solving Equations":
        st.session_state.problem_type = 'equations'
    else:
        st.session_state.problem_type = random.choice(['simplify', 'equations'])
    
    # If problem type changed, generate new problem
    if previous_type != st.session_state.problem_type:
        st.session_state.current_problem = None
        st.rerun()
    
    st.divider()
    
    st.markdown("""
    ### 💡 Tips for Success
    - Take breaks when you need them
    - Use hints if you're stuck
    - It's okay to see the steps
    - Practice makes progress!
    """)

# Main content area
if st.session_state.current_problem is None or st.button("🔄 New Problem", type="primary", use_container_width=True):
    st.session_state.current_problem, st.session_state.current_answer, st.session_state.current_steps, st.session_state.hints, st.session_state.problem_label = generate_new_problem(st.session_state.problem_type)
    st.session_state.show_hint = False
    st.session_state.show_steps = False
    st.session_state.answered = False
    st.session_state.hint_level = 0
    st.rerun()

# Display problem
st.markdown("---")
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown(f"## {st.session_state.problem_label}")
    st.markdown(f"### `{st.session_state.current_problem}`")

st.markdown("---")

# Answer input
if not st.session_state.answered:
    col1, col2 = st.columns([3, 1])
    with col1:
        user_answer = st.text_input(
            "Your Answer:",
            key="answer_input",
            placeholder="Type your answer here...",
            help="Write your answer. For fractions, use / (like 3/4). For expressions with x, write like: 2x + 3"
        )
    with col2:
        st.write("")
        st.write("")
        submit = st.button("✅ Submit", type="primary", use_container_width=True)
    
    # Hint buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💡 Get a Hint", use_container_width=True):
            if st.session_state.hint_level < len(st.session_state.hints):
                st.session_state.show_hint = True
                st.session_state.hint_level += 1
    with col2:
        if st.button("📝 Show All Steps", use_container_width=True):
            st.session_state.show_steps = True
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
    
    # Show steps if requested
    if st.session_state.show_steps:
        st.markdown("### 📖 Solution Steps:")
        for step in st.session_state.current_steps:
            st.markdown(f"<div class='step-box'>{step}</div>", unsafe_allow_html=True)
    
    # Check answer
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
            
        else:
            # Incorrect
            st.session_state.total_questions += 1
            st.session_state.streak = 0
            st.session_state.answered = True
            
            st.error(f"Not quite! The correct answer is: **{st.session_state.current_answer}**")
            
            st.markdown("### 📖 Here's how to solve it:")
            for step in st.session_state.current_steps:
                st.markdown(f"<div class='step-box'>{step}</div>", unsafe_allow_html=True)
            
            st.info("💪 Don't worry! Making mistakes is how we learn. Try another one!")

# If answered, show next button
if st.session_state.answered:
    st.markdown("---")
    if st.button("➡️ Next Problem", type="primary", use_container_width=True):
        st.session_state.current_problem = None
        st.rerun()
